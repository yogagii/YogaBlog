Title: pelican blog搭建
Date: 2018-10-20 16:32
Category: Programming
Author: 张本轩

## Installation

1. `pip install pelican`
2. `pip install Markdown`
3. `pelican-quickstart` to build a quick start version project 
4. [Optional] `pip install typogrify`

## Usage

blog metadata

```
Title: My title
Date: 2010-12-03 10:20
Modified: 2010-12-05 19:30
Category: Python
Tags: pelican, publishing
Slug: my-post
Authors: Alexis Metaireau, Conan Doyle
Summary: Short version for index and feeds

This is the content of my blog post.
```

* make regenerate 
* make serve
* make devserve

## Reference

[pelican](http://docs.getpelican.com/en/stable/install.html)

[typogrify](https://pypi.org/project/typogrify/)

```bash
pip3 install pelican

echo $PATH
vim ~/.zshrc // .bash_profile
export PATH="/Users/yoga/Library/Python/3.8/bin:$PATH"
source ~/.zshrc // 使修改的环境变量生效
which pelican

pip3 install typogrify
pip3 install Markdown

make html
make serve
```