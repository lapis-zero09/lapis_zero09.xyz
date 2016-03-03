Title: さくらVPSにNginx1.9系をインストールした話
Date: 2016-03-03 22:00
Category: さくらVPS
Tags: さくらVPS, Nginx
Slug: second
Author: lapis_zero09
Summary:さくらVPSに最新のNginxをインストールした時のHowto．

# さくらVSP

## さくらVPSの状態

  - [ここ](http://qiita.com/lapis_zero09/items/a77db6bbeb5fa83742a6)か[ここ](https://www.lapis-zero09.xyz/first.html)の初期設定が終わってる状態．
  - OSは標準のCentOS 6.7

さくらVPSにインストールされているOSを確認するコマンドは  

```bash
$ cat /etc/redhat-release
CentOS release 6.7 (Final)
```

## Nginxのビルド
(ここは読み飛ばしても大丈夫)  
早速，Nginxをビルドしていく．  
以下はさくらVPSにSSH接続している前提．  
yumでできるかなと思って

```bash
$ yum info nginx
```

してみるもVersion古すぎてうっそだろお前状態．  
そこで以下のコマンドでリポジトリを追加．  

```bash
$ sudo rpm -ivh http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm
```

これでokかなと思いきや．  

```bash
$ sudo yum -y install nginx
$ nginx -v
nginx version: nginx/1.8.1
```

インストールされたのはNginx1.8系，  
欲しいのは1.9系なのでダメ．  
(1.8系でもいい人はok)  

## Nginxをソースからビルド・インストール
先ほどの章で`yum -y install nginx`した人は，
`yum remove nginx`する  

まず，なんでもいいので作業用ディレクトリを作っておく．  

```bash
$ mkdir ~/hoge
$ cd ~/hoge
```

### ソースのダウンロード
作ったディレクトリの中に必要な最新版のソースをダウンロードしてくる．
必要なソースのホームページはこちら

  - nginx-1.9系 http://nginx.org/en/download.html
  - openssl-1.0.2系 https://www.openssl.org/source/
  - pcre-8.3系 http://ftp.csx.cam.ac.uk/pub/software/programming/pcre/
  - zlib-1.2系 http://zlib.net/

現時点(2016-03-03)での最新は以下

  - nginx-1.9.12
  - openssl-1.0.2g
  - pcre-8.38
  - zlib-1.2.8
(筆者はwgetだけど他の方法でもok)  

```bash
$ wget http://nginx.org/download/nginx-1.9.12.tar.gz
$ wget https://www.openssl.org/source/openssl-1.0.2g.tar.gz
$ wget http://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.38.tar.gz
$ wget http://zlib.net/zlib-1.2.8.tar.gz
```

※なんかうめこまれてたら怖いのでちゃんとMD5，SHASUM等，ハッシュ値を照合する．

### ソースの展開
照合できたら展開．  
以下の4コマンドをやってもいいけど，  

```bash
$ tar zxvf nginx-1.9.12.tar.gz
$ tar zxvf openssl-1.0.2g.tar.gz
$ tar zxvf pcre-8.38.tar.gz
$ tar zxvf zlib-1.2.8.tar.gz
```

シェルに頼って以下で一気にやったほうが効率的．  

```bash
$ find ./ -type f -name "*.tar.gz" -exec tar zxf {} \;
```

一応，確認しとく．

```bash
$ ls
nginx-1.9.12         openssl-1.0.2g.tar.gz
nginx-1.9.12.tar.gz  pcre-8.38              zlib-1.2.8.tar.gz    zlib-1.2.8
openssl-1.0.2g       pcre-8.38.tar.gz
```

ok．

### ソースのビルド・インストール
確認できたのでNginxのソース中でビルド・インストールする．  
インストールパスは /usr/local/nginx 以下．  

```bash
$ cd nginx-1.9.12
$ ./configure --with-openssl=../openssl-1.0.2g/ --with-http_ssl_module --with-pcre=../pcre-8.38 --with-zlib=../zlib-1.2.8  --with-http_v2_module --with-debug
$ make
$ sudo make install
```

エラーが出たら `configure` の引数のそれぞれの名前が一致しているかとか確かめる．  

これで一応終了．  

確認する．  

```bash
$ sudo /usr/local/nginx/sbin/nginx -v
nginx version: nginx/1.9.12
```

ok．  

起動して確認してみる．  

```bash
$ sudo /usr/local/nginx/sbin/nginx
$ tail /usr/local/nginx/logs/error.log
2016/03/02 17:18:03 [notice] 3008#0: signal process started
```

ok．
もろもろの設定は
`/usr/local/nginx/conf/nginx.conf` をいじる．  
自分のPCのブラウザから契約しているさくらVPSのIPアドレスにアクセス(URL欄にIPアドレスを入れる)してNginxの初期ページが見れたら成功．  

## Nginxのパスを通す
無事インストールできたけど，
起動したり止めたりリロードする際に
いちいち `sudo /usr/local/nginx/sbin/nginx`
って打つのはcoolじゃないのでパスを通しておく．

```bash
$ sudo vim ~/.bash_profile
```

以下を記載．  

```bash
export PATH=/usr/local/nginx/sbin:$PATH
```

書けたら `bash_profile` のリロード

```bash
$ source ~/.bash_profile
```

これで出来るはず．

`nginx` コマンドは動くようになったけど，  
`sudo` 実行したらコマンドが見つかりませんって怒られた人は，
`visudo` を以下のようにいじる．

```bash
$ sudo nginx -v
sudo: nginx: コマンドが見つかりません
```

```bash
$ sudo visudo
```

```bash
# Defaults   env_keep += "HOME"
Defaults    secure_path = /sbin:/bin:/usr/sbin:/usr/bin
↓
Defaults   env_keep += "HOME"
# Defaults    secure_path = /sbin:/bin:/usr/sbin:/usr/bin
```

これで `sudo nginx` やりたい放題．  

```bash
$ sudo nginx -v
nginx version: nginx/1.9.12
```

## Nginxを自動起動するようにする
ソースビルド・インストールしたNginxはそのままだと `service` や `chkconfig` できないので出来るようにする．

`/etc/init.d` 以下に起動スクリプトを作成しデーモン化，
自動起動を可能にする．  

```bash
$ sudo vim /etc/init.d/nginx
```

以下を記載．  

```bash
#!/bin/bash

#chkconfig: 2345 80 30
#description: nginx
set -e
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin/:/usr/sbin:/usr/bin
DESC="nginx deamon"
NAME=nginx
DAEMON=/usr/local/nginx/sbin/$NAME
SCRIPTNAME=/etc/init.d/$NAME

test -x $DAEMON || exit 0

d_start() {
        $DAEMON || echo -n " already running"
}

d_stop() {
        $DAEMON -s stop || echo -n " not running"
}

d_reload() {
        $DAEMON -s reload || echo -n " could not reload"
}

case "$1" in
        start)
                echo -n "Starting $DESC: $NAME"
                d_start
                echo "."
        ;;
        stop)
                echo -n "Stopping $DESC: $NAME"
                d_stop
                echo "."
        ;;
        reload)
                echo -n "Reloading $DESC configuration..."
                d_reload
                echo "reloaded."
        ;;
        restart)
                echo -n "Restarting $DESC: $NAME"
                d_stop
                sleep 2
                d_start
                echo "."
        ;;
        *)
                echo "Usage: $SCRIPTNAME {start|stop|restart|reload}" >&2
                exit 3
        ;;
esac

exit 0
```

できたらパーミッションを変更．  

```bash
$ sudo chmod +x /etc/init.d/nginx
$ ls -l /etc/init.d/nginx
-rwxr-xr-x 1 root root 872  3月  3 18:55 2016 /etc/init.d/nginx
```

ok．  
`chkconfig` に `nginx` を追加.  

```bash
$ sudo chkconfig --add nginx
$ chkconfig --list nginx
nginx          	0:off	1:off	2:on	3:on	4:on	5:on	6:off
```

これで自動起動するようになった．





後は `/usr/local/nginx/conf/nginx.conf` を好きなようにいじる．

[さくらVPSにお名前.comで契約したドメインを関連付けた話](https://www.lapis-zero09.xyz/third.html)
[NginxをHTTP/2対応にした話](https://www.lapis-zero09.xyz/forth.html)

追記：公式あるっぽい http://nginx.org/packages/mainline/centos/6/x86_64/RPMS/
