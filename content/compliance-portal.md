Title: Compliance Portal
Date: 2024-04-14
Category: Project
Author: Yoga

## Project Overview

### Introduction

* User Portal - Persona Tool: An easy-to-access, comprehensive, and visualized tool to reflect compliance behavior and empower people and line managers to mitigate and improve compliance behavior efficiently and enhance the culture of accountability.

* Admin Portal - Compliance Portal: To build a comprehensive, unified and independent compliance system/platform to integrate multiple systems and modules to ensure compliance program efficiency and effectiveness, incl. but not limited to compliance learning, interactive engagement, dashboard, persona, end-to-end process oversight and consequence management tool, etc.

### Business Value

* For Company: An integrated one-stop compliance portal with comprehensive compliance functions
Health Care Compliance

* For HCC: Improve real-time compliance coaching, oversight and mitigation efficiency.

* For Employees: Access to compliance information; tools to manage self and team's compliance behavior; dashboard to view compliance efforts and inspire employees to be more compliant

## Tech Overview

* ExpressJS
	* Authorization & Authentication
	* Swagger Document
	* Axios
	* File Upload to Azure Blob
* CI/CD
	* Kubernetes
	* Cron Job
* Pen Test
	* Snyk
* Drupal
	* JSON:API
* Knex
	* DB migration

## High Scalability

> Website scaling helps handle growing traffic and user demands while maintaining peak performance.

高可扩展性（High Scalability）是网站开发中至关重要的一个方面，它涉及设计和优化技术，以确保网站能够处理不断增长的用户数量和数据量，同时保持高性能。

1. Load balancing 负载均衡：负载均衡通过将请求分配给多个服务器来分散负载，从而提高网站的响应速度和可靠性。

	在 Kubernetes（K8s）中，负载均衡是指将应用程序的流量分配到多个实例（Pod）上，以提高应用程序的性能和可靠性。通过以下组件实现流量的分发：

	Service：负责在集群内部或外部暴露应用。Service 提供了一种稳定的方式，使用统一的 IP 地址和端口访问不同节点上的 Pod，无需关心 Pod 的实际 IP 地址。

	ReplicaSet：确保应用的指定数量的 Pod 一直处于运行状态。ReplicaSet 可以动态调整 Pod 的数量，以应对负载的变化。

	Ingress 是一种管理集群内部服务外部访问的 API 对象，主要用于 HTTP 和 HTTPS 路由。它的工作机制类似于 Nginx 或其他反向代理服务器，通过定义规则将外部流量重定向到集群内的服务


2. Caching 缓存：缓存是提高性能的重要手段。前端可以使用浏览器缓存和CDN，后端可以采用多层次的缓存技术，比如反向代理缓存和数据库缓存。

Caching stores data in a temporary storage location, or cache, for faster retrieval.

CDNs (a form of horizontal scaling) store copies of your website and blog content on servers in various geographic regions. When users request content, the nearest CDN server responds, quickly delivering content while minimizing latency.

3. Database optimization 数据库优化：使用高效的数据库查询和架构，并考虑使用NoSQL数据库来处理大量的非结构化数据。improve data retrieval speeds: indexing, query optimization, and strategic scaling

4. 异步处理：对于长时间运行的任务，可采用异步处理机制，例如消息队列系统（如Kafka），以避免阻塞主要的应用线程。


5. Microservices architecture 分布式系统：采用分布式架构，将不同的功能模块拆分并分布在多个服务器上。比如使用微服务架构，将单一应用程序拆分为多个小的、独立部署的服务。

A microservices architecture divides your website into smaller, autonomous sections that communicate through application programming interfaces (APIs). This horizontal scaling method allows you to scale individual applications rather than the entire system to make development and updates more agile.
Tools like Docker manage containerized site segments, while API gateways such as Amazon Web Services and Kong streamline communication between these microservices.



