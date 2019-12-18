Title: React 路由
Date: 2019-08-17
Category: React
Tags: React, Route
Author: Yoga

前端路由每次访问一个新页面的时候都要向服务器发送请求，然后服务器响应请求；而前端路由访问一个新页面的时候仅仅变换了一下路径，没有网络延迟。因此前端路由相较于后端路由，在性能和用户体验上有相当大的提升。

```javascript
import {Router, Route, browserHistory} from 'react-router';
render ((
  <Router history = {browserHistory}>
    <Route path="/" component={APP} /> //嵌套
      <IndexRoute component={Home} /> //默认
      <Redirect from="messages/:id" to="/messages/:id" /> //重定向
      <IndexRedirect to="/welcome" /> //访问跟路由时重定向到子组件
      <Route name="course" path="course/:id" handler={course} /> //带参数
      <NotFoundRoute handler={NotFound} /> //未匹配
    </Route>
  </Router>
), document.getElementById('app));
//嵌套路由
render() {
  return(
    <div>
      {this.props.children}
    </div>
  );
}
//在APP内部加载About组件
let routes = <Route path="/about" component={About} />
<Router routes={routes} />
```

### 路由配置

默认路由：指定默认情况下加载的子组件。

path属性不以"/"开头时是相对路径。

path规则匹配只执行最先遇到的规则（从上往下），所以带参数的路径要写在路由规则底部。

获得URL字符串 /foo?bar=baz中foo后面的参数：this.props.location.query.bar

NotFoundRoute组件用于声明父组件匹配成功但未找到子组件

Redirect用于路由跳转

IndexRedirect用于访问跟路由时重定向到某个子组件

history属性用来监听浏览器地址栏的变化

* hashHistory: 路由会计算URL的hash值，并根据hash值切换
* browserHistory: 地址是在本地切换，不能向服务器请求子路由(--history-api-fallback)
* createMemoryHistory: 主要用户服务器渲染

路由回调 Enter/Leave 进入/离开该路由时触发

```javascript
//onEnter 实现认证功能
<Route path="/admin" component={Admin} onEnter={requireAuth} />
//onEnter 实现redirect
<Route path="/admin" component={Admin} onEnter={
  ({params}, replace) => replace(`messages/${params.id}`)
} />
```

### 路由切换

a元素的react的版

```javascript
<Link to="about" activeStyle={{color:'red'}} activeClassName="active">About</Link>
```

IndexLink: 可以对路径进行精确匹配

```javascript
<IndexLink to="/">Home</IndexLink>
<Link to="/" onlyActiveOnIndex={true}>Home</Link>
```

动态切换

```javascript
browserHistory.push(path);
this.context.router.push(path);
```