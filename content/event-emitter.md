Title: 高阶函数
Date: 2019-01-01
Category: Javascript
Tags: nodeJS
Author: Yoga

EventEmitter是Node.js的内置模块events提供的一个类，它是Node事件流的核心

https://www.runoob.com/nodejs/nodejs-event.html

https://nodejs.org/api/events.html#class-eventemitter

要实现的API有：
* on(event, listener)：为指定事件注册一个监听器，接受一个字符串 event 和一个回调函数。
* off(event)： 移除指定事件的某个监听回调
* trigger(event, args)： 按监听器的顺序执行每个监听器

```js
function EventEmitter() {
  this.listeners = {};
}

EventEmitter.prototype.on = function (event, cb) {
  var listeners = this.listeners;
  if (listeners[event] instanceof Array) {
    if (listeners[event].indexOf(cb) === -1) {
      listeners[event].push(cb);
    }
  } else {
    listeners[event] = [].concat(cb);
  }
}

EventEmitter.prototype.trigger = function (event, ...arguments) {
  if (this.listeners[event]) {
    this.listeners[event].forEach(cb => {
      cb.apply(null, arguments);
    });
  } else {
    console.error(`Event ${event} not exist`);
  }
}

EventEmitter.prototype.off = function (event, cb) {
  var listeners = this.listeners;
  var arr = listeners[event] || [];
  if (cb) {
    var i = arr.indexOf(cb);
    if (i >= 0) {
      listeners[event].splice(i, 1);
    }
  } else {
    delete listeners[event];
  }
}

re
emitter.on('foo', function(e){
  console.log('listening foo event 2', e);
});
emitter.on('bar', function(e){
  console.log('listening bar event', e);
});
emitter.on('*', function(e){
  console.log('listening all events');
});

emitter.trigger('foo', {name : 'John'});
emitter.trigger('bar', {name : 'Sun'});
emitter.trigger('*', {name : 'Sun'});

emitter.off('foo');
emitter.trigger('foo', {name : 'Yoga'});
```