Title: jupyter notebookのカラースキームについて
Date: 2016-03-23 22:00
Category: jupyter_notebook
Tags: python, ipython4.x, css, jupyter, ipython
Slug: eighth
Author: lapis_zero09
Summary: jupyter notebook(ipython4.x)のcustom.cssを作る時のHowto．

# ipython4.x以降のcustom.cssの作り方が変わった．

## ipython3.xまで

```
!ipython profile create custom_css
```

で作れる．  

※このやり方で作ったcssは一応ipython4.xxでも動くっぽい？(要検証)
4.x以降はipythonコマンドではなくてjupyterコマンドが推奨されている？ので  
そっちでやるようにする．

## ipython4.x以降

```
confdir = !jupyter --config-dir
confdir = confdir[0]
confdir
```


```
import os
cssprofdir = os.path.realpath(os.path.join(
            confdir, 'css_profile'))
cssdir = os.path.join(cssprofdir, 'custom')
csspath = os.path.join(cssdir, 'custom.css')
os.makedirs(cssdir)
```

```
%%writefile {csspath}
~css内容~
```

```


from sys import platform
if platform == 'win32':
    print('set JUPYTER_CONFIG_DIR="{0}"'.format(cssprofdir))
    print('jupyter notebook')
else:
    print('JUPYTER_CONFIG_DIR="{0}" jupyter notebook'.format(cssprofdir))
```


```
!cp {csspath} custom.css
```


後日．好きなcss作ってまとめる．  

以上．  

(メモ)
```
JUPYTER_CONFIG_DIR="~/.jupyter/css_profile" jupyter notebook
```
