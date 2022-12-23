Title: JAVA Object Oriented
Date: 2022-04-04
Category: Backend
Tags: Java
Author: Yoga

## 面向对象

```java
class Person {
  public String name;
  private int age; // private修饰field拒绝外部访问
  private String[] hobbies;

  public int getAge() {
    return this.age;
    return age; // 没有命名冲突，可以省略this
  }

  public void setAge(int age) {
    this.age = age; // 局部变量优先级更高，就必须加上this
  }

  public void setHobbies(String... hobbies) { // 可变参数相当于数组
    this.hobbies = hobbies;
  }
  public void setHobbies2(String[] hobbies) { 
    this.hobbies = hobbies;
  }
}

public class Main {
  public static void main(String[] args) {
    Person ming = new Person(); // 一个类没有定义构造方法，编译器会自动生成一个默认构造方法
    ming.name = "Xiao Ming"; // 设置name

    ming.setAge(12); // 设置age
    System.out.println(ming.getName() + ", " + ming.getAge());

    g.setHobbies("Singing", "Sleeping", "Eating");
    String[] hobbies = new String[] { "Singing", "Sleeping", "Eating" };
    g.setHobbies2(hobbies); // 调用方需要先构造String[]
    hobbies[0] = "Dancing"; // 引用类型参数的传递指向的是同一个对象 ming.hobbies[0] = "Dancing"
  }
}
```

## 构造方法
```java
class Person {
  private String name = "Unamed"; // 引用类型的字段默认是null
  private int age = 10; // int类型默认值是0

  public Person(String name, int age) { // 构造方法的名称就是类名, 构造方法没有返回值，调用构造方法必须用new
    this.name = name;
    this.age = age;
  }

  public Person(String name) {
    this(name, 18); // 调用另一个构造方法Person(String, int)
  }
}

public class Main {
  public static void main(String[] args) {
    Person p = new Person("Xiao Ming", 15); // 自动匹配到构造方法public Person(String, int)
    Person p = new Person("Xiao Ming"); // 自动匹配到构造方法public Person(String)
  }
}
```

## 方法重载 Overload

方法名相同，但各自的参数不同，返回值类型通常都是相同的

## 继承 extends

```java
class Person {
    protected String name;
    protected int age;

    public Person(String name, int age) {
      this.name = name;
      this.age = age;
    }
}

class Student extends Person {
  private int score;
 
  public Student(String name, int age, int score) { // 子类不会继承任何父类的构造方法
    // super(); 如果没有明确地调用父类的构造方法，编译器会自动加一句super();自动调用父类的构造方法，但是Person类并没有无参数的构造方法
    super(name, age); // 任何class的构造方法，第一行语句必须是调用父类的构造方法。
    this.score = score;
  }

  public String hello() {
    return "Hello, " + super.name; // super关键字表示父类，等于this.name, name
  }
}
```

一个class只允许继承自一个类，一个类有且仅有一个父类，只有Object特殊没有父类。

子类无法访问父类的private字段和private方法，用protected修饰的字段可以被子类访问

## 覆写 Override

子类定义了一个与父类方法签名相同，并且返回值也相同的方法

```java
class Student extends Person {
  @Override // 加上@Override可以让编译器帮助检查是否进行了正确的覆写
  public void run() {}
}
```

父类中用final修饰的方法不能被Override

## 多态

针对某个类型的方法调用，其真正执行的方法取决于运行时期实际类型的方法。

多态的特性：运行期才能动态决定调用的子类方法。对某个类型调用某个方法，执行的实际方法可能是某个子类的覆写方法。

多态的功能：允许添加更多类型的子类实现功能扩展，却不需要修改基于父类的代码。

```java
// 三种纳税方式
class Income {
  protected double income;
  public double getTax() { return income * 0.1; }
}

class Salary extends Income {
  @Override
  public double getTax() { return (income - 5000) * 0.2; }
}

class SpecialAllowance extends Income {
  @Override
  public double getTax() { return 0; }
}

// totalTax()方法只需要和Income打交道，它完全不需要知道Salary和SpecialAllowance的存在，就可以正确计算出总的税。
public double totalTax(Income... incomes) {
  double total = 0;
  for (Income income: incomes) {
      total = total + income.getTax();
  }
  return total;
}
```

## 抽象类

```java
abstract class Person {
  public abstract void run(); // 抽象方法
}
```

抽象方法：如果父类的方法本身不需要实现任何功能，仅仅是为了定义方法签名，目的是让子类去覆写它。抽象方法本身没有实现任何方法语句，所以方法本身是无法执行的

抽象类：包含抽象方法的类无法被实例化。必须把类本身也声明为abstract才能编译，抽象类可以强迫子类实现其定义的抽象方法，抽象方法实际上相当于定义了“规范”。

```java
class Student extends Person {
  @Override
  public void run() {
    System.out.println("Student.run");
  }
}
```

面向抽象编程：尽量引用高层类型，避免引用实际子类型的方式。

上层代码只定义规范，不需要子类就可以实现业务逻辑（正常编译），具体的业务逻辑由不同的子类实现，调用者并不关心。

## 接口

```java
interface Person {
  int MALE = 1; // public static final int MALE = 1;
  int FEMALE = 2;

  String getName(); // public abstract String getName();
}
```

接口：一个抽象类没有字段，所有方法全部都是抽象方法（方法默认都是public abstract），连字段都不能有（可以有静态字段public static final）

```java
class Student implements Person {
  private String name;

  public Student(String name) {
    this.name = name;
  }

  @Override
  public String getName() {
    return this.name;
  }
}
```

一个类只能继承自另一个类，不能从多个类继承。但是，一个类可以实现多个interface

```java
class Student implements Person, Hello {}
```

一个interface可以继承自另一个interface

```java
interface Person extends Hello {}
```

在接口中，可以定义default方法：当我们需要给接口新增一个方法时，会涉及到修改全部子类。如果新增的是default方法，那么子类就不必全部修改，只需要在需要覆写的地方去覆写新增方法。

```java
interface Person {
  String getName();
  default void run() {
      System.out.println(getName() + " run");
  }
}
```

## 静态字段

```java
class Person {
  public int age;
  public static int number; // 定义静态字段number
}

person1.age = 10;
person2.age = 20; // 各个实例的同名字段互不影响
person1.number = 99; // 所有实例都会共享静态字段 person2.number = person1.number = 99
```
可以把静态字段理解为描述class本身的字段（非实例字段）Person.number

## 静态方法

静态方法属于class而不属于实例，因此，静态方法内部，无法访问this变量，也无法访问实例字段，它只能访问静态字段。调用静态方法则不需要实例变量，通过类名就可以调用。

静态方法经常用于工具类：

Arrays.sort()

Math.random()

## 包 package

在定义class的时候，我们需要在第一行声明这个class属于哪个包，来解决类名冲突

```java
package com.xxx.jcrd;

public class JcrdApplication {
  public static void main(String[] args) {
    SpringApplication.run(JcrdApplication.class, args);
  }
}
```

位于同一个包的类，可以访问包作用域的字段和方法。

引用其他包的类：

```java
package a;
public class Person {}

package b;
// 法一：用完整类名
a.Person p1 = new a.Person();
// 法二：import
import a.Person; // 或import a.*;
Person p1 = new Person();
```

包作用域是指一个类允许访问同一个package的没有public、private修饰的class，以及没有public、protected、private修饰的字段和方法。

