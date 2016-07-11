Title: さくらVPSにお名前.comで契約したドメインを関連付けた話
Date: 2016-03-03 22:01
Category: さくらVPS
Tags: さくらVPS, Nginx
Slug: 3rd
Author: lapis_zero09
Summary:さくらVPSにお名前.comで契約したドメインを関連付けた時のHowto．

# さくらVSP

## 対象

  - Nginxのインストールが終わってる状態．
  - お名前.comでドメイン取得済み

## ドメインを関連付ける
[ドメインNavi](http://www.onamae.com/navi/domain.html)にアクセスしてログイン．  

"ネームサーバーの設定"項目から"DNS関連機能の設定"をクリック．  
![犬](./img/third-1.png)

関連付けたいドメインにチェックを入れて，  
"次へ進む"をクリック．  

"DNSレコード設定を利用する"の"設定する"をクリック．  

"ホスト名"欄に"www"と書く．  
"VALUE"欄にIPアドレスを入れる．  
その他はいじらずに追加ボタンをクリック．　

一番下の"DNSレコード設定用ネームサーバー変更確認"欄にチェックを入れて，  
"確認画面に進む"をクリック．

後はなりゆきに任せる．

## Nginx側の設定
`nginx.conf` をいじる．  
`server_name`  の後にドメインを追加する．

```bash
server {
    ~省略~
    server_name  www.{契約したドメイン};
    ~省略~
}
```


これで `www.{契約したドメイン}` にアクセスしてNginxの初期ページが現れれば成功．

※[ドメインNavi](http://www.onamae.com/navi/domain.html)での設定から時間が経ってないと反映されない場合もあるので10分くらい待ってみるのが重要

[NginxをHTTP/2対応にした話](https://www.lapis-zero09.xyz/4th.html)
