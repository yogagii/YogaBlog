Title: JAVA Logging - SLF4J
Date: 2025-02-05
Category: Backend
Tags: Java
Author: Yoga

Java log发展历史：
* System.out.println
* java.until.logging (JDK1.4)
* log4j: Ceki Gülcü将Log4j捐献给了Apache
* LogBack: Ceki Gülcü出走后另起炉灶，开发出LogBack，受到LogBack的冲击，2015年9月Apache软件基金业宣布Log4j不再维护
* Log4J2是Apache开发的一个新的日志框架，改进了很多Log4J的缺点，同时也借鉴了LogBack，在多线程场景中，异步记录器的吞吐量比 Log4j 1.x 和 Logback 高 18 倍，延迟更低

### SLF4J 

> SLF4J (Simple Logging Facade for Java) 简单日志门面

SLF4J 是一个日志框架的抽象层，提供了一个简单的、统一的接口，用于在 Java 应用程序中进行日志记录。它不是具体的日志实现，而是一个桥梁，可以与多种流行的日志库（如 Logback、Log4j、java.util.logging 等）集成使用。使用日志门面引入日志组件的最大优势是：将系统和具体的日志实现框架解耦合。

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
Logger logger = LoggerFactory.getLogger(Test.class);
logger.info("Hello World!")
```

### Log4J2

Log4J2 可以通过异步 Appender 实现非阻塞的日志记录，可以显著提高日志记录的性能，尤其是在高负载情况下。Log4J2 支持许多新的特性，包括更灵活的配置方式（支持 XML、JSON 和 YAML 格式），并且可以通过插件系统轻松扩展功能。

pom.xml
```xml
<!-- 使用 spring-boot-starter 会引入 Logback 作为默认日志框架，要去掉这个依赖 -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter</artifactId>
  <exclusions>
    <exclusion>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-logging</artifactId>
    </exclusion>
  </exclusions>
</dependency>
<!-- 不需要单独添加 log4j-core、log4j-api 和 log4j-slf4j-impl 的依赖，因为它们会通过 spring-boot-starter-log4j2 自动引入 -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-log4j2</artifactId>
</dependency>
<!-- log4j-layout-template-json 不是 spring-boot-starter-log4j2 的默认依赖，需要手动添加它 -->
<dependency>
  <groupId>org.apache.logging.log4j</groupId>
  <artifactId>log4j-layout-template-json</artifactId>
</dependency>
```

### MDC 

Mapped Diagnostic Context (MDC) 是一个用于在日志中添加上下文信息的工具，它属于 SLF4J（Simple Logging Facade for Java）的一部分。MDC 允许你将一组键值对存储在当前线程的上下文中，这些键值对可以被日志框架访问并记录到日志中。

Key Features
* Thread-Local Storage 线程局部存储：MDC 使用线程局部变量（ThreadLocal）来存储上下文信息，这意味着每个线程都有自己的独立上下文，不会相互干扰。
* Dynamic Context Information 动态上下文信息：你可以根据需要动态地添加、修改或删除上下文信息，这些信息会随着日志输出而记录下来。
* Logging Framework Support 日志框架支持：大多数现代日志框架（如 Log4j2、Logback）都支持 MDC，并且可以通过配置文件来控制如何将 MDC 中的信息输出到日志中。

Use Cases
* Distributed Tracing 分布式追踪：在微服务架构中，MDC 常用于存储追踪 ID（如 CorrelationId），以便在多个服务之间追踪请求的路径。
* User Session Information 用户会话信息：在 Web 应用中，MDC 可以存储用户会话信息（如用户 ID、角色等），便于在日志中记录用户行为。
* Transaction Information 事务信息：在处理事务时，MDC 可以存储事务 ID，方便追踪事务的执行路径。

###  CorrelationId 

CorrelationId 是一个用于追踪请求的唯一标识符，通常在分布式系统中使用。它的主要作用是将一个请求在多个服务或组件之间的调用链路关联起来，便于调试和监控。

* 唯一性：每个请求都有一个唯一的 CorrelationId，通常使用 UUID（Universally Unique Identifier）生成。
* 传递性：CorrelationId 会随着请求在系统中的流转而传递，确保在不同服务或组件中可以识别同一个请求。在微服务架构中，CorrelationId 用于追踪一个请求在多个服务之间的调用路径，帮助开发者快速定位问题。
* 日志记录：CorrelationId 通常会被记录在日志中，便于在出现问题时快速定位请求的路径。通过 CorrelationId，可以将分散在不同服务中的日志关联起来，便于分析和调试。
* 性能监控：在性能监控工具中，CorrelationId 可以帮助追踪请求的处理时间和瓶颈。

### Configuring Log4j2

1.To configure Log4j2 to output logs in this format, use a JSON template layout. 

log4j2.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN">
    <Appenders>
        <Console name="Console" target="SYSTEM_OUT">
          <!-- %X{CorrelationId} is used to retrieve the CorrelationId from the MDC context -->
          <!-- <PatternLayout pattern="%d{yyyy-MM-dd HH:mm:ss} [%t] %-5level %logger{36} - %X{CorrelationId} - %msg%n"/> -->
            <JsonTemplateLayout eventTemplateUri="classpath:log4j2-layout.json"/>
        </Console>
        <File name="MyFile" fileName="logs/app.log">
            <JsonTemplateLayout eventTemplateUri="classpath:log4j2-layout.json"/>
        </File>
    </Appenders>
    <Loggers>
        <Root level="info">
            <AppenderRef ref="Console"/>
            <AppenderRef ref="MyFile"/>
        </Root>
    </Loggers>
</Configuration>
```

2.Create a JSON template file named log4j2-layout.json in the src/main/resources directory:

log4j2-layout.json
```json
{
  "timestamp": {
    "$resolver": "timestamp"
  },
  "level": {
    "$resolver": "level",
    "field": "name"
  },
  "logger": {
    "$resolver": "logger",
    "field": "name"
  },
  "message": {
    "$resolver": "message",
    "stringified": true
  },
  "correlationId": {
    "$resolver": "mdc",
    "key": "CorrelationId"
  },
  "userId": {
    "$resolver": "mdc",
    "key": "UserId"
  },
  "userRole": {
    "$resolver": "mdc",
    "key": "UserRole"
  },
  "errorType": {
    "$resolver": "exception",
    "field": "className"
  },
  "errorMessage": {
    "$resolver": "exception",
    "field": "message"
  },
  "errorStackTrace": {
    "$resolver": "exception",
    "field": "stackTrace",
    "stackTrace": {
      "stringified": true
    }
  }
}
```

3.Create a custom HandlerInterceptor that generates a CorrelationId and sets it in the MDC.

HandlerInterceptor 是 Spring MVC 提供的一个接口，用于在请求处理过程中拦截请求。它主要与 Spring 的 DispatcherServlet 配合使用，适用于基于 Spring MVC 的 Web 应用程序。

主要方法：
* preHandle：在请求处理之前被调用。可以用于验证请求、解析请求参数、设置请求上下文等。如果返回 false，则中断请求处理，不再调用后续的拦截器和控制器方法。
* postHandle：在请求处理之后、视图渲染之前被调用。可以用于修改模型和视图、添加额外的属性等。
* afterCompletion：在请求处理完成之后被调用，无论请求处理是否成功。可以用于清理资源、记录日志等。

```java
import org.slf4j.MDC;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.servlet.HandlerInterceptor;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.util.UUID;
 
public class CorrelationIdInterceptor implements HandlerInterceptor {
 
    private static final Logger log = LoggerFactory.getLogger(CorrelationIdInterceptor.class);
 
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        // Generate a new CorrelationId if not already present in the request
        String correlationId = request.getHeader("CorrelationId");
        if (correlationId == null || correlationId.isEmpty()) {
            correlationId = UUID.randomUUID().toString();
        }
 
        // Set the CorrelationId in the MDC
        MDC.put("CorrelationId", correlationId);
 
        // Omit the steps for obtaining the userId and userRole.
 
        // Optionally, set the CorrelationId in the response header
        response.setHeader("CorrelationId", correlationId);
 
        if (log.isDebugEnabled()) {
            log.debug("CorrelationId set to: {}", correlationId);
        }
 
        return true;
    }
 
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
        // Remove the CorrelationId from the MDC to avoid memory leaks
        MDC.remove("CorrelationId");
 
        if (log.isDebugEnabled()) {
            log.debug("CorrelationId removed from MDC");
        }
    }
}
```

Filter 是 Java Servlet API 提供的一个接口，用于在请求到达 Servlet 之前或响应返回客户端之前对请求和响应进行预处理或后处理。它是一个更通用的机制，适用于所有基于 Servlet 的 Web 应用程序。

主要方法：
* init：在 Filter 被初始化时调用，用于初始化 Filter。
* doFilter：在请求处理之前被调用。可以用于修改请求、响应，执行安全检查等。必须调用 chain.doFilter(request, response) 将请求传递给下一个 Filter 或目标 Servlet。
* destroy()：在 Filter 被销毁时调用，用于清理资源。

```java
import org.slf4j.MDC;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.util.UUID;

public class CorrelationIdFilter implements Filter {

    private static final Logger logger = LoggerFactory.getLogger(CorrelationIdFilter.class);

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        // Initialization code if needed
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        try {
            HttpServletRequest httpRequest = (HttpServletRequest) request;
            String correlationId = getCorrelationId(httpRequest);
            MDC.put("CorrelationId", correlationId);
            chain.doFilter(request, response);
        } finally {
            MDC.remove("CorrelationId");
        }
    }

    private String getCorrelationId(HttpServletRequest request) {
        HttpSession session = request.getSession();
        String correlationId = (String) session.getAttribute("CorrelationId");
        if (correlationId == null) {
            correlationId = UUID.randomUUID().toString();
            session.setAttribute("CorrelationId", correlationId);
        }
        return correlationId;
    }

    @Override
    public void destroy() {
        // Cleanup code if needed
    }
}
```

4.Register the CorrelationIdInterceptor by adding it to the WebMvcConfigurer.

WebMvcConfigurer.java
```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
 
@Configuration
public class WebConfig implements WebMvcConfigurer {
 
    @Autowired
    private CorrelationIdInterceptor correlationIdInterceptor;
 
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(correlationIdInterceptor);
    }
}
```
若使用filter, Register the Filter Using FilterRegistrationBean or web.xml.

5.使用

直接用
```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

Logger logger = LoggerFactory.getLogger(Test.class);
logger.info("Hello World!")
```
或者 @Slf4j 是 Lombok 提供的一个注解，用于在类中生成 SLF4J Logger 的实例，这样你就不需要手动编写 logger 的常规代码。

```java
java
import lombok.extern.slf4j.Slf4j;

@Slf4j // 使用 @Slf4j 注解
public class MyController {

  @GetMapping("/hello")
  public String hello() {
      log.info("Hello endpoint was called");
      return "Hello, World!";
  }
}
```
