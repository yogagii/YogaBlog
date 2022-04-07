Title: JAVA Grammer
Date: 2022-04-03
Category: Backend
Tags: Java
Author: Yoga

## 变量

```java
int n = 100; // 第一次定义变量n需要指定变量类型int
n = 200; // 重新赋值不能再重复定义
```

### 基本类型：

* 整数类型：byte，short，int，long
* 浮点数类型：float，double
* 字符类型：char
* 布尔类型：boolean

### 引用类型：

* String

toUpperCase, equals, contains, indexOf, lastIndexOf, startsWith, endsWith, substring, trim, strip, isEmpty, isBlank, replace, replaceAll, split, join, format, formatted, valueOf

### 常量：

* final

```java
public class Color {
  public static final String RED = "r";
  public static final String GREEN = "g";
}

if (color == Color.RED) {}
```

### 枚举类:

* enum

```java
enum Weekday {
  SUN, MON, TUE, WED, THU, FRI, SAT;
}

if (day == Weekday.SAT || day == Weekday.SUN) {
  // "Work at home!";
} 
```

### 自动推断变量类型：

* var

### 数组：

```java
int[] ns = new int[5];
int[] ns = new int[] { 68, 79, 91, 85, 62 };
int[] ns = { 68, 79, 91, 85, 62 };
String[] names = { "ABC", "XYZ", "zoo" };
```

数组所有元素初始化为默认值，整型都是0，浮点型是0.0，布尔型是false；

数组一旦创建后，大小就不可改变

```java
for (int i=0; i<ns.length; i++) {}
for (int n : ns) {}
```

* ArrayList 可变长度数组

```java
import java.util.ArrayList;

ArrayList list = new ArrayList();
list.add("Hello");
String first = (String) list.get(0); // 获取到Object，必须强制转型为String
```

---

## 泛型

使用ArrayList时，如果不定义泛型类型时，泛型类型实际上就是Object，定义泛型类型<String>后，List<T>的泛型接口变为强类型List<String>

```java
ArrayList<String> list2 = new ArrayList<String>();
list2.add("Hello");
String first2 = list2.get(0); // 无强制转型
```

先在类中标记所有的特定类型，再把特定类型替换为T

```java
public class Pair<T, K> {
  private T first;
  private K last;
  public Pair(T first, K last) {
    this.first = first;
    this.last = last;
  }
  public T getFirst() { return first; }
  public K getLast() { return last; }
}

Pair<String, Integer> p = new Pair<>("test", 123);
```

泛型类型<T>不能用于静态方法

---

## Collection 集合

* List

一种有序列表的集合

```java
import java.util.ArrayList;
import java.util.List;

List<String> list = new ArrayList<>();
list.add("apple"); // size=1
list.add("apple"); // size=2 允许添加重复的元素
list.add(null); // size=3 允许添加null

String third = list.get(2); // null

List<Integer> list = List.of(1, 2, 5); // 不接受null值

list.contains("apple") // true
list.indexOf("apple") // 0
```

遍历List：

```java
for (int i=0; i<list.size(); i++) {
  String s = list.get(i);
}
for (Iterator<String> it = list.iterator(); it.hasNext(); ) { // 迭代器
  String s = it.next();
}
for (String s : list) {
  System.out.println(s);
}
```

list 转 数组：

```java
Object[] array = list.toArray(); // toArray()方法返回一个Object[]数组，会丢失类型信息
Integer[] array = list.toArray(new Integer[3]); // toArray(T[]) 泛型参数<T>
Integer[] array = list.toArray(new Integer[list.size()]);
```

数组 转 list：

```java
Integer[] array = { 1, 2, 3 };
List<Integer> list = List.of(array);
```

* Map

一种通过键值（key-value）查找的映射表集合，key不能重复

```java
import java.util.HashMap;
import java.util.Map;

Map<String, Integer> map = new HashMap<>();
map.put("apple", 123);
map.get("apple"); // 123
```

遍历Map:

```java
for (String key : map.keySet()) {
  Integer value = map.get(key);
  System.out.println(key + " = " + value);
}
for (Map.Entry<String, Integer> entry : map.entrySet()) {
  String key = entry.getKey();
  Integer value = entry.getValue();
  System.out.println(key + " = " + value);
}
```
HashMap不保证顺序，TreeMap有序，如果作为Key的class没有实现Comparable接口，必须在创建TreeMap时同时指定一个自定义排序算法

```java
import java.util.*;

Map<DayOfWeek, String> map = new EnumMap<>(DayOfWeek.class); // EnumMap查找效率非常高
Map<String, Integer> map = new TreeMap<>(); // SortedMap保证遍历时以Key的顺序来进行排序
Map<Person, Integer> map = new TreeMap<>(new Comparator<Person>() {
  public int compare(Person p1, Person p2) {
    return p1.name.compareTo(p2.name);
  }
});
```

Java默认配置文件以.properties为扩展名，每行以key=value表示

* Set

一种保证没有重复元素的集合

```java
import java.util.*;

Set<String> set = new HashSet<>(); // 无序
set.add("abc");
set.contains("xyz");
set.remove("hello");
set.size();

```

TreeSet有序，实现了SortedSet，添加的元素必须正确实现Comparable接口，如果没有实现Comparable接口，那么创建TreeSet时必须传入一个Comparator对象。

```java
Set<String> set2 = new TreeSet<>();
```

* Queue

是实现了一个先进先出（FIFO：First In First Out）的有序表，List可以在任意位置添加和删除元素，而Queue只有两个操作：

把元素添加到队列末尾；
从队列头部取出元素。

```java
import java.util.LinkedList;
import java.util.Queue;

Queue<String> q = new LinkedList<>();
q.add("apple"); // 添加失败时（可能超过了队列的容量），它会抛出异常
q.offer("pear"); // 当添加失败时，不会抛异常，而是返回false
q.remove(); // apple 空队列调用remove()方法，会抛出异常
q.peek(); // pear 不会删除，可以反复获取
q.poll(); // poll 会删除，获取失败时，它不会抛异常，而是返回null
```
PriorityQueue “VIP插队”的业务，必须给每个元素定义“优先级”

```java
Queue<String> q = new PriorityQueue<>();
```

* Deque 

双端队列: 两头都进，两头都出

| 队列 | Queue | Deque
| - | - | -
| 添加到队尾 | add / offer | addLast / offerLast
| 取删队首 | remove / poll | removeFirst / pollFirst
| 取队首 | element / peek | getFirst / peekFirst / peek
| 添加到队首 | / | addFirst / offerFirst / push
| 取删队尾 | / | removeLast / pollLast / pop
| 取队尾 | / | getLast / peekLast

```java
import java.util.Deque;
import java.util.LinkedList;

Deque<String> deque = new LinkedList<>();
```

* Collections 方法

```java
Collections.sort(list); // 排序
Collections.shuffle(list); // 随机打乱
Collections.unmodifiableList(list); // 把可变集合封装成不可变集合
```