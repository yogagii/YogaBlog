Title: Swift UI
Date: 2020-03-20
Category: IOS
Tags: Swift
Author: Yoga

## UIViewController

1. AppDelegate.swift 程序入口 (负责逻辑)

didFinishLauchingOptions第一次打开程序

2. SceneDelegate（负责UI）应用的入口和生命周期

willConnectTo第一加载页面

sceneWillEnterForeground即将进入前台

sceneDidBecomeActive进入前台

3. ViewController 一个页面

```
 class ViewController: UIViewController

```

UIViewController

UITabBarController底部tab栏

UINavigationController数组（栈）路由，有顶层导航栏可以显示页面名字

UITableViewController list

UICollectionViewController

生命周期

```
override func viewDidLoad() {

}
```
viewDidLoad

viewWillAppear
viewWilllayoutSubviews


viewDidAppear

viewDidDisappear

deinit {
}



4. Main storyboard

5. LaunchScreen.storyboard

6. info.plist配置

## UIView

1. 静态的 label，img

2. 可交互的 button



## Interface Builder

## Layout by Code

## Swift UI

需要最新macOS

## Custom UIView

## Screen Adaptation