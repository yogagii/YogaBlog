Title: Flutter
Date: 2021-12-20
Category: IOS
Tags: Flutter
Author: Yoga

Flutter Widget采用现代响应式框架构建，这是从 React 中获得的灵感，中心思想是用widget构建你的UI。 Widget描述了他们的视图在给定其当前配置和状态时应该看起来像什么。当widget的状态发生变化时，widget会重新构建UI，Flutter会对比前后变化的不同， 以确定底层渲染树从一个状态转换到下一个状态所需的最小更改（类似于React/Vue中虚拟DOM的diff算法）。

## Widget

runApp函数接受给定的Widget并使其成为widget树的根，根widget强制覆盖整个屏幕

* 无状态的 StatelessWidget
* 有状态的 StatefulWidget

widget的主要工作是实现一个build函数，用以构建自身。一个widget通常由一些较低级别widget组成。Flutter框架将依次构建这些widget，直到构建到最底层的子widget时，这些最低层的widget通常为RenderObject

* Text
* Row, Column: 基于web Flexbox
* Stack: 基于web position absolute
* Container: background, margins, padding...

Widget是不可变的, Widget中定义的属性必须是 final.

## Stateful widget有状态的部件

Stateful widget 可以拥有状态，这些状态在 widget 生命周期中是可以变的，而 Stateless widget 是不可变的。

实现一个 stateful widget 至少需要两个类:

* 一个 StatefulWidget类。
* 一个 State类。 StatefulWidget类本身是不变的，但是State类中持有的状态在 widget 生命周期中可能会发生变化。

调用setState() 会为State对象触发build()方法，从而导致对UI的更新

