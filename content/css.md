Title: CSS
Date: 2021-08-18
Category: Javascript
Tags: CSS
Author: Yoga

## Position

* static: 默认值，忽略TRBL, z-index
* inherit: 继承
* fixed: 固定定位，相对于浏览器窗口TRBL
* relative: 相对定位，相对于正常位置TRBL

遵循正常文档流，占有文档空间，父级padding影响，根为root

TRBL | 父级 | 定位
- | - | -
无 | 无 | 上一元素底部/浏览器左上角
无 | 有 | 父级左上角
有 | 父级有无position | 父级左上角
有 | 父级有padding | 内容区域左上角

* absolute: 绝对定位，相对于除static以外第一个父元素TRBL

脱离文档流，不占文档空间，父级padding不影响，根为html

TRBL | 父级 | 定位
- | - | -
无 |  | 默认auto, 变回relative
有 | 父级无position | 找上级直到html
有 | 父级有position | 父级左上角，无论padding