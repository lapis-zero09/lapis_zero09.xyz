#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'lapis_zero09'
SITENAME = '題未定'
SITEURL = 'https://www.lapis-zero09.xyz'
# SITEURL = 'http://localhost:8000'
TIMEZONE = 'Asia/Tokyo'
DEFAULT_LANG = 'ja'
PATH = 'content'

PROFILE_IMG_URL = './img/profile.jpg'
THEME = './pure-single/'


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('github', 'https://github.com/Shandy-ko'),
    ('twitter-square', 'https://twitter.com/lapis_zero09'),
    ('gift', 'http://www.amazon.co.jp/registry/wishlist/2TLPKVEIT5D9B'),
    ('search', 'http://qiita.com/lapis_zero09'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
