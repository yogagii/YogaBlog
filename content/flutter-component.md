Title: Flutter Component
Date: 2021-12-31
Category: IOS
Tags: Flutter
Author: Yoga

## 基础组件

文本
```dart
Text("Hello world",
  textAlign: TextAlign.left,
  maxLines: 1,
  overflow: TextOverflow.ellipsis,
  textScaleFactor: 1.5,
  style: TextStyle(
    color: Colors.blue,
    fontSize: 18.0,
    height: 1.2,  // 行高
    fontFamily: "Courier",
    background: Paint()..color=Colors.yellow,
    decoration:TextDecoration.underline,
    decorationStyle: TextDecorationStyle.dashed
  ),
);

Text.rich(TextSpan(
  children: [
    TextSpan(
      text: "Home: "
    ),
))
```
按钮
```dart
ElevatedButton(
  child: Text("normal"),
  onPressed: () {},
);
ElevatedButton.icon(
  icon: Icon(Icons.send),
  label: Text("发送"),
  onPressed: _onPressed,
),

TextButton(
  child: Text("normal"),
  onPressed: () {},
)

OutlineButton(
  child: Text("normal"),
  onPressed: () {},
)

IconButton(
  icon: Icon(Icons.thumb_up),
  onPressed: () {},
)
```

图片
```dart
Image(
  image: AssetImage("images/avatar.png"),
  image: NetworkImage( "https://avatars2.githubusercontent.com/u/20411648?s=460&v=4"),
  width: 100.0,
  fit: BoxFit.fill,
  color: Colors.blue,
  colorBlendMode: BlendMode.difference, // 对每一个像素进行颜色混合处理
  repeat: ImageRepeat.repeatY,
);
```

单选开关
```dart
Switch(
  value: _switchSelected,//当前状态
  onChanged:(value){
    setState(() {
      _switchSelected=value;
    });
  },
)
```

复选框
```dart
Checkbox(
  value: _checkboxSelected,
  activeColor: Colors.red, //选中时的颜色
  onChanged:(value){
    setState(() {
      _checkboxSelected=value;
    });
  } ,
)
```

输入框
```dart
TextField(
  autofocus: true,
  decoration: InputDecoration(
    labelText: "用户名",
    hintText: "用户名或邮箱",
    prefixIcon: Icon(Icons.person)
  ),
),
```

## 布局类组件

* 非容器类组件基类
* 单子组件基类: child用于接收子 Widget
* 多子组件基类: children用于接收子 Widget

线性布局：Row 沿水平方向排列其子widget
```dart
Row(
  crossAxisAlignment: CrossAxisAlignment.start,  
  verticalDirection: VerticalDirection.up,
  mainAxisAlignment: MainAxisAlignment.spaceEvenly, // 将水平方向的的剩余显示空间均分成多份穿插在每一个 child之间
  children: <Widget>[
    Text("t1"),
    Text("t2"),
  ],
),
```
Row默认只有一行，如果超出屏幕不会折行，右边溢出部分报错。

Column可以在垂直方向排列其子组件

弹性布局：Expanded 只能作为 Flex 的孩子（否则会报错），它可以按比例“扩伸”Flex子组件所占用的空间。
```dart
Flex(
  direction: Axis.vertical,
  children: <Widget>[
    Expanded(
      flex: 2,
      child: Container(
        height: 30.0,
        color: Colors.red,
      ),
    ),
    Spacer(flex: 1), // 占用指定比例的空间
    Expanded(
      flex: 1,
      child: Container(
        height: 30.0,
        color: Colors.green,
      ),
    ),
  ],
)
```

流式布局：超出屏幕显示范围会自动折行
```dart
Wrap(
   spacing: 8.0, // 主轴(水平)方向间距
   runSpacing: 4.0, // 纵轴（垂直）方向间距
   alignment: WrapAlignment.center, //沿主轴方向居中
   children: <Widget>[
     Chip(
       avatar: CircleAvatar(backgroundColor: Colors.blue, child: Text('A')),
       label: Text('Hamilton'),
     ),
     ...
   ],
)
```

层叠布局：Stack允许子组件堆叠，而Positioned用于根据Stack的四个角来确定子组件的位置

```dart
Stack(
  alignment:Alignment.center , //指定未定位或部分定位widget的对齐方式
  fit: StackFit.expand, //未定位widget占满Stack整个空间
  children: <Widget>[
    Container(
      child: Text("Hello world"),
      color: Colors.red,
    ),
    Positioned(
      left: 18.0,
      child: Text("I am Jack"),
    ),
  ],
)
```

相对定位：Align 组件可以调整一个子元素在父元素中的位置
```dart
Align(
  alignment: Alignment.topRight,
  child: FlutterLogo(
    size: 60,
  ),
),
```
Center继承自Align(Alignment.center)。
```dart
Center(
  child: Text("xxx"),
)
```

使用 LayoutBuilder 来根据设备的尺寸来实现响应式布局。

```dart
LayoutBuilder(
  builder: (BuildContext context, BoxConstraints constraints) {
    if (constraints.maxWidth < 200) {
      return ...;
    } else {
      return ...;
    }
  },
)
```

## 容器类组件

Padding可以给其子节点添加填充（留白）
```dart
Padding(
  // 分别指定四个方向的补白
  padding: const EdgeInsets.fromLTRB(20.0,.0,20.0,20.0),
  child: Text("Your friend"),
)
```

尺寸限制类容器：ConstrainedBox用于对子组件添加额外的约束
```dart
ConstrainedBox(
  constraints: BoxConstraints(
    minWidth: double.infinity, //宽度尽可能大
    minHeight: 50.0 //最小高度为50像素
  ),
  child: Container(
    height: 5.0, 
    child: redBox ,
  ),
)

BoxConstraints.tight(Size size) // 生成固定宽高
BoxConstraints.expand() // 填充尽可能大的容器

SizedBox(
  width: 80.0,
  height: 80.0,
  child: redBox
)
```

空间适配FittedBox：子组件适配父组件空间

```dart
FittedBox(
  fit: BoxFit.contain, // 按照子组件的比例缩放，尽可能多的占据父组件空间
  child: Container(...),
)
```
封装单行缩放布局：SingleLineFittedBox
```dart
FittedBox(
  child: ConstrainedBox(
    constraints: constraints.copyWith(
      minWidth: constraints.maxWidth,
      maxWidth: double.infinity,
    ),
    child: child,
  ),
)
```
装饰容器DecoratedBox：背景、边框、渐变

```dart
DecoratedBox(
  decoration: BoxDecoration(
    gradient: LinearGradient(colors:[Colors.red,Colors.orange.shade700]), //背景渐变
    borderRadius: BorderRadius.circular(3.0), //3像素圆角
    boxShadow: [ //阴影
      BoxShadow(
        color:Colors.black54,
        offset: Offset(2.0,2.0),
        blurRadius: 4.0
      )
    ]
  ),
child: ...,
)
```

变换 Transform
```dart
Transform.translate // 平移
Transform.rotate // 旋转
Transform.scale // 缩放
```

Transform的变换是应用在绘制阶段，所以无论对子组件应用何种变化，其占用空间的大小和在屏幕上的位置都是固定不变的。

RotatedBox的变换是在layout阶段，会影响在子组件的位置和大小。

组合类容器 Container具备多种组件的功能
```dart
Container(
  margin: EdgeInsets.all(20.0), //容器外补白
  padding: EdgeInsets.all(20.0), //容器内补白
  constraints: BoxConstraints.tightFor(width: 200.0, height: 150.0),//卡片大小
  decoration: BoxDecoration(...), //背景装饰
  transform: Matrix4.rotationZ(.2), //卡片倾斜变换
  alignment: Alignment.center, //卡片内文字居中
  child: Text("5.20"),
)
```

剪裁 Clip
```dart
ClipOval(child: avatar), //剪裁为圆形
ClipRRect( //剪裁为圆角矩形
  borderRadius: BorderRadius.circular(5.0),
  child: avatar,
), 
ClipRect	// 溢出部分剪裁
```

Scaffold 是一个路由页的骨架
```dart
Scaffold(
  appBar: AppBar(), // 导航栏
  drawer: MyDrawer(), // 抽屉
  bottomNavigationBar: BottomNavigationBar(), // 底部导航
  floatingActionButton: FloatingActionButton(),  //悬浮按钮
)
```
## 颜色和主题

color 使用的是 ARGB, 前两位表示透明度

```dart
// RED
#ff0000 // RGB
0xffff0000 // ARGB
```

primarySwatch是主题颜色的一个"样本色"

