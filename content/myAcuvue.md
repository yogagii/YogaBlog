Title: Some Concept
Date: 2020-04-03
Category: Programming
Tags: proxy
Author: Yoga

## Firebase

mobile version of GA

## APIGEE

## cloudflare

## 反向代理

正向代理代理的对象是客户端，反向代理代理的对象是服务端。
反向代理隐藏了真实的服务端，当我们请求 www.baidu.com 的时候，就像拨打10086一样，背后可能有成千上万台服务器为我们服务，但具体是哪一台，你不知道，也不需要知道，你只需要知道反向代理服务器是谁就好了，www.baidu.com 就是我们的反向代理服务器，反向代理服务器会帮我们把请求转发到真实的服务器那里去。Nginx就是性能非常好的反向代理服务器，用来做负载均衡。

> 正向代理隐藏真实客户端，反向代理隐藏真实服务端

反向代理的实现
1. 需要有一个负载均衡设备来分发用户请求，将用户请求分发到空闲的服务器上
2. 服务器返回自己的服务到负载均衡设备
3. 负载均衡将服务器的服务返回用户

以上的潜台词是：用户和负载均衡设备直接通信，也意味着用户做服务器域名解析时，解析得到的IP其实是负载均衡的IP，而不是服务器的IP，这样有一个好处是，当新加入/移走服务器时，仅仅需要修改负载均衡的服务器列表，而不会影响现有的服务。

链接：https://www.zhihu.com/question/24723688/answer/160252724


## GraphQL

a query language for what you need

ask for what you need

前端直接传query语句给后端，要什么请求什么

## GrapeJS

export MJML 邮件中的HTML

## Data Democratization 数据民主化

Data democratization is the ability for information in a digital format to be accessible to Subject Matter Expert in JSC and data analysts/scientists.

授予员工访问数据的权限，确保信息易于查找、检索和理解。使决策权掌握在员工手中，并为员工提供一些他们所需的信息以辅助他们优化工作。

## EDW 企业数据仓库

The primary function of the Enterprise Data Warehouse, is to provide a centralized data store of J&J enterprise-level data.

## CDL 

The Common Data Layer (CDL) is a repository that centralizes the Supply Chain Data.This common layer can support all digital solutions across the business. The CDL ingests and publishes near real-time data from supply chain systems globally. The Level 0 layer of the CDL is a direct reflection of the data as it is stored in the upstream source systems.

CDL defined Databricks as the tool to use for data consumption. A secure access to CDL is given via an Azure Active Directory (AD) credential passthrough. The access is of type read-only, preventing L2 teams to write/modify any content in CDL L0 and L1. The access is direct to CDL Production environment, even during the development in downstream DEV & QA systems. 
