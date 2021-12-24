Title: Angular应用
Date: 2021-11-29
Category: Angular
Tags: Angular
Author: Yoga

## 组件 Components

带有 @Component() 装饰器的 TypeScript 类

@Component() 装饰器:
* CSS 选择器 ('app-'+组件名称)
* HTML 模板
* 一组可选的 CSS 样式

```js
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent { }
```

@input() 装饰器：

用来把某个类字段标记为输入属性，并提供配置元数据。 当变更检测时，Angular 会自动使用这个 DOM 属性的值来更新此数据属性。

## 模板 Templates

* 双花括号：插入动态值

```ts
//app.component.html
<p>{{ message }}</p>
//app.component.ts
export class HelloWorldInterpolationComponent {
    message = 'Hello, World!';
}
```

* 方括号：属性绑定

```html
<p
  [id]="sayHelloId"
  [style.color]="fontColor">
  You can set my color in the component!
</p>
```

* 圆括号：事件监听器

```ts
//app.component.html
<button
  [disabled]="canClick"
  (click)="sayMessage()">
  Trigger alert message
</button>
//app.component.ts
export class HelloWorldBindingsComponent {
  canClick = false;
  message = 'Hello, World';
 
  sayMessage() {
    alert(this.message);
  }
 
}
```

* 指令directives：*ngIf，*ngFor

```ts
<div *ngIf="canEdit; else noEdit">
  <p>You can edit the following paragraph.</p>
</div>
```

## 依赖注入 Dependency injection

声明 TypeScript 类的依赖项

```ts
// logger.service.ts
import { Injectable } from '@angular/core';

@Injectable({providedIn: 'root'})
export class Logger {
  writeCount(count: number) {
    console.warn(count);
  }
}
//app.component.ts
import { Logger } from '../logger.service';

export class HelloWorldDependencyInjectionComponent  {
  constructor(private logger: Logger) { }
  onLogMe() {
    this.logger.writeCount(this.count);
  }
}

```