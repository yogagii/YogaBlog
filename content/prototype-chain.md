Title: 原型链
Date: 2019-01-01
Category: Javascript
Tags: Javascript
Author: Yoga

原型链：JS万物皆对象，对象都有_proto_属性，_proto_连起来的链条，最终为null。

## 创建对象

1. 工厂模式

```js
function createPerson(name) {
  var o = new Object();
  o.name = name;
  return o;
}
var person1 = createPerson('Yoga');
person1.constructor == Object // yes
person1 instanceof Object // yes
```

2. 构造函数模式

```js
function Person(name) { // Person首字母大写
  this.name = name;
  this.sayName = function() { // 每次调用都要重新创建
    alert(this.name)
  }
}
```

3. 原型模式

```js
Person.prototype.age = 20;
Person.prototype.sayName = function() {
  alert(this.name)
}
var person2 = new Person("Tom");
person2.constructor === Person // yes
person2 instanceof Person // yes
person2 instanceof Object // yes
```

A instanceof B 检测A是否是B new出来的实例

A的原型链上是否存在B的原型

## 返回实例属性

查找对象属性时，先查找对象本身是否存在该属性，如果不存在会在原型链上找

1. Object.keys 可枚举，自身属性
2. for-in 所有可枚举属性，包括原型链

```js
for (var key in student1) {
  if (obj.hasOwnProperty(key)) {
    // 判断是否是自身属性
  }
}
```

3. Object.getOwnPropertyName 自身可/不可枚举属性