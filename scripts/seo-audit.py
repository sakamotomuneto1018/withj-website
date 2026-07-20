#!/usr/bin/env python3
# 技術SEO一括監査（レポート生成用・読み取り専用）
import os, re, json, glob
from html.parser import HTMLParser
from urllib.parse import urldefrag, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Doc(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title=None; self._intitle=False
        self.metas={}   # name/property -> content (last wins, but track dup separately)
        self.meta_desc=None
        self.h1=0
        self.imgs_total=0; self.imgs_noalt=0
        self.jsonld=[]; self._injsonld=False; self._buf=[]
        self.links=[]  # (attr, url)
        self._inh1=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='title': self._intitle=True
        elif tag=='meta':
            key=a.get('name') or a.get('property')
            if key:
                key=key.lower()
                self.metas.setdefault(key,[]).append(a.get('content','') or '')
                if key=='description': self.meta_desc=a.get('content','') or ''
        elif tag=='h1': self.h1+=1
        elif tag=='img':
            self.imgs_total+=1
            if 'alt' not in a or a.get('alt') is None: self.imgs_noalt+=1
            src=a.get('src')
            if src: self.links.append(('img',src))
        elif tag=='a':
            href=a.get('href')
            if href: self.links.append(('a',href))
        elif tag=='link':
            href=a.get('href')
            if href: self.links.append(('link',href))
        elif tag=='script' and a.get('type','').lower()=='application/ld+json':
            self._injsonld=True; self._buf=[]
    def handle_endtag(self, tag):
        if tag=='title': self._intitle=False
        elif tag=='script' and self._injsonld:
            self._injsonld=False
            self.jsonld.append(''.join(self._buf))
    def handle_data(self, data):
        if self._intitle:
            self.title=(self.title or '')+data
        if self._injsonld:
            self._buf.append(data)

def collect_types(objs):
    types=set()
    def walk(o):
        if isinstance(o,dict):
            t=o.get('@type')
            if isinstance(t,str): types.add(t)
            elif isinstance(t,list):
                for x in t:
                    if isinstance(x,str): types.add(x)
            for v in o.values(): walk(v)
            if '@graph' in o: walk(o['@graph'])
        elif isinstance(o,list):
            for x in o: walk(x)
    for o in objs: walk(o)
    return types

def has_address_locality(objs):
    found=[False]
    def walk(o):
        if isinstance(o,dict):
            addr=o.get('address')
            if isinstance(addr,dict) and addr.get('addressLocality'): found[0]=True
            if o.get('addressLocality'): found[0]=True
            for v in o.values(): walk(v)
        elif isinstance(o,list):
            for x in o: walk(x)
    for o in objs: walk(o)
    return found[0]

LOCALBIZ={'LocalBusiness','HealthClub','SportsActivityLocation','ExerciseGym','Gym','Organization'}

def audit_file(path):
    with open(path,encoding='utf-8',errors='replace') as f: html=f.read()
    d=Doc();
    try: d.feed(html)
    except Exception: pass
    objs=[]
    for raw in d.jsonld:
        try: objs.append(json.loads(raw))
        except Exception: pass
    types=collect_types(objs)
    title=(d.title or '').strip()
    desc=(d.meta_desc or '').strip()
    rel=os.path.relpath(path,ROOT)
    # broken internal links
    broken=[]
    base=os.path.dirname(path)
    for attr,url in d.links:
        u=urldefrag(url)[0]
        if not u: continue
        if re.match(r'^(https?:)?//',u) or u.startswith('mailto:') or u.startswith('tel:') or u.startswith('data:') or u.startswith('javascript:'): continue
        u=unquote(u)
        if u.startswith('/'):
            target=os.path.join(ROOT,u.lstrip('/'))
        else:
            target=os.path.normpath(os.path.join(base,u))
        # directory -> index.html
        cand=[target]
        if u.endswith('/') or os.path.isdir(target):
            cand.append(os.path.join(target,'index.html'))
        if not any(os.path.exists(c) for c in cand):
            broken.append(url)
    return {
        'path':rel,
        'title':title,
        'title_len':len(title),
        'desc':desc,
        'desc_len':len(desc),
        'desc_count':len(d.metas.get('description',[])),
        'h1':d.h1,
        'og_title':bool(d.metas.get('og:title')),
        'og_image':bool(d.metas.get('og:image')),
        'imgs_total':d.imgs_total,
        'imgs_noalt':d.imgs_noalt,
        'types':sorted(types),
        'has_localbiz':bool(types & LOCALBIZ),
        'has_addr':has_address_locality(objs),
        'has_faq':'FAQPage' in types,
        'has_breadcrumb':'BreadcrumbList' in types,
        'broken':sorted(set(broken)),
        'roi':'投資回収' in html,
    }

# scope
shops=sorted(glob.glob(os.path.join(ROOT,'shops','*','index.html')))
mains=[os.path.join(ROOT,'index.html'),
       os.path.join(ROOT,'gym-blog','index.html'),
       os.path.join(ROOT,'gym-blog','bridal','index.html'),
       os.path.join(ROOT,'bridal','index.html'),
       os.path.join(ROOT,'faq','index.html')]
mains=[m for m in mains if os.path.exists(m)]

results=[]
for p in shops: r=audit_file(p); r['group']='shop'; results.append(r)
for p in mains: r=audit_file(p); r['group']='main'; results.append(r)

# title duplication
from collections import Counter, defaultdict
tc=Counter(r['title'] for r in results if r['title'])
dups=defaultdict(list)
for r in results:
    if r['title'] and tc[r['title']]>1: dups[r['title']].append(r['path'])

# place-name in shop titles
def has_place(t):
    return bool(re.search(r'駅|区|市|町', t))

json.dump({'results':results,'dups':dups}, open(os.path.join(ROOT,'scripts','_audit.json'),'w'), ensure_ascii=False)

# summary print
print("TOTAL:", len(results), "shops:", len(shops), "mains:", len(mains))
print("=== title dups ===")
for t,ps in dups.items(): print(f"[{len(ps)}] {t[:50]} :: {', '.join(ps)}")
print("=== shop titles missing place ===")
for r in results:
    if r['group']=='shop' and not has_place(r['title']): print(" ", r['path'], "::", r['title'][:60])
print("=== desc issues (missing/dup/<120) ===")
for r in results:
    flags=[]
    if r['desc_count']==0: flags.append('MISSING')
    if r['desc_count']>1: flags.append('DUP')
    if 0<r['desc_len']<120: flags.append(f"SHORT({r['desc_len']})")
    if flags: print(" ", r['path'], flags)
print("=== H1 issues ===")
for r in results:
    if r['h1']!=1: print(" ", r['path'], "h1=",r['h1'])
print("=== localbiz/addr (shops) ===")
for r in results:
    if r['group']=='shop' and (not r['has_localbiz'] or not r['has_addr']):
        print(" ", r['path'], "localbiz=",r['has_localbiz'],"addr=",r['has_addr'])
print("=== faq missing (shops) count ===", sum(1 for r in results if r['group']=='shop' and not r['has_faq']))
print("=== breadcrumb missing ===")
for r in results:
    if not r['has_breadcrumb']: print(" ", r['path'])
print("=== og missing ===")
for r in results:
    if not r['og_title'] or not r['og_image']: print(" ", r['path'],"ogT=",r['og_title'],"ogImg=",r['og_image'])
print("=== img noalt (top offenders) ===")
for r in sorted(results,key=lambda x:-x['imgs_noalt']):
    if r['imgs_noalt']>0: print(" ", r['path'], r['imgs_noalt'],"/",r['imgs_total'])
print("=== broken internal links ===")
for r in results:
    if r['broken']: print(" ", r['path'], r['broken'])
print("=== ROI word ===")
for r in results:
    if r['roi']: print(" ", r['path'])
