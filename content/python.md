Title: Python 基础
Date: 2022-11-22
Category: Programming
Tag: Python, ETL
Author: Yoga

## List 列表

```python
list1 = ['red', 'green', 'blue']

list1[0] # red
list1[-1] # blue 反向索引
list1[0:2] # red, green [0, 2)
```

* 更新列表项

```python
list1[2] = 2001 # 修改
list1.append('newItem') # append 添加
del list1[2] # del 删除
```

* 操作
```python
len([1, 2, 3]) # 3 长度

[1, 2, 3] + [4, 5, 6] # 拼接
list1 += [4, 5, 6] # 拼接

for x in [1, 2, 3]: print(x, end=" ") # 遍历

max([1, 2, 3]) # 最大值
min([1, 2, 3]) # 最小值

list(seq) # 将元组转换为列表
```

* 方法

```python
list1.append(obj) # push
list1.count(obj) # 统计某个元素在列表中出现的次数
list1.index(obj) # indexof
list1.insert(index, obj) # 将对象插入列表
list1.pop(obj) # 移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
list1.remove(obj) # 移除列表中某个值的第一个匹配项
list1.reverse() # 反向
list1.sort( key=None, reverse=False) # 排序
list1.clear() # 清空
list1.copy() # 复制
```

## String 字符串

```python
str1 = 'Hello World'

str1[0] # H
str1[-1] # d
str1[1:4] # ell [1, 4)
```

* 更新字符串
```python
str1[:6] + 'Runoob!'
```

* 转义字符
```python
print("line1 \
  line2") # \续行符 line1 line2
print("Hello \b World!") # \b 退格 Hello World!
print("\n") # \n 换行	
print (r'\n') # 原始字符串

para_str = """python三引号允许一个字符串跨多行，
字符串中可以包含换行符、制表符以及其他特殊字符。
"""
```

* 字符串格式化

符号 | desc |
|-|-|
%c | 格式化字符及其ASCII码 |
%s | 格式化字符串 |
%d | 格式化整数 |
%u | 格式化无符号整型 |

```python
print ("我叫 %s 今年 %d 岁!" % ('Yoga', 10)) # 我叫 Yoga 今年 10 岁!

print('Hello %s' % name)
print(f'Hello {name}') # f-string 字面量格式化字符串 python3.6
```

* 查找
```python
'H' in str1 # True
'H' not in str1 # False
```

* 操作
```python
capitalize() # 首字母大写
```