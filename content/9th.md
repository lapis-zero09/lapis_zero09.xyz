Title: git commit時のエラーについて
Date: 2016-03-28 22:00
Category: git
Tags: git
Slug: 9th
Author: lapis_zero09
Summary: git commitでエラーが出る時のHowto．

# git commit

今まではできてたのにある日から  
`git commit` をviでした時に以下のようなエラーが出る．

```
$ git commit -a
error: There was a problem with the editor 'vi'.
Please supply the message using either -m or -F option.
```

gitconfigを確認する．

```
$ cat ~/.gitconfig
```


[core]タグの中のeditorの設定を見る．  
vimのパスを確認．  

```
$ which vim
/usr/local/bin/vim
```

以下コマンドでエディタをvimに設定．  

```
$ git config --global core.editor /usr/local/bin/vim
```


gitconfigを確認して，  
[core]タグのeditorが変わっていればok．  



以上．
