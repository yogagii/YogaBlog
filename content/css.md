Title: CSS
Date: 2019-01-01
Category: Frontend
Tags: CSS
Author: Yoga

## Position

* static: 默认值，忽略TRBL, z-index
* inherit: 继承
* fixed: 固定定位，相对于浏览器窗口TRBL
* relative: 相对定位，相对于正常位置TRBL

遵循正常文档流，占有文档空间，父级padding影响，根为root

TRBL | 父级 | 定位 |
| - | - | -
无 | 无 | 上一元素底部/浏览器左上角
无 | 有 | 父级左上角
有 | 父级有无position | 父级左上角
有 | 父级有padding | 内容区域左上角

* absolute: 绝对定位，相对于除static以外第一个父元素TRBL

脱离文档流，不占文档空间，父级padding不影响，根为html

TRBL | 父级 | 定位
| - | - | -
无 |  | 默认auto, 变回relative
有 | 父级无position | 找上级直到html
有 | 父级有position | 父级左上角，无论padding

## Display

display: inherit, none, block, inline, inline-block,table, table-cell

元素 | 宽高 | margin | padding | 换行排列 | example
| - | - | - | - | - | -
块状元素 | y | y | y | y (从上至下) | div, p, nav, ul, li , header, footer, aside
行内块状元素 | y | y | y | n (从左到右) |
行内元素 | n | 左右 | y | n (从左到右) | span, a, b, i, strong, em, img, input, select

* inline-block

行内块状元素div之间产生空白间隙的原因是，元素被当成行内元素排版的时候，元素之间的空白符（空格、回车换行等）都会被浏览器处理，根据white-space的处理方式（默认是normal，合并多余空白），原来HTML代码中的回车换行被转成一个空白符，所以元素之间就出现了空隙。

1. 将上一个元素的闭合标签与下一个元素的开始标签写在同一行; 或者将两个inline-block元素间加上空白注释；或者不写元素的闭合标签
```html
<ul>
  <li>one</li  
  ><li>two</li  
  ><li>three</li>
</ul>
<!-- or -->
<ul>
    <li>one</li><!--  
    --><li>two</li><!--  
    --><li>three</li>
</ul>
```
2. 父元素设置font-size为0
```css
.parent {
  font-size: 0;
}
```
3. 设置字符间距或单词间距
```css
/* letter-spacing */
.parent{
  letter-spacing: -0.5em;
}
``` 
4. 设置margin-right为负值

* None: 不存在且不加载

Visibility: hidden 隐藏，仍占据空间

* flex
```css
.parent {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

* table
```css
.parent {
  display: table;
}
.son {
  display: table-cell;
  vertical-align: middle;
  text-align: center;
}
```

// 水平居中
```css
.son {
  width: xxpx;
  margin: 0 auto;
}
```

// 水平垂直居中
```css
.parent {
  position: relative;
}
.son {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```

## 盒子模型 Box Model

CSS盒模型本质上是一个盒子，封装周围的HTML元素，它包括：外边距（margin）、边框（border）、内边距（padding）、实际内容（content）四个属性。

两个上下相邻的盒子垂直相遇时，外边距会合并，等于较大的那个

* W3C标准盒：

box-sizing: content-box

总宽度 = margin + border + paddig + width(content)

* IE盒

box-sizing: border-box

总宽度 = margin + width(border + padding + content)

```css
// 向下三角
.triangle {
  width: 0;
  height: 0;
  border: 100px solid transparent;
  border-top: 100px solid blue;
}
```

## 滚动条样式

webkit内核的浏览器（谷歌、ie、Safari等）

使用伪类改变滚动条样式

1. ::-webkit-scrollbar 滚动条整体

2. ::-webkit-scrollbar-thumb 滚动条的方块

3. ::-webkit-scrollbar-track 滚动条的轨道

4. ::-webkit-scrollbar-button 滚动条的两端按钮

5. ::-webkit-scrollbar-track-piece 内层轨道，滚动条中间部分

6. ::-webkit-scrollbar-corner 边角，即垂直滚动条和水平滚动条相交的地方

https://blog.csdn.net/qq_35355153/article/details/107205254

```css
ul {
  &::-webkit-scrollbar {
      width: 5px;
  }
  &::-webkit-scrollbar-thumb {
    background: @primary-color;
    border-radius: 5px;
  }
}
```

火狐滚动条不能修改样式