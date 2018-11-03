Title: Make总结
Date: 2018:10:25 14:33
Category: Programming
Tags: make
Author: 张本轩

## Make

Make是常见的构建工具，按照文件中写好的规则进行构建. Make命令放在一个Makefile的文件中，你也可以通过`make -f rules.txt`指定其他文件名.

### Make rules

```javascript
<target>: <prerequisites>
[tab]   <command>
```

一个目标构成一条规则，即可以是文件名也可以是某个操作的名字．
```javascript
clean:
    rm *.o
```
通过调用`make clean`指令来执行上述程序, 为避免歧义．可以加入`.PHONY: clean`声明`clean`是为目标，但不是文件名来执行．`make`指令默认执行第一个目标

前置条件(prerequisites)指定目标是否重新构建的标准，如果前置文件不存在或者更新过，就需要重新构建

命令表示如何更新目标，由一行或多行Shell命令组成．`#`表示注释，`@`关闭回声，允许使用等号自定义变量,变量放在`$()`之间．

暂时之需要这些，如果以后还有需要再更新

## Reference

[make命令教程](http://www.ruanyifeng.com/blog/2015/02/make.html)