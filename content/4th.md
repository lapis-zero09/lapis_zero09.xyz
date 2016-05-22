Title: NginxをHTTP/2対応にした話
Date: 2016-03-03 22:01
Category: Nginx
Tags: さくらVPS, Nginx, http2, tls, Let'sEncrypt
Slug: forth
Author: lapis_zero09
Summary:NginxをHTTP/2対応にした時のHowto．



# NginxをHTTP/2対応にした話

## 環境

  - [ここ](http://qiita.com/lapis_zero09/items/a77db6bbeb5fa83742a6)と[ここ](http://qiita.com/lapis_zero09/items/74b6ac261546dfee077e)の初期設定が終わってる状態．
  - CentOS 6.7
  - Nginx 1.9.12

## 現状のnginx.conf

```bash
~省略~
server {
  listen 80;
  server_name www.{自分の契約しているドメイン};
  location / {
    root   /var/www; #公開したいドキュメントのルート
    index  index.html;
  }
  ~省略~
}
~省略~
```

## TLSに対応させる
### 証明書を取得する
[Let's Encrypt](https://github.com/letsencrypt/letsencrypt)を使って無料で証明書を取得する．

ホームディレクトリで

```bash
$ cd /usr/local/
$ git clone https://github.com/letsencrypt/letsencrypt
$ cd letsencrypt
$ ./letsencrypt-auto --help
$ ./letsencrypt-auto certonly --webroot -d www.{自分の契約しているドメイン} --webroot-path {公開したいドキュメントのルートここでは/var/www}
```

するとEnter email addressという画面が表示されるので、メールアドレスを入力．
筆者はwhoisで登録されてるアドレスにしました．

<Agree> を選択．

うまくいくとこんな感じの表示が出る

```bash
IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at
   /etc/letsencrypt/live/itochan.jp/fullchain.pem. Your cert
   will expire on 2016-03-08. To obtain a new version of the
   certificate in the future, simply run Lets Encrypt again.
 - If like Lets Encrypt, please consider supporting our work by:

   Donating to ISRG / Lets Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le
```
### 証明書取得を自動化する
Let's encryptは証明書の期限が３ヶ月と短いので，自動更新する．

```bash
$ su -
$ crontab -e
```

以下を記載．

```bash
00 05 01 * * /usr/local/letsencrypt/letsencrypt-auto certonly --webroot -d www.{自分の契約しているドメイン} --webroot-path {公開したいドキュメントのルートここでは/var/www} --renew-by-default && nginx -s reload
```

### TLSに対応させる

`nginx.conf` をいじる．
http接続をhttps接続にリダイレクトさせる内容を  
`listen 80` の `server` タグ内に書く．  
`listen 443` の `server` タグのコメントを外してドキュメントルート等書く．  
Let's Encryptで取得した証明書は `/etc/letsencrypt/live/www.{自分の契約しているドメイン}/` 以下にあるのでそれを参照する旨を書く．

```bash
~省略~
server {
  listen 80;
  server_name www.{自分の契約しているドメイン};
  return 301 https://www.{自分の契約しているドメイン}$request_uri;
}

server {
        listen       443 ssl;
        server_name  www.{自分の契約しているドメイン};
        ~省略~
        ssl_certificate      /etc/letsencrypt/live/www.{自分の契約しているドメイン}/fullchain.pem;
       ssl_certificate_key  /etc/letsencrypt/live/www.{自分の契約しているドメイン}/privkey.pem;

        location / {
            root   /var/www;
            index  index.html;
        }
    }
~省略~
```

`nginx.conf` の文法チェック  

```bash
$  sudo nginx -t
```

okが出たらNginxをリロードする．  

```bash
$ sudo nginx -s reload
```

一応アクセスできるか確認．  
できたら[SSLLab](https://www.ssllabs.com/ssltest/index.html)のテストもやってみる．  
(BかCが出る)

### http2に対応させる

`nginx.conf` をいじる．

```bash
~省略~
server {
        listen       443 ssl http2;
        server_name  www.{自分の契約しているドメイン};
        ~省略~
        ssl_certificate      /etc/letsencrypt/live/www.{自分の契約しているドメイン}/fullchain.pem;
        ssl_certificate_key  /etc/letsencrypt/live/www.{自分の契約しているドメイン}/privkey.pem;

        ssl_ciphers  ECDHE+AESGCM:DHE+AESGCM:HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers  on;
        location / {
            root   /var/www;
            index  index.html;
        }
    }
~省略~
```

文法チェック，リロードの流れをもう一度．  

## SSLLabでA+をとる
HTTP/2がTLSに求める制限

 - TLSのバージョンは1.2以上
 - プロトコル選択にALPN(RFC7301)を使う
 - サーバ認証を共有できる接続は接続共有が可能
 - SNI(Server Name Indicator)拡張必須
 - SNI(Server Name Indicator)拡張必須
 - TLS Compression禁止
 - Renegotiation禁止
 - 鍵長 (DHE 2048bit以上、ECDHE 224bit以上)サポート必須 • PFS必須 (DHE,
ECDHE)
 - AEAD(GCM/CCM)以外の暗号方式をブラックリストとして利用禁止

そんなことはいいからやり方はよ

### DHEの鍵長増加
2048bitのDHパラメータファイルを生成．  
`nginx.conf` があるフォルダで以下を実行．  

```bash
$ openssl dhparam -out dhparam.pem 2048
$ openssl dhparam -text -in dhparam.pem  -noout
```

`nginx.conf` のsslサーバの部分にDHパラメータのファイルを加える．  
`nginx.conf` をいじる．

```bash
~省略~
server {
        listen       443 ssl http2;
        server_name  www.{自分の契約しているドメイン};
        ~省略~
        ssl_certificate      /etc/letsencrypt/live/www.{自分の契約しているドメイン}/fullchain.pem;
        ssl_certificate_key  /etc/letsencrypt/live/www.{自分の契約しているドメイン}/privkey.pem;
        ssl_dhparam          dhparam.pem;

        ssl_ciphers  ECDHE+AESGCM:DHE+AESGCM:HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers  on;
        location / {
            root   /var/www;
            index  index.html;
        }
    }
~省略~
```

文法チェック，リロードの流れをもう一度．  
[SSLLab](https://www.ssllabs.com/ssltest/index.html)のテストもやってみる．  
(AかA-が出る)

### HSTSヘッダ
`nginx.conf` のsslサーバの部分にHSTSヘッダを返すように以下の設定を追加．  
(max-ageは半年に設定)  

```bash
~省略~
server {
        listen       443 ssl http2;
        server_name  www.{自分の契約しているドメイン};
        add_header Strict-Transport-Security "max-age=15768000; includeSubdomains";

        ssl_certificate      /etc/letsencrypt/live/www.{自分の契約しているドメイン}/fullchain.pem;
        ssl_certificate_key  /etc/letsencrypt/live/www.{自分の契約しているドメイン}/privkey.pem;
        ssl_dhparam          dhparam.pem;
        ssl_session_cache    shared:SSL:1m;
        ssl_session_timeout  5m;

        ssl_ciphers  ECDHE+AESGCM:DHE+AESGCM:HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers  on;
        location / {
            root   /var/www;
            index  index.html;
        }
    }
~省略~
```

文法チェック，リロードの流れをもう一度．  
[SSLLab](https://www.ssllabs.com/ssltest/index.html)のテストもやってみる．  
(A+が出る(2016-03-03))
