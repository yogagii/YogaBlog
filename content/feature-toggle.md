Title: Feature Toggle
Date: 2021-10-26
Category: Programming
Author: Zack, Yoga

Feature Toggles (often also refered to as Feature Flags) are a powerful technique, allowing teams to modify system behavior without changing code. 允许团队不用修改代码而来改变系统的功能行为。

"Feature Toggling" is a set of patterns which can help a team to deliver new functionality to users rapidly but safely. 

https://martinfowler.com/articles/feature-toggles.html

### Types of Feature Toggles

* Release Toggle: When developing code that is not ready for consumption and has a high risk of breaking the application. 发布型：出现在生产环境上，用于开放或者隐藏部分特性功能的toggle；
* Experimental Toggle: When performing multivariate testing (e.g. AB Testing). 体验型：即A/B testing，用于区分A、B方案的实际使用情况；
* Operation Toggle: When rolling out a new feature with unclear performance impact. 操作型：提供给操作员工的一系列特殊操作。比如遭到DOS攻击时可以关掉网络端口。
* Permission Toggle: Used in cases of dogfooding, alpha and beta programs. 权限型：使得部分指定范围内的用户可以体验到新特性功能，而并不是面向全部用户。


### Why Feature Toggle

> Feature Toggle allows us to decouple Release from Deployment

* Deployed: A technical concern that applies in the domain of the team and means __the functionality is introduced in Production__.
* Released: A business term that defines functionality being available to an end-user. __Deployed doesn’t necessarily mean Released.__

每两个周发布一次生产版本，但是同时又需要去维护一个很多个月才能进行发布的特性分支。feature toggle可以保障团队成员们在开发主线(mainline)上的工作不受到未完全实现的特性分支的影响.

https://www.jianshu.com/p/6931b0abc956

### When do we remove it

* When experiment is over (We can’t be doing one experiment forever)
* When release is approved (e.g. Mock Closing ended)

| - | Permission Toggle | Authorization Service
| - | - | -
Purpose | To hide release from deployment. Experiment new feature for specific users before releasing for public use. | To limit user access on long-term capabilities and by job roles. For example, admin page, data access etc.
Longevity | Short Term (Time-boxed) | Long Term
Maintenance | Product Team only | Business Admin (by Job Role)

Introduce purpose-fit implementation separately for Permission Toggle and Authorization Service.

### Feature Toggle Lifecycle

* When setting up feature toggle, it will be disabled by default. Any users that want to see the feature needs to opt in.
* When feature is ready to be released to general users, we can enable the feature by default.
* At the end of the lifecycle, the feature toggle would be removed in the next release.

> Disabled by default -> Enabled for developers -> Enabled for QA -> Enabled for Product Team -> Enabled for UAT users -> Enabled for general users -> Remove Feature Toggle

### Maintain Toggle Config file

基础思路：存在一个配置文件，配置文件里定义了许多的toggle，这些toggle都是待发布的特性功能。这一些toggle定义了哪一些features需要呈现，哪些并不需要。

* Toggle feature (on/off) by updating Toggle Config File for each environments.
* This config file will be maintained in source code repository for version control.
* CICD pipeline will be set up differently from existing Frontend code build pipeline.
* Config file will be maintained in a different bucket / different folder from existing site assets.
* Raise a Jira ticket and assign to dev team to update config file for lower environments (dev,
stage, preprod); or raise a support ticket.
* Raise a support ticket to update config file for production site.

1. Edit config file in code repository (Bitbucket)
2. Push edited config file into Bitbucket
3. Changes in Bitbucket triggers CICD pipeline
4. CICD pipeline
pushes edited config file into S3 bucket
5. Config file is served via Lambda & API Gateway

```js
// toggleConfig.json
{
   "defaults":{
      "feature1": false
   },
   "groups":{
      "developer": {
         "feature1": true
      }
   },
   "users":{
      "user1":{
         "feature1": false
      },
   }
}
// toggleGroupConfig.json
{
	"developer":[ "user1" ],
	"productOwner": [ "user2" ]
}
```