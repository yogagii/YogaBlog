Title: Wecom Admin Portal
Date: 2025-02-07
Category: Project
Author: Yoga
Password: project

## Project Overview

#### Enterprise WeChat

A communication channel for JNJ Medical Sales Representatives to communicate with External HCP via WeChat

#### Wecom Admin Portal

Manage Conversation Records between JNJ Employee and the External HCP. Main functionality includes

* Managing employee's Enterprise WeChat account
* Monitoring of 1v1 or Group Chat conversation content
* Audit trail of Admin Console operations, data query, data exports

## Tech Overview

* Java
  * Spring boot
* VueJS
* Security testing
  * SonarQube
  * Snyk
  * NoName API Security Test
  * Pen Test
* File system
  * ADF
  * Azure blob mount
  * Malware scan
  * Azure cognitive service
* CI/CD
  * Kubernetes
  * Key Vault
* Wecom

## Wecom

### 登录

企微不支持邮箱能录，只支持手机号登陆。
目前企业微信用户必须为已实名认证的状态，才支持使用外部沟通能力。不实名的影响是会有可能无法添加企业微信外部联系人或微信联系人。

用户换手机号和手机号换用户两种情况：
1. 根据员工手机号查企微用户id，如果企微用户id不等于当前要同步员工数据对应的邮箱号码，则调腾讯删除接口，把该手机号之前使用的用户数据删除；意味着手机号如果换用户就是新账号。
2. 根据邮箱查腾讯企微用户id，如果企微用户id不等于当前要同步员工数据对应的邮箱号码，则调腾讯删除接口，把该员工邮箱之前使用的手机号的账号删除。意味着用户如果换手机号就是换账号了。

### 二次登陆

当成员触发了二次验证时，会自动跳转到企业配置的验证页面，并且会带上如下参数：code=CODE。拿到code之后企业可以通过[获取用户二次验证信息](https://developer.work.weixin.qq.com/document/path/99519#50693)接口获取到需要验证成员的userid和tfa_code，

**请求方式：** POST（**HTTPS**）

**请求地址：** https://qyapi.weixin.qq.com/cgi-bin/auth/get_tfa_info?access_token=ACCESS_TOKEN

**参数说明：** `{	"code": "CODE" }`

待验证用户身份信息无误后，再调用[通过二次验证](https://developer.work.weixin.qq.com/document/path/99519#50695)让成员进入企业或者正常使用。

登录二次验证如果成员是首次加入企业，企业获取到userid，并验证了成员信息后，调用如下接口即可让成员成功加入企业。

**请求方式：** GET（**HTTPS**）

**请求地址：** https://qyapi.weixin.qq.com/cgi-bin/user/authsucc?access_token=ACCESS_TOKEN&userid=USERID

**参数说明：**

| 参数 | 必须 | 说明 |
| --- | --- | --- |
| access_token | 是 | 调用接口凭证 |
| userid | 是 | 成员UserID。对应管理端的账号 |

使用二次验证：POST（**HTTPS**）

tfa_code五分钟内有效且只能使用一次 （`tfa_code` 通常指的是“Two-Factor Authentication (2FA) Code”，即双因素认证代码。这是一种安全措施，用于在用户登录或进行敏感操作时，除了传统的用户名和密码之外，还需要提供一个额外的认证因素。）

https://developer.work.weixin.qq.com/document/path/99519

企业微信二次登录（SSO）只允许填写域名而不是直接填写登录URL，主要是出于以下几个原因：

1. **安全性**：通过限制只能填写域名，企业微信可以更好地控制和验证应用的安全性。这样可以确保只有经过认证的域名才能参与到SSO流程中，减少中间人攻击等安全风险。
    
    **Security**: By restricting to only domain names, WeChat Work can better control and verify the security of the applications. This ensures that only authenticated domains can participate in the SSO process, reducing security risks.
    
2. **灵活性**：使用域名而不是具体的URL，可以让应用开发者有更多的灵活性来设计自己的登录流程。例如，可以在域名下设置多个路径来处理不同的登录场景。
    
    **Flexibility**: Using domain names instead of specific URLs allows application developers more flexibility in designing their own login processes. For example, multiple paths can be set under the domain name to handle different login scenarios.
    
3. **简化管理**：对于企业微信来说，管理域名比管理具体的URL要简单得多。域名是固定的，而URL可能会因为应用的更新而变化。通过管理域名，可以减少维护成本。
4. **重定向控制**：在SSO流程中，企业微信需要将用户重定向回应用的某个URL。如果只允许填写域名，那么应用开发者可以自由地控制重定向的具体路径和逻辑，比如添加必要的查询参数或进行额外的验证。
5. **兼容性**：不同的应用可能有不同的登录流程和需求。通过只要求填写域名，企业微信可以兼容更多的应用场景，而不需要为每种场景定制特定的URL规则。
6. **避免硬编码**：如果直接填写具体的URL，那么一旦URL发生变化，就需要更新企业微信的配置，这会增加额外的工作量。而使用域名，即使应用内部的URL发生变化，也不会影响到企业微信的配置。
    
    **Avoiding Hardcoding**: If specific URLs are directly filled in, then once the URL changes, the configuration of WeChat Work needs to be updated, which increases additional workload. By using domain names, even if the internal URLs of the application change, it will not affect the configuration of WeChat Work.

### 语音

msgtype: voice 语音消息为amr格式的 （只有这个需要语音转文字）

msgtype: meeting_voice_call 语音通话音频类型为mp3   

msgtype: voiptext 语音通话只有meta data 没有mp3


### 撤回

企微标准的会话留存接口针对撤回的消息获取的信息是一条撤回消息的提示信息，类似 “ 谁什么时间撤回了一条消息” 这种文案。后台api接口里有返回撤回的消息对应的被撤回消息的id。这个id不会因为用户撤回了而删除。

### 添加好友

企业内的员工可以添加外企业的联系人进行工作沟通，外部联系人分为企业微信联系人和微信联系人两种类型。企业微信账号访问是不返回unionid的，若用户添加的外部联系人是企业微信，拿不到unionid

https://developer.work.weixin.qq.com/document/path/96315

https://developer.work.weixin.qq.com/community/question/detail?content_id=16307126230000571017

客户删除成员，客户仍然会存在企业的客户列表。成员删除客户，会将客户从客户列表移除。客户删除企业成员，实际企业库中还会存在好友关系，依旧可以调用获取客户相关接口，属于单向删除，只有服务人员删除客户，这个是完全删除，就是无法再调用相关客户的接口了，可以通过回调进行判断

https://developer.work.weixin.qq.com/document/path/92113

https://developer.work.weixin.qq.com/community/question/detail?content_id=16291843538907183448

### 在职继承

关于腾讯端在职继承和离职继承的权限
1. 只有管理员和客户联系负责人有这个权限，可以在企微app端操作
2. 普通员工没有这个操作继承的权限，有查看管理员或客户联系负责人的继承给他的客户和群。

因此，可以在腾讯后台设置客户联系负责人，由他们做离职继承，在职继承。

### 证书

同一家公司最多可以开通5个企业微信

对话留存在腾讯的wecom里面是需要先有license，先确定谁有这些license。然后才可以做authorization的。

### 发送欢迎语

https://developer.work.weixin.qq.com/document/path/92137


### Conversation Log

https://developer.work.weixin.qq.com/document/path/91774

用sdkfield通过get media files这个API去拿它的二进制的media data，然后转成文件

text message里面只有text，video和voice和picture才会有这个STK field

### 域名配置

企微对域名ICP备案公司和企微认证公司校验，如果不一致的话，需要联系客服确认主体一致

### 文件下载失败
* 10000：请求参数错误	
* 10001：网络请求错误
* 10002：数据解析失败	

单元函数必须实现针对瞬时故障的重试逻辑，具有可配置的重试限制和指数退避策略
