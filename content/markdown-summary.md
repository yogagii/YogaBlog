Title: Markdown语法介绍
Date: 2018-10-14 21:14
Category: Programming
Tags: markdown
Author: 张本轩
Summary: 这篇文章介绍Markdown的语法，包括标题、引用、列表、代码、强调、链接、表格、分割线、图片

## Table of Contents

This is a markdown file This is a markdown fileThis is a markdown file This is a markdown file This is a markdown file This is a markdown file

* [标题](#标题)
* [引用](#引用)
* [列表](#列表)
* [代码](#代码)
* [强调](#强调)
* [链接](#链接)
* [表格](#表格)
* [分割线](#分割线)
* [图片](#图片)
* [Reference](#Reference)

### 标题

Markdown共支持六级标题:

```
    # 一级标题
    ## 二级标题
    ### 三级标题
    #### 四级标题
    ##### 五级标题
    ###### 六级标题
```

### 引用

通过在段落的第一行最前面加上*>*来使用引用:

> 这是一个引用
> > 这是二级引用

### 列表

列表项目一般放在最左边，项目标记后面要接一个空格

*无序列表*: 使用*, +或者-标记

+ 这是无序列表
- 这也是无序列表

*有序列表*: 使用数字接一个英文句话

1. 有序列表
2. 有序列表

### 代码

使用```来包裹代码块即可

```
这是一段代码
```

### 强调

这是*斜体*, 这是**加粗**

### 链接

```
[说明](链接url)
```

### 表格

First Header | Second Header | Third Header
------------ | ------------- | ------------
Content Cell | Content Cell  | Content Cell
Content Cell | Content Cell  | Content Cell

### 分割线

可以使用三个以上-符号制作分割线

```
ABA
---
BAB
```

### 图片

```
![Alt text](/path/img.jpg)
```

### Reference

[Markdown语法介绍](https://coding.net/help/doc/project/markdown.html)