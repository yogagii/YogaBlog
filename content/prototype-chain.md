Title: 原型链
Date: 2019-01-01
Category: Javascript
Tags: Javascript
Author: Yoga

原型链：JS万物皆对象，对象都有_proto _属性，_proto _连起来的链条，最终为null。

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

## prototype 和 _proto _

> prototype是函数才有的属性，_proto _是每个对象都有的属性

_proto _([[Prototype]])“构造器的原型”: _proto _ === constructor.prototype

```js
Person.prototype.constructor == Person
person2.constructor == Person
```

![prototype](img/prototype.png)

```js
person2: {
  name: "Tom",
  sayName: ƒ (),
  __proto__: Object
}
person2.__proto__: {
  age: 20,
  sayName: f(),
  __proto__: Object,
  constructor: f Person(name)
}
```

## 继承

```js
function Student() {
  this.school = 'SJTU';
}
Student.prototype = new Person('Yoga') // 继承，重写原型
Student.prototype.major = 'design' // 一定要写在继承之后 person2.major: undefined
var student1 = new Student();

student1: {
  school: 'SJTU',
  __proto__: Person
}
student1.__proto__: {
  major: 'design',
  name: 'Yoga',
  sayName: f(),
  __proto__: Object
}
student1.__proto__.__proto__: {
  age: 20,
  sayName: f(),
  constructor: f Person(name),
  __proto__: Object
}
```

## 返回实例属性

查找对象属性时，先查找对象本身是否存在该属性，如果不存在会在原型链上找

1. Object.keys 可枚举，自身属性
```js
Object.keys(person2) // ['name', 'sayName']
Object.keys(student1) // ['school']
```
2. for-in 所有可枚举属性，包括原型链

```js
for (var key in person2) {
  // ['name', 'sayName', 'age']
  if (Object.hasOwnProperty(key)) {
    // 判断是否是自身属性 'name'
  }
}
for (var key in student1) {
  // ['school', 'name', 'sayName', 'major', 'age']
  if (Object.hasOwnProperty(key)) {
    // 判断是否是自身属性 'name'
  }
}
```

3. Object.getOwnPropertyNames 自身可/不可枚举属性
```js
Object.getOwnPropertyNames(person2) // ['name', 'sayName']
Object.getOwnPropertyNames(student1) // ['school']
```

可枚举属性是指那些内部 “可枚举enumerable” 标志设置为 true 的属性。对于通过直接的赋值和属性初始化的属性，该标识值默认为即为 true。但是对于通过 Object.defineProperty 等定义的属性，该标识值默认为 false。