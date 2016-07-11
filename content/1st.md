Title: さくらVPSを契約した話
Date: 2016-03-02 22:00
Category: さくらVPS
Tags: さくらVPS, ssh, yum
Slug: 1st
Author: lapis_zero09
Summary:さくらVPSを契約した時のHowto．

# さくらVSP

さくらVPSの[512プラン](http://vps.sakura.ad.jp/specification/)を契約した．  
月額635円でとてもやすい．  
クレジットカードで登録すると2週間無料お試しができる．  
(初期費用で約2000円位持ってかれる．)  

## 初期設定
コントロールパネルで契約したサーバを起動した後，自分のPCのterminalでSSH接続．  
```bash
$ ssh root@{サーバのIPアドレス}
```
yum update をする  
```bash
$ yum update
```
すると，いきなりエラーを吐かれるので  
clean up してから update　する  
```bash
$ yum clean up
$ yum update
```
うまくいきました．  
時間がかかったので screen の中で回したほうがいいかも  

## 日本語化
一応，日本語化しておく．  
```bash
$ vim /etc/sysconfig/i18n
```
```bash
LANG="ja_JP.UTF-8"
SYSFONT="latarcyrheb-sun16"
```

## 作業用ユーザの登録
作業用ユーザの登録をする．  
```bash
$ useradd {新しいユーザの名前}
$ passwd {useraddしたユーザの名前}
```
作業用ユーザに sudo 権限を与える．  
(userをwheelグループに入れるように変更)  
```bash
$ usermod -G wheel {useraddしたユーザの名前}
```
wheelグループがsudoコマンドを使えるようにする．  
```bash
$ visudo
```
%wheel  ALL=(ALL)  ALLの行を以下のように変更  
```
# %wheel       ALL=(ALL)      ALL
↓
%wheel       ALL=(ALL)      ALL
```

## 鍵認証
### さくら側
.sshフォルダを作っておく  
```bash
$ mkdir ~/.ssh
$ chmod 700 ~/.ssh
```
### 自分のPC側
自分のPCで鍵作成．  
(パスフレーズなど聞かれるのでデフォルトのままでok)
筆者はSSH先ごとに鍵を変えてるので名前を変えた．  
```bash
$ ssh-keygen -t rsa
Enter file in which to save the key : id_rsa.sakura
Enter passphrase :
```

ちゃんとできてるか確認．  
```bash
$ ls -a ~/.ssh
id_rsa.sakura   id_rsa.sakura.pub
```
できてる．  
パーミッションを変えておく．  
```bash
$ chmod 600 id_rsa.sakura.pub
```
SSH接続の時にいちいちIPアドレスを書くのが面倒どうなので  
configに登録しておく．
```bash
$ cd ~/.ssh
$ vim config
```
```bash
Host sakura
  HostName {さくらのIPアドレス}
  User {useraddしたユーザの名前}
```
これで  
```bash
$ ssh sakura
```
でつなげるようになる．  

pubの方をさくらVPSに転送．  
転送時にauthorized_keysに名前変更．  
```bash
$ scp ~/.ssh/id_rsa.sakura.pub sakura:~/.ssh/authorized_keys
```
さくら側で確認．  
```bash
$ ls -a ~/.ssh
authorized_keys
```
ok．  

configに鍵を登録しておく．
```bash
$ vim ~/.ssh/config
```
```bash
Host sakura
  HostName {さくらのIPアドレス}
  User {useraddしたユーザの名前}
  IdentityFile ~/.ssh/id_rsa.sakura
```

## SSH設定
セキュリティを高めるために以下を実行．  
- ポート番号の変更
  - デフォルトの22から任意の番号に変更
  - 指定できる範囲は1024~65535
- パスワードログインの禁止
- rootログインの禁止

### さくら側
rootにスイッチ
```bash
$ sudo -s
```
SSH設定をいじっていく．  
SSHの設定は /etc/ssh/ssh_config
先にバックアップをとる．  
```bash
$ cp /etc/ssh/ssh_config /etc/ssh/ssh_config.org
```
```bash
$ vim /etc/ssh/ssh_config
```
以下の3つを変更．
```bash
#Port 22
↓
Port {任意の番号}

PasswordAuthentication yes
↓
PasswordAuthentication no

#PermitRootLogin yes
↓
PermitRootLogin no
```
変更を反映させる．  
```bash
$ service sshd restart
```


### 自分のPC
configにportを登録する．
```bash
$ vim ~/.ssh/config
```
```bash
Host sakura
  HostName {さくらのIPアドレス}
  User {useraddしたユーザの名前}
  Port {/etc/ssh/ssh_config.orgのPortで指定した番号}
  IdentityFile ~/.ssh/id_rsa.sakura
```

接続できたらok．  

## FireWall(iptables)の設定
/etc/sysconfig/iptablesをいじる．  
```bash
$ vim /etc/sysconfig/iptables
```
以下をコピペでも可．  
```bash
*filter
:INPUT     DROP    [0:0]
:FORWARD   DROP    [0:0]
:OUTPUT    ACCEPT  [0:0]
:SERVICES  -       [0:0]
-A INPUT -i lo -j ACCEPT
-A INPUT -p icmp --icmp-type echo-request -m limit 1/s --limit-burst4 -j ACCEPT
-A INPUT -p tcp -m state --state ESTABLISHED,RELATED -j ACCEPT
-A INPUT -p tcp -m state --state NEW -j SERVICES
-A INPUT -p udp --sport 53 -j ACCEPT
-A INPUT -p udp --sport 123 --dport 123 -j ACCEPT
-A SERVICES -p tcp --dport {/etc/ssh/ssh_config.orgのPortで指定した番号} -j ACCEPT
-A SERVICES -p tcp --dport 80 -j ACCEPT
-A SERVICES -p tcp --dport 443 -j ACCEPT
COMMIT
```
筆者はこんな感じ．  

設定を反映させる．
```bash
$ service iptables start
```
okが出たらok．  

設定を確認するためのコマンド
```bash
$ iptables -L
```



[Nginxをインストールした話](https://www.lapis-zero09.xyz/2nd.html)
