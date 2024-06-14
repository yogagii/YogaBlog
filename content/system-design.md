Title: System Design
Date: 2024-06-04
Category: Programming
Tags: Architecture
Author: Yoga

https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#step-2-review-the-scalability-article

## High Scalability


Website scaling helps handle growing traffic and user demands while maintaining peak performance.

Website scaling is the process of improving your website’s capacity to accommodate more traffic, data, and user demands effectively. 

高可扩展性（High Scalability）是网站开发中至关重要的一个方面，它涉及设计和优化技术，以确保网站能够处理不断增长的用户数量和数据量，同时保持高性能。

* Horizontal scaling: adding more servers or nodes to a system to distribute your website’s load
* Vertical scaling: improve a single server’s resources — like processor speed, RAM, or storage

Ways to expand to high scalability:

1. Clone-able & Copy-able
  * Stateless user
  * Deployment consistent

2. Load balancing 负载均衡：负载均衡通过将请求分配给多个服务器来分散负载，从而提高网站的响应速度和可靠性。(NGINX and AWS Elastic Load Balancing)

3. Caching 缓存：缓存是提高性能的重要手段。前端可以使用浏览器缓存和CDN，后端可以采用多层次的缓存技术，比如反向代理缓存和数据库缓存。

    Caching stores data in a temporary storage location, or cache, for faster retrieval.

    CDNs (a form of horizontal scaling) store copies of your website and blog content on servers in various geographic regions. When users request content, the nearest CDN server responds, quickly delivering content while minimizing latency.

    Cache what? SQL query & result?

4. Database optimization 数据库优化

  * improve data retrieval speeds: indexing, query optimization, and strategic scaling
  * 使用高效的数据库查询和架构：Denormalization 大宽表
  * NoSQL：考虑使用NoSQL数据库来处理大量的非结构化数据

5. 异步处理：对于长时间运行的任务，可采用异步处理机制，例如消息队列系统（如Kafka），以避免阻塞主要的应用线程。

  * Not computing intensive task
  * Computing intensive task

6. Microservices architecture 分布式系统：采用分布式架构，将不同的功能模块拆分并分布在多个服务器上。比如使用微服务架构，将单一应用程序拆分为多个小的、独立部署的服务。

    A microservices architecture divides your website into smaller, autonomous sections that communicate through application programming interfaces (APIs). This horizontal scaling method allows you to scale individual applications rather than the entire system to make development and updates more agile.
    Tools like Docker manage containerized site segments, while API gateways such as Amazon Web Services and Kong streamline communication between these microservices.


https://webflow.com/blog/website-scaling

