Title: Google Tag Manager
Date: 2019-07-20
Category: Analytics
Tags: GTM
Author: Yoga

## 谷歌标签管理器

### 优点：

1. 通过GTM可以更快测试和发布代码而不需要在站点上硬编码

2. 个性化跟踪

3. 管理更有效

4. 提高网站加载速度，优化了异步加载

### 缺点：

多一层跳转：先加载GTM容器，再加载其他跟踪代码，如GA

### 账户结构：

一个google可以有多个GTM account，

一个account可以有多个GTM Container Tag，

每个容器对应一个站点（Tag，Trigger，Variables）

### Variable变量

变量是键值对，其中的值在运行时填充

1. 在触发器中，变量用来定义指定特定触发器应在何时执行的过滤条件（URL变量）

2. 在代码中，变量用来捕获动态值，传递到转化跟踪代码

### built-in variable内置变量：

网页：

* Page Hostname(域名)

* Page Path(路径)

* Page URL(网址)

* Referrer(引荐来源网址)utm_source=BAIDU

工具：

* Container ID

* Container Version

* Environment Name

* Event(当前dataLayer事件的名称)

* HTMLID

错误：

点击:（设置Trigger时限定点击位置）

* Click Element(访问dataLayer中的gtm.element键)

* Click Classes

* Click ID

* Click Target

* Click URL

* Click Text

表单：

Form ID

历史

### User-Defined Variables自定义变量：

第一方Cookie:名称与用户所在网域匹配的第一个Cookie（第一方cookie变量返回的是浏览器cookie中该变量的值,如用户等级，用户IP）

内置变量

常量字符串(如经常需要使用的ga tracking id可以定义为常量)

容器版本号

自定义JavaScript(可返回值的匿名函数)

数据层变量(dataLayer.push({'Data Layer Name': 'value'}))

调试模式

DOM元素

HTTP引荐来源网址(用户访问的前一个网页)

Javascript变量(获取指定的全局变量)

对照表（批量做数据跟踪）

随机数字

网址


### Trigger:控制触发条件

页面触发器：

* Page View：GTM容器代码被成功加载，在看到页面内容之前就触发了，用于页面浏览跟踪

* Dom Ready：当DOM准备好，既已经渲染完所有html元素时触发，用于跟踪某些东西已被呈现

* Window Loaded：当浏览器已经显示完搜有信息时触发

点击触发器：（监听用户的大部分交互）

* All Element：所有左键点击（图片，按钮，链接，元素）

* Just Links：只有html链接

自定义事件：

在控制台输入dataLayer可以查看推送到指定页面上的数据层的事件序列

### Tag

代码指的是向第三方（Google）发送信息的js代码段

应用场景：部署跟踪代码、事件跟踪、电子商务、注入代码

export container / import container

下载配置json

### GTM数据传输模型：

1. 部署第三方代码：trigger -> tag -> GA

2. 主动push数据（电子商务）：Web(dataLayer) -> Trigger -> tag -> GA

3. 常规事件跟踪：Web -> Variable/trigger -> tag -> GA

4. 网页面注入js跟踪：Web -> Variable/trigger -> tag -> 注入Web主动监听 / GA

### GTM debug: Publish -> Preview

事件部署不成功：

1. 触发器没设置正确

2. 页面端没有将数据正确推送出去

tag manager inject


跨子域跟踪：共用顶级域名下的cookie（识别用户唯一性）

GA默认开启

GTM：

Field name: cookie domain; value:auto

add referer exclusive

设置cookie domin和引荐流量：将两个二级域名之间跳转事的用户和会话降










