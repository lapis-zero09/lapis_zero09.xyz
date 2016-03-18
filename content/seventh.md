Title: TeXshopのcolor schemeを変更したときの話
Date: 2016-03-18 22:00
Category: TeX
Tags: TeX, El_Capitan, TeXshop
Slug: seventh
Author: lapis_zero09
Summary: TeXshopのcolor schemeを変更した時のHowto．

# TeXshopのcolor schemeを変更する

デフォルトの白背景黒文字から変更する．  

指定したいcolorのRGB値を"255"で割って，  
その値を指定してやれば良い．  

例えば，backgroundならこんな感じ．  

```
# background = 39 40 34 (#272822)
defaults write TeXShop background_R 0.15
defaults write TeXShop background_G 0.16
defaults write TeXShop background_B 0.13
```

これをshファイルとして保存・実行してやれば，
設定が変わるはず．  
※TeXshopの再起動が必要．

monokai, safari_night, solarized dark lightの例を，  
[gist](https://gist.github.com/lapis-zero09/7f973b2d80d2486510f9)に記す．  



戻したい時は，以下を保存・実行．  

```
defaults write TeXShop background_R 1.0
defaults write TeXShop background_G 1.0
defaults write TeXShop background_B 1.0

defaults write TeXShop commandred 0.0
defaults write TeXShop commandgreen 0.0
defaults write TeXShop commandblue 1.0

defaults write TeXShop commentred 1.0
defaults write TeXShop commentgreen 0.0
defaults write TeXShop commentblue 0.0

defaults write TeXShop foreground_R 0.00
defaults write TeXShop foreground_G 0.00
defaults write TeXShop foreground_B 0.00

defaults write TeXShop indexred 1.00
defaults write TeXShop indexgreen 1.00
defaults write TeXShop indexblue 0.00

defaults write TeXShop insertionpoint_R 0.00
defaults write TeXShop insertionpoint_G 0.00
defaults write TeXShop insertionpoint_B 0.00

defaults write TeXShop markerred 0.02
defaults write TeXShop markergreen 0.51
defaults write TeXShop markerblue 0.13
```


以上．  



