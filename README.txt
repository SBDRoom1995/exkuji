EXくじ デモアプリ（ホーム画面に追加できるWebアプリ）

■ 入っているファイル
index.html            アプリ本体
manifest.webmanifest  アプリ名・アイコン・色の設定
sw.js                 オフラインでも開けるようにする仕組み
icons/                アイコン画像
firebase.json         Firebase Hosting に置くときの設定

■ いちばん簡単な試し方（Netlify Drop）
1. パソコンのブラウザで https://app.netlify.com/drop を開く
2. この「exkuji-app」フォルダを、画面にドラッグ＆ドロップする
3. 表示された https://〜.netlify.app のURLをスマホで開く
   ※ 無料アカウントを作らないと、URLは一定時間で消えます。続けて使う場合は登録してください

■ ずっと使う場合（Firebase Hosting・EX-Staffと同じ方法）
1. パソコンでこのフォルダを開き、ターミナルで「firebase login」
2. 「firebase use --add」で、EXくじ用に作ったFirebaseプロジェクトを選ぶ
3. 「firebase deploy --only hosting」
4. 表示された https://〜.web.app のURLをスマホで開く

■ スマホでホーム画面に追加する方法
iPhone：Safariで開く → 下の共有ボタン → 「ホーム画面に追加」 → 「追加」
Android：Chromeで開く → 画面の「ホーム画面に追加」ボタン、またはメニュー（︙）→「アプリをインストール」

■ 注意
・これはデモです。データはそれぞれのスマホの中だけに保存され、ほかの人とは共有されません
・決済・広告・ギフト発行・取引先とのつなぎ込みはまだ入っていません
・ファイルを差し替えて新しくしたときは、sw.js の CACHE='exkuji-v1' の数字を v2 などに変えると、スマホ側も確実に新しくなります
