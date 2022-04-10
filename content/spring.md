Title: Spring
Date: 2022-04-09
Category: Backend
Tags: Java
Author: Yoga

## Spring

Spring的核心就是提供了一个IoC容器，它可以管理所有轻量级的JavaBean组件，提供的底层服务包括组件的生命周期管理、配置和组装服务、AOP支持，以及建立在AOP基础上的声明式事务服务等。

### IoC 容器

IoC: Inversion of Control控制反转

https://yogagii.github.io/typescript.html

```java
public class BookService {
  private DataSource dataSource = new HikariDataSource(config);
}
```
缺点：
1. 一个组件如果要使用另一个组件，必须先知道如何正确地创建它。
2. 没有必要让BookService和UserService分别创建DataSource实例，完全可以共享同一个DataSource
3. 很多组件需要销毁以便释放资源
4. 测试某个组件须要在真实的数据库环境下执行

```java
public class BookService {
  private DataSource dataSource;

  public void setDataSource(DataSource dataSource) {
    this.dataSource = dataSource;
  }
}
```

不直接new一个DataSource，而是注入一个DataSource

优点：
1. BookService不再关心如何创建DataSource，不必读取数据库配置
2. 共享一个组件：DataSource实例被注入到BookService和UserService
3. 测试BookService更容易，因为注入的是DataSource，可以使用内存数据库，而不是真实的MySQL配置。

在IoC模式下，控制权发生了反转，即从应用程序转移到了IoC容器，所有组件不再由应用程序自己创建和配置，而是由IoC容器负责，将组件的创建+配置与组件的使用相分离，并且，由IoC容器负责管理组件的生命周期。

```xml
<beans>
    <bean id="dataSource" class="HikariDataSource" />
    <bean id="bookService" class="BookService">
        <property name="dataSource" ref="dataSource" />
    </bean>
    <bean id="userService" class="UserService">
        <property name="dataSource" ref="dataSource" />
    </bean>
</beans>
```
上述XML配置文件指示IoC容器创建3个JavaBean组件，并把id为dataSource的组件通过属性dataSource（即调用setDataSource()方法）注入到另外两个组件中。

由Spring IoC容器管理的对象叫做beans。 bean就是由Spring IoC容器实例化、组装和以其他方式管理的对象

---

## Spring Boot

Spring Boot是Spring框架的扩展，它消除了设置Spring应用程序所需的XML配置。

1. Spring Boot是Spring框架的扩展，创建独立的Spring应用
2. 嵌入式Tomcat、Jetty、 Undertow容器（无需部署war文件）
3. 消除了设置Spring应用程序所需的XML配置

### 基础结构

* src
  * main
    * java 程序开发以及主程序入口
    * resources 配置文件
  * test
    * java 测试程序

### 根目录结构

* com.example.myproject
  * Application.java 框架配置
  * controller 页面访问控制
    * CustomerController.java
  * service 业务类代码
    * CustomerService.java
  * model 实体（Entity）
    * Customer.java
  * dao (Data Acess Object) 数据访问对象（Repository）
    * CustomerRepository.java
  * config
    * SwaggerConfig.java
  * dto (Data Transfer Objec) 数据传输对象 
  * vo (View Object) 视图对象

## Controller

```java
@RestController
public class HelloWorldController {
  @RequestMapping("/hello")
  public String index() {
    return "Hello World";
  }
}
```

### 特殊注解
* @SpringBootApplication 核心注解，开启自动配置
* @EnableCaching 开启缓存
* @Controller 定义控制器类
* @RestController 默认里面的方法都以json格式输出
* @RequestMapping

## Service

* @Service 用于修饰service层的组件


## Model

```java
@Entity
public class User implements Serializable {
	@Id
	@GeneratedValue
	private Long id;
	@Column(nullable = false, unique = true)
	private String userName;
	@Column(nullable = false)
	private String passWord;

  public String getUserName() {
    return userName;
  }
}
```
Entity 中不映射成列的字段得加 @Transient 注解

## Dao

1.JpaRepository

* @Repository 确保DAO或者repositories提供异常转译

dao 只要继承 JpaRepository 类就可以，几乎可以不用写方法，还可以根据方法名来自动的生成 SQL，比如 findAlll 自动会查询表里面的所有数据

```java
public interface UserRepository extends JpaRepository<User, Long> {
  User findByUserName(String userName);
  User findByUserNameOrEmail(String username, String email);
}
```

2.Mybatis

* @Mapper 添加了@Mapper注解之后这个接口在编译时会生成相应的实现类

法一：
```xml
<!--  main/resources/mapper/UserMapper.xml -->
<mapper namespace="com.jnj.jcrd.dao.UserMapper" >
  <resultMap id="BaseResultMap" type="com.jnj.jcrd.model.User" >
    <id column="id" property="id" jdbcType="INTEGER" />
    <result column="wwid" property="wwid" jdbcType="VARCHAR" />
    <result column="first_name" property="firstName" jdbcType="NVARCHAR" />
  </resultMap>
  <select id="selectAll" resultMap="BaseResultMap">
    select
    <include refid="Base_Column_List" />
    from sys_user
  </select>
</mapper>
```
```java
// main/java/.../dao/UserMapper.java
package com.jnj.jcrd.dao;

import com.jnj.jcrd.model.User;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface UserMapper {
  List<UserEntity> selectAll();
}
```

法二：
```java
public interface UserMapper {
  @Select("SELECT * FROM users")
  @Results({
      @Result(property = "wwid",  column = "wwid"),
      @Result(property = "first_name", column = "first_name")
  })
  List<UserEntity> selectAll();
}
```

## Config

* @Bean 等价于XML中配置的bean


## Resources

application.properties


log配置
```yaml
logging.path=/user/local/log
logging.level.com.favorites=DEBUG
logging.level.org.springframework.web=INFO
logging.level.org.hibernate=ERROR
```

数据库配置

```yaml
spring.datasource.url=jdbc:mysql://localhost:3306/test
spring.datasource.username=root
spring.datasource.password=root
spring.datasource.driver-class-name=com.mysql.jdbc.Driver
```

Redis
```yaml
spring.redis.database=0  
# Redis服务器地址
spring.redis.host=localhost
# Redis服务器连接端口
spring.redis.port=6379  
# Redis服务器连接密码（默认为空）
spring.redis.password=
```

托管到缓存中来共享 Session: 默认采用外置的 Redis 来存储 Session 数据