# ブライダル画像 割当表（wedding-image-assignment）

> 全62店舗ページのブライダルセクションに配置する結婚式画像の割当。ストーリー5段構成（①悩み→②決意→③達成→④当日→⑤その後）で各段1点、計5点/店。
> **設計方針**: 近接店舗クラスタごとにローテーションし、隣り合う店舗で同一画像を使わない（コンテンツカニバリ回避）。検証済み: 隣接店舗間の画像重複=0、フル組合せのユニーク=60/62（重複2件は東京↔大阪/福岡で地理的に無関係）。
> 画像は `images/wedding/<slug>.webp`。各段の被写体プールは wedding素材37点を意味的に5分割。

## 段プール
- **①悩み/相談**: dress_tight / dress_counseling / commit / commit_group
- **②決意・伴走**: effort_couple×2 / scale / ring_glove×2
- **③達成**: dress_fit / eve×2
- **④挙式当日**: aisle×2 / ring_exchange×2 / toast×2 / bouquet×2 / carry×2 / walk_couple×2 / smile / smile_couple / blessed_couple / cake / speech / welcome×2 / back
- **⑤その後**: album / photo_frame / movie / frame×2


### 港区・都心

| 店舗 | ①悩み | ②決意 | ③達成 | ④当日 | ⑤その後 |
|---|---|---|---|---|---|
| nogizaka-akasaka | dress_tight_01 | effort_couple_01 | dress_fit_01 | aisle_01 | album_01 |
| mita | dress_counseling_01 | effort_couple_02 | eve_01 | aisle_02 | photo_frame_01 |
| shirokanedai | commit_01 | scale_01 | eve_02 | ring_exchange_01 | movie_01 |

### 大田区・馬込

| 店舗 | ①悩み | ②決意 | ③達成 | ④当日 | ⑤その後 |
|---|---|---|---|---|---|
| nishi-magome | commit_group_01 | ring_glove_01 | dress_fit_01 | ring_exchange_02 | frame_01 |
| nishi-magome-annex | dress_tight_01 | ring_glove_02 | eve_01 | toast_01 | frame_02 |
| magome | dress_counseling_01 | effort_couple_01 | eve_02 | toast_02 | album_01 |

### 大田区・池上線

| 店舗 | ①悩み | ②決意 | ③達成 | ④当日 | ⑤その後 |
|---|---|---|---|---|---|
| kita-senzoku | commit_01 | effort_couple_02 | dress_fit_01 | bouquet_01 | photo_frame_01 |
| nagahara | commit_group_01 | scale_01 | eve_01 | bouquet_02 | movie_01 |
| ishikawadai | dress_tight_01 | ring_glove_01 | eve_02 | carry_01 | frame_01 |
| musashi-nitta | dress_counseling_01 | ring_glove_02 | dress_fit_01 | carry_02 | frame_02 |

### 大田区・蒲田/池上

| 店舗 | ①悩み | ②決意 | ③達成 | ④当日 | ⑤その後 |
|---|---|---|---|---|---|
| kamata-hasunuma | commit_01 | effort_couple_01 | eve_01 | walk_couple_01 | album_01 |
| kugahara | commit_group_01 | effort_couple_02 | eve_02 | walk_couple_02 | photo_frame_01 |
| ikegami | dress_tight_01 | scale_01 | dress_fit_01 | smile_01 | movie_01 |
| zoshiki | dress_counseling_01 | ring_glove_01 | eve_01 | smile_couple_01 | frame_01 |
| chidoricho | commit_01 | ring_glove_02 | eve_02 | blessed_couple_01 | frame_02 |
| yukigaya-otsuka | commit_group_01 | effort_couple_01 | dress_fit_01 | cake_01 | album_01 |

### 中野区

| 店舗 | ①悩み | ②決意 | ③達成 | ④当日 | ⑤その後 |
|---|---|---|---|---|---|
| shin-nakano | dress_tight_01 | effort_couple_02 | eve_01 | speech_01 | photo_frame_01 |
| nakano | dress_counseling_01 | scale_01 | eve_02 | welcome_01 | movie_01 |
| numabukuro | commit_01 | ring_glove_01 | dress_fit_01 | welcome_02 | frame_01 |
| nakano-fujimicho | commit_group_01 | ring_glove_02 | eve_01 | back_01 | frame_02 |
| nakano-shimbashi | dress_tight_01 | effort_couple_01 | eve_02 | aisle_01 | album_01 |
| shin-egota | dress_counseling_01 | effort_couple_02 | dress_fit_01 | aisle_02 | photo_frame_01 |

### 世田谷・京王沿線

| 店舗 | ①悩み | ②決意 | ③達成 | ④当日 | ⑤その後 |
|---|---|---|---|---|---|
| taishido | commit_01 | scale_01 | eve_01 | ring_exchange_01 | movie_01 |
| ikenoue | commit_group_01 | ring_glove_01 | eve_02 | ring_exchange_02 | frame_01 |
| meidaimae | dress_tight_01 | ring_glove_02 | dress_fit_01 | toast_01 | frame_02 |
| sasazuka | dress_counseling_01 | effort_couple_01 | eve_01 | toast_02 | album_01 |
| shibuya-shinsen | commit_01 | effort_couple_02 | eve_02 | bouquet_01 | photo_frame_01 |
| okusawa | commit_group_01 | scale_01 | dress_fit_01 | bouquet_02 | movie_01 |

### 杉並・練馬・板橋

| 店舗 | ①悩み | ②決意 | ③達成 | ④当日 | ⑤その後 |
|---|---|---|---|---|---|
| nishi-ogikubo | dress_tight_01 | ring_glove_01 | eve_01 | carry_01 | frame_01 |
| nerima | dress_counseling_01 | ring_glove_02 | eve_02 | carry_02 | frame_02 |
| kami-itabashi | commit_01 | effort_couple_01 | dress_fit_01 | walk_couple_01 | album_01 |

### 文京区

| 店舗 | ①悩み | ②決意 | ③達成 | ④当日 | ⑤その後 |
|---|---|---|---|---|---|
| hakusan | commit_group_01 | effort_couple_02 | eve_01 | walk_couple_02 | photo_frame_01 |
| sendagi | dress_tight_01 | scale_01 | eve_02 | smile_01 | movie_01 |

### 江東・中央・台東

| 店舗 | ①悩み | ②決意 | ③達成 | ④当日 | ⑤その後 |
|---|---|---|---|---|---|
| kiyosumi-shirakawa | dress_counseling_01 | ring_glove_01 | dress_fit_01 | smile_couple_01 | frame_01 |
| kikukawa | commit_01 | ring_glove_02 | eve_01 | blessed_couple_01 | frame_02 |
| higashi-nihonbashi | commit_group_01 | effort_couple_01 | eve_02 | cake_01 | album_01 |
| tsukishima | dress_tight_01 | effort_couple_02 | dress_fit_01 | speech_01 | photo_frame_01 |
| ueno | dress_counseling_01 | scale_01 | eve_01 | welcome_01 | movie_01 |

### 足立・江戸川

| 店舗 | ①悩み | ②決意 | ③達成 | ④当日 | ⑤その後 |
|---|---|---|---|---|---|
| nishi-kasai | commit_01 | ring_glove_01 | eve_02 | welcome_02 | frame_01 |
| umejima-nishiarai | commit_group_01 | ring_glove_02 | dress_fit_01 | back_01 | frame_02 |

### 神奈川・東横/港北

| 店舗 | ①悩み | ②決意 | ③達成 | ④当日 | ⑤その後 |
|---|---|---|---|---|---|
| tsunashima | dress_tight_01 | effort_couple_01 | eve_01 | aisle_01 | album_01 |
| takata-ekimae | dress_counseling_01 | effort_couple_02 | eve_02 | aisle_02 | photo_frame_01 |
| hiyoshi | commit_01 | scale_01 | dress_fit_01 | ring_exchange_01 | movie_01 |
| hakuraku | commit_group_01 | ring_glove_01 | eve_01 | ring_exchange_02 | frame_01 |
| oguchi | dress_tight_01 | ring_glove_02 | eve_02 | toast_01 | frame_02 |
| mitsuzawa-kamicho | dress_counseling_01 | effort_couple_01 | dress_fit_01 | toast_02 | album_01 |

### 神奈川・横浜

| 店舗 | ①悩み | ②決意 | ③達成 | ④当日 | ⑤その後 |
|---|---|---|---|---|---|
| ichigao | commit_01 | effort_couple_02 | eve_01 | bouquet_01 | photo_frame_01 |
| tokaichiba | commit_group_01 | scale_01 | eve_02 | bouquet_02 | movie_01 |
| nakamachidai | dress_tight_01 | ring_glove_01 | dress_fit_01 | carry_01 | frame_01 |
| gumyoji | dress_counseling_01 | ring_glove_02 | eve_01 | carry_02 | frame_02 |
| mitsukyo | commit_01 | effort_couple_01 | eve_02 | walk_couple_01 | album_01 |
| kibogaoka | commit_group_01 | effort_couple_02 | dress_fit_01 | walk_couple_02 | photo_frame_01 |

### 神奈川・鎌倉/川崎

| 店舗 | ①悩み | ②決意 | ③達成 | ④当日 | ⑤その後 |
|---|---|---|---|---|---|
| ofuna | dress_tight_01 | scale_01 | eve_01 | smile_01 | movie_01 |
| kashimada-shinkawasaki | dress_counseling_01 | ring_glove_01 | eve_02 | smile_couple_01 | frame_01 |
| noborito | commit_01 | ring_glove_02 | dress_fit_01 | blessed_couple_01 | frame_02 |

### 大阪

| 店舗 | ①悩み | ②決意 | ③達成 | ④当日 | ⑤その後 |
|---|---|---|---|---|---|
| osaka-fukushima | commit_group_01 | effort_couple_01 | eve_01 | cake_01 | album_01 |
| toyonaka | dress_tight_01 | effort_couple_02 | eve_02 | speech_01 | photo_frame_01 |
| sone | dress_counseling_01 | scale_01 | dress_fit_01 | welcome_01 | movie_01 |
| hattori-tenjin | commit_01 | ring_glove_01 | eve_01 | welcome_02 | frame_01 |
| sojiji | commit_group_01 | ring_glove_02 | eve_02 | back_01 | frame_02 |
| ryokuchi-koen | dress_tight_01 | effort_couple_01 | dress_fit_01 | aisle_01 | album_01 |

### 福岡

| 店舗 | ①悩み | ②決意 | ③達成 | ④当日 | ⑤その後 |
|---|---|---|---|---|---|
| hirao | dress_counseling_01 | effort_couple_02 | eve_01 | aisle_02 | photo_frame_01 |
