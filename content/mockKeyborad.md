Title: Button模拟键盘事件
Date: 2020-04-17
Category: Javascript
Tags:
Author: Yoga

### 尝试方法一：

Tableau文档提供的接口

困难：没有找到用于保存尚未创建的workbook的接口，目前已尝试过saveAsync和rememberCustomViewAsync都不行
 
### 尝试方法二：

前端模拟tableau保存的流程，点击我们的按钮时，请求五六个tableau的接口，根据返回的数据照着做一个保存的窗口，例如:

https://prodbitabcrp.jnj.com/vizportal/api/web/v1/getDestinationProjects

困难：跨域问题，无法直接调用tableau的接口

### 尝试方法三：

前端做个按钮，点击后向后端发送workbook信息，让后端调用tableau的接口完成保存

困难：wenyu说后端保存workbook会使发布人从用户变为某个admin账号
 
### 尝试方法四：

模拟ctrl+s —— execCommand('SaveAs')

困难：不兼容，在我的mac和Rick的windows（IE11）上都没有成功

各浏览器对SaveAs支持：

| sCommand | IE6 |  IE7 | IE8 |  Firefox | Chrome | Safari | Opera
- | :-: | :-: | :-: | :-: | :-: | :-: | :-:
saveAs | Y | Y | Y | N | N | N | N |
 
### 尝试方法五：

模拟ctrl+s —— 创建点击事件

1. jQuery.Event("keydown");
```js
var e = jQuery.Event("keydown");
$("button").click(function(){
  e.keyCode=83,e.metaKey=true;
	$(window).trigger(e);
}
$(window).keydown(function(e){
  if(e.keyCode==83&&e.metaKey){
    document.execCommand("saveAs");
    e.preventDefault();
    alert("按下了ctrl+S`````");
  }
});
```
2. createEvent('KeyboardEvent')
```js
var ev=document.createEvent('KeyboardEvent')
ev.initKeyboardEvent("keydown",true,true,window,83,0,false,false,false,true);
document.dispatchEvent(a);
```
3. createEventObject()
```js
var eventObj = document.createEventObject()
if (eventObj.initEvent) {
  eventObj.initEvent('keydown', true, true)
}

eventObj.keyCode = keyCode
eventObj.which = keyCode
el.dispatchEvent ? el.dispatchEvent(eventObj) : el.fireEvent('onkeydown', eventObj)
```

困难：试了三种都失败了，首先是初始化的时候keycode赋值无效，即使用Object.defineProperty强行修改keycode，也无法触发原生事件，因为isTrusted值为false，参考下文：https://www.jianshu.com/p/3ca5075229d4

* 事件生成的用户代理,作为用户交互的结果,或直接导致修改DOM,可信的用户代理与特权,不提供事件生成的脚本通过createEvent()方法,使用initEvent修改()方法,或通过dispatchEvent派遣()方法。可信事件的isTrusted属性值为true，而不可信事件的isTrusted属性值为false。

* 除了click事件外，大多数不受信任的事件不会触发默认操作。这个事件总是触发默认动作，即使isTrusted属性为false(此行为为向后兼容保留)。所有其他不受信任的事件的行为就好像对该事件调用了preventDefault()方法一样。