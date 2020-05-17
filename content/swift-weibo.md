Title: Weibo demo
Date: 2020-04-09
Category: IOS
Tags: Swift
Author: Yoga

open.weibo.com/wiki

SwiftUI是一个优秀的用户界面框架


| UIKit | SwiftUI
:-: | :-: |
UILabel | Text
UIStackView 垂直排列时 | VStack
UIStackView 水平排列时 | HStack
UIButton | Button

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

ContentView遵循View协议，在SwiftUI中想要显示任何的视图，都需要遵循View，通过通过body属性来返回视图

body返回类型 some View。some是swift5.1新增加的一种返回类型，返回some View意味着body属性将要返回一个遵循View协议的视图，必须返回一个子视图

Text("Hello World") 创建一个内容为Hello World的文本

ContentView_Previews是用来在Xcode中用来预览调试的部分

> option+command+enter 预览 </br>
SwiftUI Previews require macOS 10.15 or later

链接：https://www.jianshu.com/p/e86d110a897f

## 布局

* VStack: 纵向布局，默认居中对齐
* HStack: 横向布局，默认居中对齐
* ZStack: 覆盖布局，默认居中对齐

占位 Spacer()