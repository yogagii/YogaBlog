Title: Swift Programming Language Basic
Date: 2020-05-03
Category: IOS
Tags: Swift
Author: Yoga

# Properties 属性

## 存储属性 stored propert

一个存储属性就是存储在特定类或结构体的实例里的一个常量或变量--变量存储属性（var），常量存储属性（let）

```swift
var foo: Double
```

## 延迟存储属性

是指当第一次被调用的时候才会计算其初始值的属性。在属性声明前使用lazy来标示一个延迟存储属性。必须将延迟存储属性声明成变量（使用var关键字），因为属性的值在实例构造完成之前可能无法得到。而常量属性在构造过程完成之前必须要有初始值，因此无法声明成延迟属性。

```swift
lazy var importer = DataImporter()
```

## 计算属性computed property

不直接存储值，而是提供一个 getter 来获取值，一个可选的 setter 来间接设置其他属性或变量的值

The value of a property can be computed rather than stored

```swift
var foo: Double {
  get {

  }
  set(newValue) { // defaults to newValue

  }
}
```

可以没有set，不设set时property变为read only

```swift
var numberOfPairsOfCards: Int {
  get {
    return (cardButtons.count+1) / 2
  }
}
// 没有set时可以省略get
var numberOfPairsOfCards: Int {
  return (cardButtons.count+1) / 2
}
```
</br>

# Dictionary 字典

> Dictionary is a generic type like array, but you specify the type both of the key and the value.

Dictionary是一种散列表，可以通过关键值（key）快速地访问其中的元素（value），key必须是符合Hashable协议的类型，而value可以是任何类型。创建空的Dictionary时，必须声明key和value的类型。

```swift
var emoji = Dictionary<Int,String>()
var emoji = [Int:String]()
```

Looking something up in the dictionary returns an optional.

</br>

# Tuple 元组

> Tuple is like a mini struct that has no methods or vars, just has values in it.

元组（tuples）把多个值组合成一个复合值。元组内的值可以是任意类型，并不要求是相同类型。

```swift
let x: (String, Int, Double) = ("hello", 5, 0.85)
let (word, number, value) = x // this names the tuple elements when accessing the tuple
print(word) // hello

// tuple elements can be named when the tuple is declared
let x: (word: String, number: Int, value: Double) = ("hello", 5, 0.85)
print(x.word) // hello
let (w, n, v) = x // rename
```

use tuples to return multiple values from a function or method

```swift
func getSize() -> (weight: Double, height: Double) { return (250, 80) }
let x = getSize()
print("weight is \(x.weight)") // weight is 250
```
</br>

# Enum枚举

Enums are value types, like struct值类型，传递时复制

## 枚举值

```swift
enum Movement:Int {
  case left = 0
  case right = 1
  case top = 2
  case bottom = 3
}
```
支持各种类型: Int, Float, String, Bool

## 嵌套枚举

```swift
enum Area {
  enum DongGuan {
    case NanCheng
    case DongCheng
  }
  
  enum GuangZhou {
    case TianHe
    case CheBei
  }
}
```

## 关联值

Each case can have associated value. 枚举的case可以传值

```swift
enum FastFoodMenu {
  case hamburger(numberOfPatties: Int) 
  case fries(size: FryOrderSize)
  case drink(String, ounce: Int)
  case cookie
}
enum FryOrderSize {
  case large
  case small
}

let food = FastFoodMenu.drink(brand: "Coke", ounce: 1)
let otherItem: FastFoodMenu = .cookie
let menuItem = FastFoodMenu.fries(size: .large)

// checking an enum's state
switch food {
case .drink(let brand,let ounce):
  print("a \(ounce) of \(brand)")
  break
case .hamburger(let numberOfPatties):
  print("numberOfPatties:\(numberOfPatties)")
default:
  ()
}
```
Enum类似Struct，可以添加方法和属性

可以添加计算属性，但是不能添加存储属性

```swift
enum FastFoodMenu {
  case hamburger
  case drink

  func isIncludedInSpecialOrder(number: Int) -> Bool {
    switch self {
      case .hamburger(let pattyCount): return pattyCount == number
      case .fries, .cookie: return true
      case .drink(_, let ounces): return ounces == 16
    }
  }
  var calories: Int {
    // 计算属性，calculate and return caloric value
  }
}
```
突变方法 mutating method
```swift
enum FastFoodMenu {
  ...
  mutating func switchToBeingACookie() {
    self = .cookie
  }
}
```

</br>

# Optional 可选类型

```swift
class ClassA {
  var name:String? //?可能有可能没有 nil &非nil
  var grade:String! //!初始化时一定要有值
  var nameA: String = "123" //默认值
}
```

> An optional is just an enum

```swift
enum Optional<T> {
  case none
  case some<T>
}
var hello: String? // var hello: Optional<String> = .none
var hello: String? = "hello" // var hello: Optional<String> = .some("hello")
var hello: String? = nil // var hello: Optional<String> = .none
```

可选值类型就是一个盒子，这个盒子有两种情况，一种是填充了值，一种是为空，没有填充任何值。当它没有填充值的时候，我们称之为nil。这个可选值变量对有值或无值进行了打包（wrap）操作。

返回值为optional的函数：
* index
* dictionary
* ...

## Unwarpping optionals 解包

```swift
// 法一 Force unwrapping 强制解包
var authorName: String? = "Matt Galloway"
var unwrappedAuthorName = authorName! // 空值会报错
print("Author is \(unwrappedAuthorName)")

// 法二 检查不为空值时解包
if emoji[card.identifier] != nil {
  return emoji[card.identifier]!
} else {
  return "?"
}

// 运算符
return emoji[card.identifier] ?? "foo"

// optional chain 可选链式调用
let x: String? = ...
let y = x?.foo()?.bar?.z

// 法三 Optional binding 可选值绑定
if let chosenEmoji = emoji[card.identifier] {
  return chosenEmoji
}

// 法四 guard关键字 guard + 条件 + else + 代码块: 先排除
guard let sides = calculateNumberOfSides(shape: shape) else {
  print("I don't know the number of sides for \(shape).")
  return
}
```