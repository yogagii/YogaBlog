Title: RESTful API
Date: 2019-09-21
Category: Backend
Tags: Rest
Author: Yoga

> REST，即Representational State Transfer(表现层状态转化)。它是一种互联网应用程序的API设计理念：URL定位资源，用HTTP动词（GET,POST,DELETE,DETC）描述操作。

Restful与传统接口对比

| 操作 | 传统风格 | RESTful风格
| - | - | - 
查询 | /user/query?name=tom GET | /user?name=tom GET
详情 | /user/getInfo?id=1 GET | /user/1 GET
创建 | /user/create?name=tom POST | /user POST
修改 | /user/update?id=1&name=jquery POST | /user/1 PUT
删除 | /user/delete?id=1 GET | /user/1 DELETE

Resultful特点:

1.使用URL描述资源

2.使用HTTP方法描述行为。使用HTTP状态码来表示不同的结果

3.使用json交互数据，传统模式使用的是键值对形式


## 路径 Endpoint

> url地址中只包含名词表示资源，使用http动词表示动作进行操作资源

https://api.example.com/v1/

将API部署在专用域名之下,将API的版本号放入URL。

路径又称"终点"（endpoint），表示API的具体网址。
在RESTful架构中，每个网址代表一种资源（resource），所以网址中不能有动词，只能有名词，而且所用的名词往往与数据库的表格名对应。一般来说，数据库中的表都是同种记录的"集合"（collection），所以API中的名词也应该使用复数。

https://api.example.com/v1/zoos

## 动词

* GET（SELECT）：从服务器取出资源（一项或多项）。 

/zoos：列出所有动物园

/zoos/ID：获取某个指定动物园的信息

/zoos/ID/animals：列出某个指定动物园的所有动物

/users?page=1&pageSize=10：分页 pagination

/users?region=US,China：过滤 filtering

/users?sort_by=first_name&order=asc：排序 sortby single column

/users?sort=first_name:asc,age:desc：排序 sortby multiple columns

* POST（CREATE）：在服务器新建一个资源。

/zoos：新建一个动物园

* PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。

/zoos/ID：更新某个指定动物园的信息（提供该动物园的全部信息）

* PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。

/zoos/ID：更新某个指定动物园的信息（提供该动物园的部分信息）

* DELETE（DELETE）：从服务器删除资源。

/zoos/ID：删除某个动物园

/zoos/ID/animals/ID：删除某个指定动物园的指定动物

* HEAD：获取资源的元数据。

* OPTIONS：获取信息，关于资源的哪些属性是客户端可以改变的

## 状态码（Status Codes）

* 200 OK - [GET]：服务器成功返回用户请求的数据，该操作是幂等的（Idempotent）。

* 201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。

* 202 Accepted - [*]：表示一个请求已经进入后台排队（异步任务）

* 204 NO CONTENT - [DELETE]：用户删除数据成功。

* 400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。

* 401 Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）。

* 403 Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的。

* 404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。

* 406 Not Acceptable - [GET]：用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。

* 410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的。

* 422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误。

* 500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功。

参考文献：http://www.ruanyifeng.com/blog/2014/05/restful_api.html

官网：https://restfulapi.cn/
