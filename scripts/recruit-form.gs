/**
 * WITH J 採用応募フォーム受信用 Google Apps Script
 *
 * 【現状】採用ページのフォームは Formspree（トップのお問い合わせと同じ送信先）で稼働中。
 * スプレッドシートへの自動記録に切り替えたくなったら、下記手順でデプロイし、
 * recruit/appointer/index.html と recruit/trainer/index.html の
 * <form> の action を発行された /exec URL に差し替える。
 * （その際は送信スクリプトを JSON POST 方式に戻すこと）
 *
 * 【セットアップ手順】
 * 1. Googleスプレッドシートを新規作成（名前例：「採用応募一覧」）
 * 2. 拡張機能 → Apps Script を開き、このコードを全文貼り付け
 * 3. NOTIFY_TO を確認（デフォルト info@withj-inc.com）
 * 4. デプロイ → 新しいデプロイ → 種類「ウェブアプリ」
 *    - 実行ユーザー：自分
 *    - アクセスできるユーザー：全員
 * 5. 発行されたURL（https://script.google.com/macros/s/…/exec）を
 *    recruit/appointer/index.html と recruit/trainer/index.html の
 *    GAS_URL に貼る
 *
 * ※ コードを修正したら「デプロイを管理 → 編集 → 新バージョン」で
 *   再デプロイしないと反映されません（URLは変わりません）
 */

var NOTIFY_TO = "info@withj-inc.com";
var SHEET_NAME = "応募一覧";
var HEADERS = [
  "受信日時", "職種", "お名前", "年齢", "お住まい",
  "希望勤務エリア", "トレーナー経験", "土日勤務",
  "電話番号", "メールアドレス", "職歴", "対応状況"
];

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);

    // ハニーポット（Bot対策）：companyに値があれば記録せず正常応答
    if (data.company) {
      return jsonResponse({ result: "ok" });
    }

    // --- スプレッドシートに記録 ---
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(SHEET_NAME);
    if (!sheet) {
      sheet = ss.insertSheet(SHEET_NAME);
      sheet.appendRow(HEADERS);
      sheet.setFrozenRows(1);
    }
    sheet.appendRow([
      new Date(),
      data.position || "",
      data.name || "",
      data.age || "",
      data.city || "",
      data.area || "",
      data.experience || "",
      data.weekend || "",
      "'" + (data.tel || ""), // 先頭0が消えないよう文字列扱い
      data.email || "",
      data.career || "",
      "未対応"
    ]);

    // --- 通知メール ---
    var subject = "【応募】" + (data.position || "") + "／" + (data.name || "");
    var body =
      "採用ページから新しい応募がありました。\n\n" +
      "■職種：" + (data.position || "") + "\n" +
      "■お名前：" + (data.name || "") + "\n" +
      "■年齢：" + (data.age || "") + "歳\n" +
      "■お住まい：" + (data.city || "") + "\n" +
      (data.area ? "■希望勤務エリア：" + data.area + "\n" : "") +
      (data.experience ? "■トレーナー経験：" + data.experience + "\n" : "") +
      (data.weekend ? "■土日の勤務可否：" + data.weekend + "\n" : "") +
      "■電話番号：" + (data.tel || "") + "\n" +
      "■メールアドレス：" + (data.email || "") + "\n" +
      "■職歴：\n" + (data.career || "") + "\n\n" +
      "応募一覧シート：" + ss.getUrl();
    MailApp.sendEmail(NOTIFY_TO, subject, body);

    // --- 応募者への自動返信 ---
    if (data.email) {
      MailApp.sendEmail(
        data.email,
        "【株式会社WITH J】ご応募ありがとうございます",
        (data.name || "") + " 様\n\n" +
        "この度は" + (data.position || "") + "職にご応募いただき、誠にありがとうございます。\n" +
        "内容を確認のうえ、担当者より2〜3営業日以内にご連絡いたします。\n\n" +
        "※本メールは自動送信です。\n\n" +
        "──────────────\n" +
        "株式会社WITH J 採用担当\n" +
        "info@withj-inc.com\n" +
        "https://www.withj-inc.com/\n" +
        "──────────────"
      );
    }

    return jsonResponse({ result: "ok" });
  } catch (err) {
    return jsonResponse({ result: "error", message: String(err) });
  }
}

function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
