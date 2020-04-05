Title: 移动端事件
Date: 2020-01-20 16:32
Category: Javascript
Tags: event
Author: Yoga

## 移动端三大事件    
1、手指按下     ontouchstart

2、手指触摸     ontouchmove  
   
3、手指抬起     ontouchend

它们的执行顺序是ontouchstart > ontouchend > onclick

处理ios键盘弹出按钮点击click失效

1. 用ontouchstart绑定事件即可

```javascript
onTouchEnd = e => {
  e.preventDefault();
  handleSelectAll(e);
}
```

用onTouchStart时会有警告：Unable to preventDefault inside passive event listener due to target being treated as passive.

2. 在IOS下，点击页面中的input时，弹出软键盘时，如果input比较靠下，整个页面会上移，document.body.scrollOffset会由0变成大于0。 软键盘消失后，页面会下移。但是document.body.scrollOffset并不会变成0，所以这时候触控不准；

```javascript
$('textarea,input').on('blur', function (event) {
  document.body.scrollTop = 0;
});
```