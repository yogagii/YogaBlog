Title: Weibo demo
Date: 2020-04-09
Category: IOS
Tags: Swift
Author: Yoga

open.weibo.com/wiki

SwiftUI 是一个优秀的用户界面框架

|         UIKit          | SwiftUI |
| :--------------------: | :-----: |
|        UILabel         |  Text   |
| UIStackView 垂直排列时 | VStack  |
| UIStackView 水平排列时 | HStack  |
|        UIButton        | Button  |

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        Text("Hello, World!")
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
```

ContentView 遵循 View 协议，在 SwiftUI 中想要显示任何的视图，都需要遵循 View，通过通过 body 属性来返回视图

body 返回类型 some View。some 是 swift5.1 新增加的一种返回类型，返回 some View 意味着 body 属性将要返回一个遵循 View 协议的视图，必须返回一个子视图

> 只有函数体中是单独表达式，才会自动添加 return

```swift
// Error
// Function declares an opaque return type, but has no return statements in its body from which to infer an underlying type
struct ContentView : View {
    var body: some View {
        Text("Hello World")
        Text("Hello World")
    }
}
```

Text("Hello World") 创建一个内容为 Hello World 的文本

ContentView_Previews 是用来在 Xcode 中用来预览调试的部分

> option+command+enter 打开/关闭预览 </br>
> option+command+p 生成预览 </br>
> SwiftUI Previews require macOS 10.15 or later

链接：https://www.jianshu.com/p/e86d110a897f

# View

## 屏幕

UIScreen.main.bounds.width

## 布局

- VStack: 纵向布局，默认居中对齐

VStack(alignment: .leading, spacing: 5) { } // leading 左对齐

- HStack: 横向布局，默认居中对齐

- ZStack: 覆盖布局，默认居中对齐

- Group 类似于 Fragment，可返回空元素

## 元素

- Spacer() 占位

- Divider() 分割线

- Image

Image(uiImage: UIImage(named: post.avatar)!)

Image(systemName: "heart")

- Button(action: {
  print("click follow buttom")
  }) {
  Text("关注")
  }

## 样式

```swift
Text("用户昵称")
    .font(Font.system(size: 16))
    .foregroundColor(Color(red: 242/255, green: 99/255, blue: 4/255))
    .lineLimit(1)
```

- 字体

.font(Font.system(size: 16))

.font(.system(size: 11))

.bold()

- 颜色

.foregroundColor(Color(red: 242/255, green: 99/255, blue: 4/255)) // color

.foregroundColor(.orange)

.background(Color.red) // background-color

- 行数

.lineLimit(1)

- 宽高

.frame(width: 50, height: 26)

- 边框

.stroke(Color.orange, lineWidth: 1)

- 图片

.resizable() // 图片可缩放

.scaledToFill() // 保持宽高比填充，会超出

.scaledToFit() // 保持宽高比适应，不会超出

.clipShape(Circle())

.clipped() // 超出裁剪

- 位置

.offset(x: 16, y: 16)

.padding(.leading, 10) // .leading 左

.padding(.horizontal, 15) // .horizontal 左右

- 叠加

.overlay(RoundedRectangle(cornerRadius: 13))

# Model

## 属性

let 常量， var 可变

数据类型: String, Bool, Int, [String]

```swift
struct Post: Codable {
    let id: Int
    let avatar: String
    let vip: Bool
}
```

计算属性：只读

```swift
var commentCountText: String {
    if commentCount <= 0 { return "评论" }
    if commentCount < 1000 { return "\(commentCount)"}
    return String(format: "%.1fk", Double(commentCount / 1000))
}
```

typealias Codable = Decodable & Encodable
这两个协议说明了对象能够自己编码和解码自己。

## 方法

- isEmpty 数组是否为空

```swift
if !post.images.isEmpty { }
```

- "%.1f" 保留一位小数

```swift
String(format: "%.1fk", Double(commentCount / 1000))
```

## 解析本地 json 文件

```swift
func loadPostListData(_ fileName: String) -> PostList {
    guard let url = Bundle.main.url(forResource: fileName, withExtension: nil) else {
        fatalError("Can not find \(fileName) in main bundle")
    }
    guard let data = try? Data(contentsOf: url) else {
        fatalError("Can not load \(url)")
    }
    guard let list = try? JSONDecoder().decode(PostList.self, from: data) else {
        fatalError("Can not parse post list json data")
    }
    return list
}
```

## 通过图片名称加载图片

```swift
func loadImage(name: String) -> Image {
    return Image(uiImage: UIImage(named: name)!)
}
```
