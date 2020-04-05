Title: Swift入门
Date: 2020-03-12
Category: IOS
Tags: Swift
Author: Yoga

IOS, iPadOS, maxOS, iwatch

## class类：面向对象，动物类，引用类型reference type

传递时只是传递指针just passing pointers to it

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

## Object 面相对象

## Functional

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

## keywords关键字

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

week 弱引用（对象销毁时deinit）

## modifier修饰符

## optional chain可选链式调用

```swift
class ClassA {
  var name:String? //?可能有可能没有 nil &非nil
  var grade:String! //!初始化时一定要有值
  var nameA: String = "123" //默认值
}
```
