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
LINKS = (('Github', 'https://github.com/yogagii'),('UI/UX/Frontend/Game Design', 'https://preview-static.clewm.net/cli/view-doc/view.html?url=//alicliimg.clewm.net/148/295/3295148/1537082834907429de68ef592b2817b37bcae93e547761537082781.pdf&t=1615824412&_=1615824412000&web_url=&shareName=&free=1&collect=0&from=active&filename=%E4%BD%9C%E5%93%81%E9%9B%86-%E5%89%8D%E7%AB%AF.pdf'),('Industrial Design Portfolio', 'https://preview-static.clewm.net/cli/view-doc/view.html?url=//alicliimg.clewm.net/148/295/3295148/1537389637354fb1ef05e2c2e77035e81f861378884fd1537389631.pdf&t=1615824215&_=1615824215000&web_url=&shareName=%E4%BD%9C%E5%93%81%E9%9B%86-%E4%BA%A7%E5%93%81&free=1&collect=0&from=active&filename=%E4%BD%9C%E5%93%81%E9%9B%86-%E4%BA%A7%E5%93%81.pdf'))

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

