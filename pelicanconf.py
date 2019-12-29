'''
@Author: your name
@Date: 2019-12-19 10:13:56
@LastEditTime : 2019-12-29 22:15:44
@LastEditors  : Please set LastEditors
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

MENUITEMS = (('React', 'category/react.html'),('React-Admin', 'category/react-admin.html'),('Data', 'category/data.html'),('Analytics', 'category/analytics.html'),('Programming', 'category/programming.html'))

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

