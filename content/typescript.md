Title: TypeScript
Date: 2021-12-1
Category: Angular
Tags: TypeScript
Author: Yoga

## interface VS type

```ts
interface Name {
  name: string
}

type Name = {
  name: string
}
```

- 拓展（extends）

  ```ts
  // interface extends interface
  interface User extends Name {
    age: number
  }

  // interface extends type
  interface User extends Name {
    age: number
  }

  // type extends type
  type User = Name & {
    age: number
  }
  // type extends interface
  type User = Name & {
    age: number
  }
  ```

- type 可以声明基本类型别名，联合类型，元组等类型

  ```ts
  type Name = string // 基本类型别名
  type PetList = [Dog, Pet] // 具体定义数组每个位置的类型
  ```

- type 语句中还可以使用 typeof 获取实例的 类型进行赋值

  ```ts
  let div = document.createElement('div')
  type B = typeof div
  ```

- interface 能够声明合并

  ```ts
  interface User {
    name: string
  }

  interface User {
    sex: string
  }

  /*
  User 接口为 {
  name: string
  sex: string 
  }
  */
  ```

  原文链接：https://juejin.im/post/5c2723635188252d1d34dc7d#heading-11

### 泛型

- Pick 选择

  pick<T，keys>：从Type中选择一系列属性来构造新类型

- Omit 省略

  omit<T，keys>：从Type中移除一系列属性值

  ```ts
  interface Props{
    A:string
    B:string
    C:number[]
  }
  type PickProps= Pick<Props,'A'|'B'> // A, B
  type OmitProps = Omit<Props,'A'|'B'>; // C
  ```

- Exclude 排除

  Exclude<T,U> 从第一个联合类型参数中，将第二个联合类型中出现的联合项全部排除

- Extract 提取

  Extract<T,U> 提取Type中所有能够赋值给Union的属性

  ```ts
  type A = "age" | "name";
  type B = "like" | "name";
  type C = Exclude<A, B>; // 'age'
  type D = Extract<A, B>; // 'name'
  ```
___
## 装饰器 Decorators

随着 TypeScript 和 ES6 里引入了类，在一些场景下我们需要额外的特性来支持标注或修改类及其成员。 装饰器（Decorators）为我们在类的声明及成员上通过元编程语法添加标注提供了一种方式。

在命令行或 tsconfig.json 里启用 experimentalDecorators 编译器选项：

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "es2017",
    "experimentalDecorators": true
  }
}
```

装饰器是一种特殊类型的声明，它能够被附加到类声明，方法， 访问符，属性或参数上。 装饰器使用 @expression 这种形式，expression 求值后必须为一个函数，它会在运行时被调用，被装饰的声明信息做为参数传入

- 装饰器工厂

普通装饰器，无法传参，装饰器工厂,可传参

```ts
// 定义装饰器工厂
function logClass(params: string) {
  return function (target: any) {
    console.log('target：', target);
    console.log('params：', params);

    target.prototype.apiUrl = params;
  }
}

@logClass('http:www.baidu.com')
class HttpClient {
  constructor() {
  }

  getData() {
  }
}

let http = new HttpClient();
console.log(http.apiUrl);
```

- 装饰器组合

```ts
// 书写在同一行上
@f @g x

// 书写在多行上
@f
@g
x
```

- 类装饰器

类装饰器在类声明之前被声明（紧靠着类声明）。 类装饰器应用于类构造函数，可以用来监视，修改或替换类定义。

类装饰器表达式会在运行时当作函数被调用，类的构造函数作为其唯一的参数。如果类装饰器返回一个值，它会使用提供的构造函数来替换类的声明。

```ts
@sealed
class Greeter {}
```

- 方法装饰器

```ts
class Greeter {
  @enumerable(false)
  greet() {}
}
```

- 访问器装饰器

```ts
class Point {
  @configurable(false)
  get x() {
    return this._x
  }
}
```

- 属性装饰器

```ts
class Greeter {
  @format('Hello, %s')
  greeting: string
}
```

- 参数装饰器

```ts
class Greeter {
  greet(@required name: string) {}
}
```
___

## 依赖注入

```ts
class B { }
class A {
  public b: B;
  constructor() {
    this.b = new B(); // 修改B类需要修改A类
  }
}

// main
const a = new A();
```

__依赖注入（DI）__： 通过A的构造函数将B的实例注入

```ts
class B { }
class A {
  constructor(public b: B) { 
    console.log(b);
  }
}

// main
const b = new B(); // 修改B类只需要修改主程序即可
const a = new A(b); // 将B的实例注入到a中
```

解决问题
1. 通过往构造函数中传入b来创建a，A类不再亲自创建b，而是消费它们，此时最大的好处就是B与A解除了强耦的关系。如果有一天对B进行升级，在创建B的时候需要传入一个参数，这时候不需要修改A类，只需要修改主程序即可
2. 在new A的时候，可以传入任何类型的b。export class B1 extends B
3. 实现数据共享。如果是通过在A里new Service的方式，是无法实现数据共享和通信的，因为不同A里的Service不是同一个实例。
4. 测试用例

__控制反转（IOC）__：类A依赖类B，但A不控制B的创建和销毁，仅使用B，那么B的控制权则交给A之外处理

__IOC Container（容器）__：IOC容器负责管理对象的生命周期、依赖关系等，实现对象的依赖查找以及依赖注入（NestJS 运行时系统，Angular框架的依赖注入器）

链接：https://www.jianshu.com/p/89249a3da84e

## Config

踩坑：

Consider using '--resolveJsonModule' to import module with '.json' extension.

```json
// tsconfig.json
{
  "compilerOptions": {
    "resolveJsonModule": true
  }
}
```

---

(type: keyof typeof colorMap) => colorMap[type]