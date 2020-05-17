Title: Swift Programming Language More
Date: 2020-05-03
Category: IOS
Tags: Swift
Author: Yoga

# Access Control 访问控制

访问控制可以限定你在源文件或模块中访问代码的级别。这个特性可以让我们隐藏功能实现的一些细节，并且可以明确的指定我们提供给其他人的接口中哪些部分是他们可以使用的，哪些是他们看不到的。

## 访问级别

* public (公开, 供外部调用): (for frameworks only) can be used by objects outside my framework

* internal (默认, 限module内使用): usable by any object in my app or framework

* private (私有, 限source file内使用): only callable from within this object

* private(set): this property is readable outside this object, but not settable

* fileprivate: accessible by any code in this source file

* open: (for frameworks only) public and objects outside my framework can subclass this

一个public访问级别的变量，不能将它的类型定义为internal和private的类型。因为变量可以被任何人访问，但是定义它的类型不可以，这样就会出现错误。函数的访问级别不能高于它的参数、返回类型的访问级别。因为如果函数定义为public而参数或者返回类型定义为internal或private，就会出现函数可以被任何人访问，但是它的参数和返回类型不可以，同样会出现错误。


类的访问级别也可以影响到类成员（属性、函数、初始化方法等）的默认访问级别。如果你将类申明为private类，那么该类的所有成员的默认访问级别也会成为private。如果你将类申明为public或者internal类，那么该类的所有成员的访问级别是internal。

A good strategy is to just mark everything private by default. Then remove the private designation when that API is ready to be used by other code.

</br>

# Assertion 断言

An assertion is just a function that you call where you assert something to be true. And if it's not your program crashes and print out an error.

通过assert实现断言，assert可以帮助开发者比较容易的发现和定位错误。一个断言断定条件是true，通过声明一个断言来确保某个必要的条件是满足的，以便继续执行接下来的代码。如果条件满足了，那么代码像往常一样执行，如果不满足了，代码就停止执行了，应用也随之停下来了。

```swift
//第一个参数为判断条件，第二个参数为条件"不满足"时的打印信息。
assert(cards.indices.contains(index), "Concentration.chooseCard(at: \(index)): chosen index not in the cards")
//如果断言被触发(index<0或index>cards.count)，将会强制结束程序，并打印相关信息：
assertion failed: Concentration.chooseCard(at: -1): chosen index not in the cards: file /Users/mac/Desktop/test/test/ViewController.swift, line 17
```
</br>

# Extensions 扩展

Extending existing data structures: you can add methods/properties to a class/struct/enum (even if you don't have the source)

swift可以为特定的class, strut, enum或者protocol添加新的特性。当你没有权限对源代码进行改造的时候，此时可以通过extension来对类型进行扩展。

* 添加计算属性 - computed properties
* 添加方法 - methods
* 添加初始化方法 - initializers
* 添加附属脚本 - subscripts
* 添加并使用嵌套类型 - nested types
* 遵循并实现某一协议 - conform protocol

extension可以为类型添加新的特性，但是它不能覆盖已有的特性。extension可以添加计算属性，但是不能添加存储属性，也不能为当前属性添加观察者。

链接：https://www.jianshu.com/p/783df05a9b59

> Do not abused! The only method and functions you wanna add to string or methods that make string a better class, not make it knows about Concentration.

给Int添加随机数方法
```swift
extension Int {
  var arc4random: Int {
    if self > 0 {
      return Int(arc4random_uniform(UInt32(self)))
    } else if self < 0 {
      return -Int(arc4random_uniform(UInt32(abs(self))))
    } else {
      return 0
    }
  }
}

let randomIndex = 5.arc4random // 0 1 2 3 4
let randomIndex = emojiChoices.count.arc4random
```
