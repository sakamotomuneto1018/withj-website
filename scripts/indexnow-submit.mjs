#!/usr/bin/env node
// IndexNow 送信スクリプト（withj-inc.com）
//
// 使い方:
//   INDEXNOW_KEY=xxxx node scripts/indexnow-submit.mjs            # sitemap.xml の全URLを送信
//   INDEXNOW_KEY=xxxx node scripts/indexnow-submit.mjs <url> ...  # 指定URLのみ送信
// （package.json 経由: `npm run indexnow` / `npm run indexnow:urls -- <url> ...`）
//
// APIキーはコードにハードコードせず、環境変数 INDEXNOW_KEY で渡す。
// ルートの .env に `INDEXNOW_KEY=xxxx` を書いておけば自動で読み込む（.env は .gitignore 済み）。
//
// --- 自動化の設計案（今回は未設定・手動運用）------------------------------
// Vercel はデプロイ完了フックが標準では無いため、自動化するなら以下いずれか:
//  (A) GitHub Actions: main への push 時に本スクリプトを実行し、
//      INDEXNOW_KEY を Actions Secrets に登録。差分ページのみ送るなら
//      `git diff --name-only` からURLを組み立てて indexnow:urls に渡す。
//  (B) Vercel Deploy Hook + 外部cron: デプロイ後に本スクリプトを叩く。
//  (C) build コマンドの後処理（postbuild）に組み込む。ただし本サイトは
//      静的配信でビルドが無いため、現状は (A) が最も素直。
// -------------------------------------------------------------------------

import { readFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");

const HOST = "www.withj-inc.com";
const ENDPOINT = "https://api.indexnow.org/indexnow";
const SITEMAP_PATH = join(ROOT, "sitemap.xml");
const INDEXNOW_MAX_URLS = 10000; // IndexNow の1リクエスト上限

// --- .env の最小ローダー（依存ライブラリ不要）---
function loadDotEnv() {
  const envPath = join(ROOT, ".env");
  if (!existsSync(envPath)) return;
  for (const line of readFileSync(envPath, "utf8").split(/\r?\n/)) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/i);
    if (!m) continue;
    const key = m[1];
    let val = m[2].replace(/^["']|["']$/g, "");
    if (process.env[key] === undefined) process.env[key] = val;
  }
}

function getUrlsFromSitemap() {
  const xml = readFileSync(SITEMAP_PATH, "utf8");
  const urls = [];
  const re = /<loc>\s*([^<\s]+)\s*<\/loc>/g;
  let m;
  while ((m = re.exec(xml)) !== null) urls.push(m[1]);
  return urls;
}

async function main() {
  loadDotEnv();

  const key = process.env.INDEXNOW_KEY;
  if (!key) {
    console.error("[IndexNow] エラー: 環境変数 INDEXNOW_KEY が未設定です。");
    console.error("  例: INDEXNOW_KEY=xxxx node scripts/indexnow-submit.mjs");
    process.exit(1);
  }

  const keyLocation = `https://${HOST}/${key}.txt`;

  // 引数があればそのURL群、無ければ sitemap 全URL
  const argUrls = process.argv.slice(2).filter((a) => /^https?:\/\//.test(a));
  let urlList = argUrls.length > 0 ? argUrls : getUrlsFromSitemap();

  // 自ホストのURLのみ許可（IndexNow は keyLocation と同一ホスト必須）
  urlList = urlList.filter((u) => {
    try {
      return new URL(u).host === HOST;
    } catch {
      return false;
    }
  });

  if (urlList.length === 0) {
    console.error("[IndexNow] 送信対象のURLがありません。");
    process.exit(1);
  }
  if (urlList.length > INDEXNOW_MAX_URLS) {
    console.error(
      `[IndexNow] URL数が上限(${INDEXNOW_MAX_URLS})を超えています: ${urlList.length}`
    );
    process.exit(1);
  }

  const payload = { host: HOST, key, keyLocation, urlList };

  console.log(`[IndexNow] host        : ${HOST}`);
  console.log(`[IndexNow] keyLocation : ${keyLocation}`);
  console.log(`[IndexNow] 送信URL件数 : ${urlList.length}`);
  console.log(`[IndexNow] 送信元      : ${argUrls.length > 0 ? "引数指定" : "sitemap.xml"}`);

  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json; charset=utf-8",
    },
    body: JSON.stringify(payload),
  });

  const bodyText = await res.text();
  console.log(`[IndexNow] ステータス  : ${res.status} ${res.statusText}`);
  if (bodyText.trim()) console.log(`[IndexNow] レスポンス  : ${bodyText.trim()}`);

  // IndexNow: 200/202 は受理。それ以外は失敗扱い。
  if (res.status === 200 || res.status === 202) {
    console.log(`[IndexNow] ✓ 送信成功（${urlList.length}件を受理）`);
    process.exit(0);
  } else {
    console.error("[IndexNow] ✗ 送信失敗");
    process.exit(1);
  }
}

main().catch((err) => {
  console.error("[IndexNow] 予期せぬエラー:", err);
  process.exit(1);
});
