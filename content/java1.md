Title: JAVA Install
Date: 2022-03-30
Category: Backend
Tags: Java
Author: Yoga

```java
// Hello.java 
public class Hello { // 类名首字母大写
  public static void main(String[] args) { // Java程序的固定入口方法
    System.out.println("Hello, world!"); // 输出并换行
    System.out.print("A"); // 不换行
    for (String arg : args) { // java App arg1 arg2
      System.out.println("arg: " + arg); // arg: arg1  arg: arg2
    }
  }
}
```
_一个Java源码只能定义一个public类型的class，并且class名称和文件名要完全一致_

* 创建：

cmd+shift+p -> Java: Create Java Project

* 运行：

```bash
javac Hello.java # 用javac把Hello.java编译成字节码文件Hello.class
java Hello # Hello.class

# Java 11可以直接运行一个单文件源码
java Hello.java
```

* classpath

```bash
java -cp . com.example.Hello # classpath缩写cp，默认当前目录.
```

* jar

jar包相当于目录，可以包含很多.class文件

jar包实际上就是一个zip格式的压缩文件，bin目录右键压缩成zip，把后缀改为jar

```bash
java -jar hello.jar
```

---

## 启动spring

* 检查安装java

判断自己的mac是macOS x64 还是 macOS ARM64

```bash
uname -a 
# Darwin WITSXRQVHQWK75 23.6.0 Darwin Kernel Version 23.6.0: Mon Jul 29 21:14:30 PDT 2024; root:xnu-10063.141.2~1/RELEASE_ARM64_T6000 arm64
```

https://www.oracle.com/java/technologies/downloads/?er=221886#jdk22-mac

下载 jdk-22_macos-aarch64_bin.dmg 双击安装

```bash
java -version
# java version "9.0.1"
```

* 检查安装maven

https://maven.apache.org/download.cgi 下载 apache-maven-3.8.8-bin.zip，解压并放入user目录下

```bash
vim ~/.zshrc

# maven
export MAVEN_HOME=/Users/jyu/apache-maven-3.8.8
export PATH=$PATH:$MAVEN_HOME/bin

source ~/.zshrc
mvn -v
```

踩坑： No compiler is provided in this environment. Perhaps you are running on a JRE rather than a JDK?

```bash
mvn -v
# Java version: 9.0.1, vendor: Oracle Corporation, runtime: /Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home

/usr/libexec/java_home -V # 找到本地 Java 的jdk安装目录
# 9.0.1 (x86_64) "Oracle Corporation" - "Java SE 9.0.1" /Library/Java/JavaVirtualMachines/jdk-9.0.1.jdk/Contents/Home

# /Users/jyu/apache-maven-3.8.8/bin
vim mvn
# 顶部添加
JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-9.0.1.jdk/Contents/Home

mvn -v
# Java version: 9.0.1, vendor: Oracle Corporation, runtime: /Library/Java/JavaVirtualMachines/jdk-9.0.1.jdk/Contents/Home
```

换源

vi /Users/jyu/apache-maven-3.8.8/conf/settings.xml

```xml
<mirror>
  <id>xxx-public-repository-group</id>
  <mirrorOf>central</mirrorOf>
  <name>xxx Public Repository Group</name>
  <url>http://repository.xxx.org/nexus/content/groups/public</url>
</mirror>
```

  setting.xml是Maven的全局配置文件，通常位于Maven安装目录下的conf文件夹中。它包含了Maven运行时需要用到的各种配置信息，例如本地仓库的位置、服务器的配置、邮件通知的配置等。

  pom.xml是Maven项目的项目配置文件，通常位于项目的根目录下。它包含了项目的各种信息，如项目坐标、依赖关系、开发者规则、缺陷管理系统、组织和许可证等。

* 安装依赖

进入项目目录

```bash
mvn install
mvn clean install # 先清理项目的工作目录，删除之前构建过程中生成的所有文件（如编译后的类文件、JAR 文件等），确保新的构建是从干净的状态开始的
mvn clean install -Dmaven.wagon.http.ssl.insecure=true -Dmaven.wagon.http.ssl.allowall=true # 跳过证书检查
mvn clean install -DskipTests # 跳过单元测试
```

* 运行项目

```bash
mvn spring-boot:run
```

---

## 配置文件

* properties 格式：key=value

```yml
# application.properties

spring.application.name=${APP_NAME:unnamed}
```

* YAML是一种层级格式，去掉了大量重复的前缀，并且更加易读

```yml
# application.yml

spring:
  application:
    name: ${APP_NAME:unnamed}
```

${DB_HOST:localhost}意思是，首先从环境变量查找DB_HOST，如果环境变量定义了，那么使用环境变量的值，否则，使用默认值localhost

