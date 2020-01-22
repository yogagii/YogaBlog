Title: F1nance GTM
Date: 2020-01-17
Category: Analytics
Tags: GTM
Author: Yoga

结果 https://analytics.google.com/

配置 https://tagmanager.google.com

## 变量

```
document.cookie = `apiErrorCode=${error.status}`;
```

命名变量：Api Status

变量类型：第一方Cookie -> Cookie名称：apiErrorCode

----

命名变量：Clicked Video Title

变量类型：自定义Javascript
```
function() {
  var clickedDOM = {{Click Element}}; // 内置变量
  return clickedDOM.parentElement.childNodes[0].innerText;
}
```


## 触发器

```
window.dataLayer.push({ event: 'api-error' });
```

命名触发器：Call Api Failed

触发器类型：自定义事件 -> 事件名称：api-error


## 代码

命名代码：Tag - Call Api - Error

代码类型：Google Analytics: Universal Analytics

跟踪类型：事件

类别：API

操作：Error

标签：{{Api Url}};{{Api Message}};{{UserId}}

值：{{Api Status}}

Google Analytics设置：{{Google Analytics Settings}}

![Flux](img/Google-Analytics-Settings.png)

触发条件：自定义事件 -> Call Api Failed