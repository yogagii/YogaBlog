'''
@Author: your name
@Date: 2019-12-19 10:13:56
@LastEditTime: 2020-03-12 10:02:09
@LastEditors: Yoga
@Description: In User Settings Edit
@FilePath: /YogaBlog/pelicanconf.py
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Yoga'
SITENAME = 'Frontend Learning Book'
SITEURL = ''

PATH = 'content'
STATIC_PATHS = [u"img"]

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

THEME = 'pelican-themes/Responsive-Pelican'

# Blogroll
LINKS = (('Github', 'https://github.com/yogagii'),)

MENUITEMS = (('Javascript', 'category/javascript.html'),('React', 'category/react.html'),('IOS', 'category/ios.html'),('Data', 'category/data.html'),('Analytics', 'category/analytics.html'),('Programming', 'category/programming.html'),('Project', 'category/project.html'),('Backend', 'category/backend.html'))

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# math
PLUGIN_PATHS=['pelican-plugins']
# PLUGINS = ["render_math"]

## load cache
LOAD_CONTENT_CACHE = False

## typogrify
TYPOGRIFY = True

SUMMARY_MAX_LENGTH = 30

