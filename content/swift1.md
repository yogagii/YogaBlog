Title: Swift Data Structures
Date: 2020-03-12
Category: IOS
Tags: Swift
Author: Yoga

IOS, iPadOS, maxOS, iwatch

# Data Structures

## class类：面向对象，动物类，引用类型reference type

> Examples: ViewController, UIButton, Concentration

传递时只是传递指针just passing pointers to it

When does it get cleaned up out of the heap?

java--garbage collection 垃圾收集(track->mark->clean)

swift--reference counting 引用计数(instantly removes it as soon as no one point to it)

init在堆内存Heap里引用计数+1,deinit计数-1，容量大，速度慢，计数到0被清理

```swift
class Car {
  var name: String?
  init(name: string) {
    self.name = name
  }
}

let tesla = Car(name: "Tesla") //Heat堆 tesla -> Car(name: "Tesla")

let teslaB = tesla

tesla.name = "A"
```

Class默认初始化方法: swift只会提供一个默认的空初始化方法。

## struct结构体：值类型value type，没有继承

传递时复制：copy-on-write只有修改时复制

在栈内存Stack创建，先进后出，进a->进b->a+b->出b->出a

栈内存的在function结束就销毁，堆内存的在deinit才销毁

```swift
struct Dog {
  var name: String?
  init(name: String) {
    self.name = name
  }
}
let dogA = Dog(name: "huahua") // error! 相当于js const，不能改属性
var dogA = Dog(name: "huahua") // 相当于js let

let dogB = DogA

dogA.name = "caocao"

print dogB.name
```

Struct默认初始化方法：1、空初始化方法；2、成员初始化方法

```swift
struct Person{
    var name = "tom"
    var age = 1
    
}

let person = Person()//空初始化方法
print("person:name=\(person.name),age=\(person.age)")

let person1 = Person(name:"JIM",age:3)//成员初始化方法
print("person:name=\(person1.name),age=\(person1.age)")
```

## enum枚举

```swift
enum ADC {
  case digital
  case edg
  case sap
}

enum ADC: String {
  case digital = "digital"
  case edg = "edg"
  case sap = "sap"
}

let digital = ADC.digital
```

## Protocal协议

```swift
protocal Car {
  var name: String { get }
  var isElectric: Bool { get }
}
protocal Car {
  var maxSpeed: Double { get }
  func charging(dianya: Int) -> Double
}

//遵循协议的结构体一定要实现协议的属性
struct Tesla: Car, ElectricDrive {
  func charging(dianya: Int) -> Double {
    return Double(dianya) / 100.0
  }
  var name: String
  var maxSpeed: Double
  init(name: String, maxSpeed: Double) {
    self.name = name
    self.maxSpeed = maxSpeed
  }
}

//扩展
extension Car where Self: ElectricDrive {
  var isElectric：Bool { return true }
}

let tesla = Tesla(name: "tesla", maxSpeed: 200.0)
print(tesla.isElectric) //true
```
</br>

# keywords 关键字

inout

```swift
var arrA = ["1","2","3"];
func arrRemoveFirst(arr: inout [String]) -> [string] {
  return [arr.remove(at: 0)]
}
```
public

func

let

var +1 -1(0时deinit)

## strong 强引用(default)

normal reference counting

当一个对象被声明为strong时，就表示父层级对该对象有一个强引用的指向。此时该对象的引用计数会增加1。

## weak 弱引用

对象销毁时deinit，弱引用对象的引用计数不会+1

当对象被声明为weak时，父层级对此对象没有指向，该对象的引用计数不会增加1。它在对象释放后弱引用也随即消失。继续访问该对象，程序会得到nil，不会崩溃。

A weak pointer will never keep an object in the heap. It gets set to nil if all the other strong points go away. It has to be an optional.

在声明弱引用对象是必须用var关键字, 不能用let.
因为弱引用变量在没有被强引用的条件下会变为nil, 而let常量在运行的时候不能被改变.

## unowned

对象在释放后，它指引的对象不会清零，依然有一个无效的引用指向对象，它不是Optional也不指向nil。如果继续访问该对象，程序就会崩溃。

当访问对象确定不可能被释放，则用unowned。比如self的引用。

The one time we use this is to avoid a memory cycle. We will use unowned with closures闭包.

