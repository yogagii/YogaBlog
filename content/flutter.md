Title: Flutter
Date: 2021-12-20
Category: IOS
Tags: Flutter
Author: Yoga

> Flutter 中万物皆为Widget。

Flutter Widget采用现代响应式框架构建，这是从 React 中获得的灵感，中心思想是用widget构建你的UI。 Widget描述了他们的视图在给定其当前配置和状态时应该看起来像什么。当widget的状态发生变化时，widget会重新构建UI，Flutter会对比前后变化的不同， 以确定底层渲染树从一个状态转换到下一个状态所需的最小更改（类似于React/Vue中虚拟DOM的diff算法）。

## Widget

runApp函数接受给定的Widget并使其成为widget树的根，根widget强制覆盖整个屏幕

* 无状态的 StatelessWidget
* 有状态的 StatefulWidget

@immutable 代表 Widget 是不可变的，这会限制 Widget 中定义的属性（即配置信息）必须是不可变的（final）

widget的主要工作是实现一个build函数，用以构建自身。一个widget通常由一些较低级别widget组成。Flutter框架将依次构建这些widget，直到构建到最底层的子widget时，这些最低层的widget通常为RenderObject

* Text
* Row, Column: 基于web Flexbox
* Stack: 基于web position absolute
* Container: background, margins, padding...

build方法有一个context参数，它是BuildContext类的一个实例，表示当前 widget 在 widget 树中的上下文，每一个 widget 都会对应一个 context 对象（因为每一个 widget 都是 widget 树上的一个节点）。

```dart
body: Container(
  child: Builder(builder: (context) {
    // 在 widget 树中向上查找最近的父级`Scaffold`  widget 
    Scaffold scaffold = context.findAncestorWidgetOfExactType<Scaffold>();
    // 直接返回 AppBar的title， 此处实际上是Text("Context测试")
    return (scaffold.appBar as AppBar).title;
  }),
),
```

## Stateful widget有状态的部件

Stateful widget 可以拥有状态，这些状态在 widget 生命周期中是可以变的，而 Stateless widget 是不可变的。

实现一个 stateful widget 至少需要两个类:

* 一个 StatefulWidget类。
* 一个 State类。 StatefulWidget类本身是不变的，但是State类中持有的状态在 widget 生命周期中可能会发生变化。

调用setState() 会为State对象触发build()方法，从而导致对UI的更新

### State生命周期

![flutter](img/flutter2.jpg)

* initState：当 widget 第一次插入到 widget 树时会被调用，对于每一个State对象，Flutter 框架只会调用一次该回调，通常在该回调中做一些一次性的操作，如状态初始化、订阅子树的事件通知等。

* didChangeDependencies()：当State对象的依赖发生变化时会被调用；InheritedWidget发生变化，那么InheritedWidget的子 widget 的didChangeDependencies()回调都会被调用。

这种机制可以使子组件在所依赖的InheritedWidget变化时来更新自身！比如当主题、locale(语言)等发生变化时，依赖其的子 widget 的didChangeDependencies方法将会被调用。

* build()：会在如下场景被调用：

在调用initState()之后。

在调用didUpdateWidget()之后。

在调用setState()之后。

在调用didChangeDependencies()之后。

在State对象从树中一个位置移除后（会调用deactivate）又重新插入到树的其它位置之后。

* reassemble()：此回调是专门为了开发调试而提供的，在热重载(hot reload)时会被调用，此回调在Release模式下永远不会被调用。

* didUpdateWidget ()：在 widget 重新构建时，会调用widget.canUpdate来检测 widget 树中同一位置的新旧节点，然后决定是否需要更新，在新旧 widget 的key和runtimeType同时相等时widget.canUpdate返回true，didUpdateWidget()就会被调用。

* deactivate()：当 State 对象从树中被移除时，会调用此回调。如果移除后没有重新插入到树中则紧接着会调用dispose()方法。

* dispose()：当 State 对象从树中被永久移除时调用；通常在此回调中释放资源。

### 在子 widget 树中获取父级 StatefulWidget 的State 对象

1.通过Context获取：context对象有一个findAncestorStateOfType()方法，该方法可以从当前节点沿着 widget 树向上查找指定类型的 StatefulWidget 对应的 State 对象

```dart
 // 查找父级最近的Scaffold对应的ScaffoldState对象
  ScaffoldState _state = context.findAncestorStateOfType<ScaffoldState>()!;
  // 打开抽屉菜单
  _state.openDrawer();

  // 如果 StatefulWidget 的状态是希望暴露出的，应当在 StatefulWidget 中提供一个of 静态方法来获取其 State 对象
  ScaffoldState _state=Scaffold.of(context);
  // 打开抽屉菜单
  _state.openDrawer();
```

2.通过GlobalKey: GlobalKey 是 Flutter 提供的一种在整个 App 中引用 element 的机制。

* globalKey.currentWidget: 该 widget 对象
* globalKey.currentElement: widget 对应的element对象
* globalKey.currentState: widget 对应的state对象。

```dart
//定义一个globalKey, 由于GlobalKey要保持全局唯一性，我们使用静态变量存储
static GlobalKey<ScaffoldState> _globalKey= GlobalKey();
...
Scaffold(
    key: _globalKey , //设置key
    ...  
)

_globalKey.currentState.openDrawer()
```

## 状态管理

* 如果状态是用户数据，如复选框的选中状态、滑块的位置，则该状态最好由父 Widget 管理。
* 如果状态是有关界面外观效果的，例如颜色、动画，那么状态最好由 Widget 本身来管理。
* 如果某一个状态是不同 Widget 共享的则最好由它们共同的父 Widget 管理。

* 跨组件状态共享（Provider）

Model变化后会自动通知ChangeNotifierProvider（订阅者），ChangeNotifierProvider内部会重新构建InheritedWidget，而依赖该InheritedWidget的子孙Widget就会更新。

```dart
Builder(builder: (context){
  var cart=ChangeNotifierProvider.of<CartModel>(context);
  return Text("总价: ${cart.totalPrice}");
}),
```

## 路由

MaterialPageRoute 是 Material组件库提供的组件，它可以针对不同平台，实现与平台页面切换动画风格一致的路由切换动画：

* 对于 Android，新页面从屏幕底部滑动到屏幕顶部；关闭页面时，当前页面从屏幕顶部滑动到屏幕底部后消失。
* 对于 iOS，新页面从屏幕右侧边缘一直滑动到屏幕左边，关闭页面时，当前页面从屏幕右侧滑出。

```dart
TextButton(
  child: Text("open new route"),
  textColor: Colors.blue,
  onPressed: () {
    //导航到新路由   
    Navigator.push( 
      context,
      MaterialPageRoute(builder: (context) {
        return NewPage(
          text: 'params' // 可传路由参数
        );
      }),
    );
  },
),
```

### 命名路由

```dart
// 注册路由表
MaterialApp(
  routes:{
   "new_page":(context) => NewRoute(),
    ...
  } ,
  home: MyHomePage(title: 'Home Page'),
);

// 通过路由名称来打开新路由
onPressed: () {
  Navigator.pushNamed(context, "new_page");
  Navigator.of(context).pushNamed("new_page", arguments: "hi"); // 传参
},
```

路由生成钩子：全局的路由跳转前置处理逻辑

如果访问的路由页需要登录，但当前未登录，则直接返回登录页路由，其它情况则正常打开路由。
```dart
onGenerateRoute:(RouteSettings settings){
  return MaterialPageRoute(builder: (context){
    String routeName = settings.name;
  }
);
```

## 事件处理

一次完整的事件分为三个阶段：手指按下、手指移动、和手指抬起。

事件处理流程：

1. 命中测试：当手指按下时，触发 PointerDownEvent 事件，按照深度优先遍历当前渲染（render object）树，对每一个渲染对象进行“命中测试”（hit test），如果命中测试通过，则该渲染对象会被添加到一个 HitTestResult 列表当中。
2. 事件分发：命中测试完毕后，会遍历 HitTestResult 列表，调用每一个渲染对象的事件处理方法（handleEvent）来处理 PointerDownEvent 事件，该过程称为“事件分发”（event dispatch）。
3. 事件清理：当手指抬（ PointerUpEvent ）起或事件取消时（PointerCancelEvent），会先对相应的事件进行分发，分发完毕后会清空 HitTestResult 列表。

通过命中测试Hit Test的组件触发事件，事件会从最内部的组件被分发到组件树根的路径上的所有组件，和Web浏览器的事件冒泡机制相似， 但是Flutter中没有机制取消或停止“冒泡”过程。

```dart
Listener(
  child: Container(...),
  onPointerDown: (PointerDownEvent event) => ...,
  onPointerMove: (PointerMoveEvent event) => ...,
  onPointerUp: (PointerUpEvent event) => ...,
)
```

IgnorePointer和AbsorbPointer，这两个组件都能阻止子树接收指针事件，不同之处在于AbsorbPointer本身会参与命中测试，而IgnorePointer本身不会参与

### 手势识别

```dart
GestureDetector(
  child: Container(...),
  onTap: () => ..., //点击
  onDoubleTap: () => ..., //双击
  onLongPress: () => ..., //长按
  onPanDown: (DragDownDetails e) => ..., //手指按下
  onPanUpdate: (DragUpdateDetails e) => ..., //手指滑动
  onPanEnd: (DragEndDetails e) => ... //滑动结束
  onVerticalDragUpdate: (DragUpdateDetails details) => ..., //垂直方向拖动事件
  onScaleUpdate: (ScaleUpdateDetails details) => ..., // 缩放
)
```
```dart
TextSpan(
  text: "...",
  recognizer: _tapGestureRecognizer
    ..onTap = () => ...,
)
```

## 包管理

pubspec.yaml
```dart
dependencies:
  english_words: ^4.0.0 // Pub仓库
  pkg1:
    path: ../../code/pkg1 // 依赖本地包
  pkg2:
    git:
      url: git://github.com/xxx/pkg1.git // git仓库
```