Title: Python类总结
Date: 2018-10-21 13:52
Category: Programming
Tags: python
Author: 张本轩

## Class

类是方法和数据的集合，每个类有多个类实例，类实例有各自的属性保持各自的状态，类实例有类方法来修改类状态。

### Namespace and Scope

namespace(命名空间)是变量名到对象的映射，Python中的命名空间包括：the set of built-in names, global names in a module and the local names in a function invocation. 不同命名空间中定义的变量名是没有关系的

By the way, I use the word **attribute** for any name following a dot — for example, in the expression z.real, real is an attribute of the object z.

不同命名空间创建时间和生命周期不同，包含built-in names的命名空间在Python解释器启动时建立，并且永远不会被删除。模块的全局命名空间当模块定义被读入时创建，函数内的命令空间在函数被调用时创建，函数执行结束时销毁。

scope(作用域)是命名空间能被直接访问的部分，包括:

* the innermost scope, which is searched first, contains the local names
* the scopes of any enclosing functions, which are searched starting with the nearest enclosing scope, contains non-local, but also non-global names
* the next-to-last scope contains the current module’s global names
* the outermost scope (searched last) is the namespace containing built-in names

这里要区分*global*, *nonlocal*之间的差异，如果一个变量被声明为*global*,则直接对该变量的所有引用和赋值发生在模块的global names作用域中。如果一个变量被声明为nonlocal, 则表示该变量在嵌套的作用域中。其他情况下，同名变量是只读的，如果对同名变量写入，则为该变量创建一个新的局部变量

```python
def scope_test():
    def do_local():
        spam = "local spam"

    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"

    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"
    do_local()
    print("After local assignment:", spam)
    do_nonlocal()
    print("After nonlocal assignment:", spam)
    do_global()
    print("After global assignment:", spam)

scope_test()
print("In global scope:", spam)
```

输出结果是:
```python
After local assignment: test spam
After nonlocal assignment: nonlocal spam
After global assignment: nonlocal spam
In global scope: global spam
```

### Class definition syntax

```python
class ClassName:
    <statement-1>
    .
    .
    .
    <statement-N>
```

### Class object

类对象支持两种类型的操作:attribute references and instantiation. 
* attribute references通过.运算符实现，obj.attribute
* 实例化通过`x = MyClass()`实现

### Instance object

 The only operations understood by instance objects are attribute references. There are two kinds of valid attribute names, *data attributes* and *methods*.

 ### Class and Instance Variables

 实例变量是各个实例独有的，而类变量是该类的所有实例所共有的

```python
class Dog:

    kind = 'canine'         # class variable shared by all instances

    def __init__(self, name):
        self.name = name    # instance variable unique to each instance

>>> d = Dog('Fido')
>>> e = Dog('Buddy')
>>> d.kind                  # shared by all dogs
'canine'
>>> e.kind                  # shared by all dogs
'canine'
>>> d.name                  # unique to d
'Fido'
>>> e.name                  # unique to e
'Buddy'
```

 ### Inheritance

 ```python
class DerivedClassName(BaseClassName):
    <statement-1>
    .
    .
    .
    <statement-N>
 ```

 There’s nothing special about instantiation of derived classes: DerivedClassName() creates a new instance of the class. Method references are resolved as follows: the corresponding class attribute is searched, descending down the chain of base classes if necessary, and the method reference is valid if this yields a function object.

Derived classes may override methods of their base classes. Because methods have no special privileges when calling other methods of the same object, a method of a base class that calls another method defined in the same base class may end up calling a method of a derived class that overrides it. (For C++ programmers: all methods in Python are effectively virtual.)

An overriding method in a derived class may in fact want to extend rather than simply replace the base class method of the same name. There is a simple way to call the base class method directly: just call BaseClassName.methodname(self, arguments). This is occasionally useful to clients as well. (Note that this only works if the base class is accessible as BaseClassName in the global scope.)

Python has two built-in functions that work with inheritance:

Use isinstance() to check an instance’s type: isinstance(obj, int) will be True only if obj.__class__ is int or some class derived from int.
Use issubclass() to check class inheritance: issubclass(bool, int) is True since bool is a subclass of int. However, issubclass(float, int) is False since float is not a subclass of int.







