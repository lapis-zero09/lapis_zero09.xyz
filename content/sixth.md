Title: TeXを入れたときの話
Date: 2016-03-15 22:00
Category: TeX 
Tags: TeX, El_Capitan
Slug: sixth
Author: lapis_zero09
Summary: TeXのPATHが勝手に通ってくれないので自分で通した時のHowto．

# El CapitanにTeXを入れる

Homebrew経由でもTeX本家からpkgを落としてきても，TeX関連のPATHが通らないのでやったこと
※本当なら勝手にPATH が通るはず?

## Ghostscriptのインストール

```
$ brew install ghostscript
```

## MacTeXのインストール

[MacTeX](https://tug.org/mactex/mactex-download.html)　から，MacTeX.pkgをダウンロード．
ファイルのダウンロードが始まらず，
"mactex-download..."のテキストが表示された場合，
"ftp://"で始まるURLをアドレスフィールドに直接コピペ．

"インストールの種類"で"カスタマイズ"をクリック．
"カスタムインストール"でGhostscriptのチェックを外して
インストールをクリック．


## PATHを通してやる

`zshrc` か `bashrc` に以下を記載．

```
export PATH="/usr/local/texlive/2015/bin/x86_64-darwin/":$PATH
```


`zshrc` か `bashrc` 書いた方をリロード．

```
$ source ~/.zshrc
```

## TeX Liveのアップデート

```
$ sudo tlmgr update --self --all
```



以上．
