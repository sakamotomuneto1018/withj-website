# 未公開店舗 不足データレポート

未公開（published:false）: **63店舗**
うち 住所・電話・営業時間が揃っている: **63店舗**（駅・エリア情報を足せば即ページ化可）

公開手順: `data/stores.json` の該当店舗に `stations` / `area_keywords` を追記 → `has_page:true` `published:true` → `python3 scripts/gen_stores.py`

| slug | 店舗名 | 所在 | 住所/電話/時間 | 追記が必要なデータ |
|---|---|---|---|---|
| `mita` | 三田店 | 東京都港区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `shibuya-shinsen` | 渋谷・神泉店 | 東京都渋谷区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `sasazuka` | 笹塚店 | 東京都渋谷区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `shirokanedai-takanawadai` | 白金台・高輪台店 | 東京都品川区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `nishi-magome` | 西馬込店 | 東京都大田区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `nishi-magome-annex` | 西馬込 ANNEX店 | 東京都大田区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `magome` | 馬込店 | 東京都大田区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `kamata-hasunuma` | 蒲田・蓮沼店 | 東京都大田区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `kugahara` | 久が原店 | 東京都大田区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `kita-senzoku` | 北千束店 | 東京都大田区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `nagahara` | 長原店 | 東京都大田区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `ishikawadai` | 石川台店 | 東京都大田区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `musashi-nitta` | 武蔵新田店 | 東京都大田区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `omori-kitaguchi-sanno` | 大森北口山王店 | 東京都大田区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `ikegami` | 池上店 | 東京都大田区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `chidoricho` | 千鳥町店 | 東京都大田区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `kiyosumi-shirakawa` | 清澄白河店 | 東京都江東区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `higashi-nihonbashi` | 東日本橋店 | 東京都中央区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `tsukishima` | 月島店 | 東京都中央区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `nakano` | 中野店 | 東京都中野区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `numabukuro` | 沼袋店 | 東京都中野区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `nakano-fujimicho` | 中野富士見町店 | 東京都中野区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `nakano-shimbashi` | 中野新橋店 | 東京都中野区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `kikukawa` | 菊川店 | 東京都墨田区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `ueno` | 上野店 | 東京都台東区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `taishido` | 太子堂店 | 東京都世田谷区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `ikenoue` | 池ノ上店 | 東京都世田谷区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `meidaimae` | 明大前店 | 東京都世田谷区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `okusawa` | 奥沢店 | 東京都世田谷区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `hakusan` | 白山店 | 東京都文京区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `sendagi` | 千駄木店 | 東京都文京区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `nishi-kasai` | 西葛西店 | 東京都江戸川区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `shin-egota` | 新江古田店 | 東京都練馬区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `kami-itabashi` | 上板橋店 | 東京都板橋区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `umejima-nishiarai` | 梅島/西新井店 | 東京都足立区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `yokohama` | 横浜店 | 神奈川県横浜市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `kishinekoen` | 岸根公園店 | 神奈川県横浜市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `tsunashima` | 綱島店 | 神奈川県横浜市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `ichigao` | 市ヶ尾店 | 神奈川県横浜市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `gumyoji` | 弘明寺店 | 神奈川県横浜市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `takata-ekimae` | 高田駅前店 | 神奈川県横浜市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `tokaichiba` | 十日市場店 | 神奈川県横浜市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `mitsukyo` | 三ツ境店 | 神奈川県横浜市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `ofuna` | 大船店 | 神奈川県横浜市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `nakamachidai` | 仲町台店 | 神奈川県横浜市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `hiyoshi` | 日吉店 | 神奈川県横浜市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `kibogaoka` | 希望ヶ丘店 | 神奈川県横浜市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `mitsuzawa-kamicho` | 三ツ沢上町店 | 神奈川県横浜市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `kashimada-shinkawasaki` | 鹿島田/新川崎店 | 神奈川県川崎市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `noborito` | 登戸店 | 神奈川県川崎市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `omiya` | 大宮店 | 埼玉県さいたま市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `ota` | 太田店 | 群馬県太田市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `fukui` | 福居店 | 栃木県足利市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `fukushima` | 福島店 | 大阪府大阪市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `toyonaka` | 豊中店 | 大阪府豊中市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `sone` | 曽根店 | 大阪府豊中市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `hattori-tenjin` | 服部天神店 | 大阪府豊中市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `sojiji` | 総持寺店 | 大阪府茨木市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `ryokuchi-koen` | 緑地公園店 | 大阪府吹田市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `nagoya-imaike` | 名古屋今池店 | 愛知県名古屋市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `motoyama` | 本山店 | 愛知県名古屋市 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `tenjin` | 天神店 | 福岡県中央区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |
| `hirao` | 平尾店 | 福岡県中央区 | ✅揃 | stations(最寄り駅・路線)、area_keywords(周辺エリア3〜5)、nearby_landmarks(任意) |