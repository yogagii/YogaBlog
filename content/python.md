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

* filter
```python
def testFilter(x):
  return x%2  #x是否能被2整除

print(list(filter(testFilter,range(1,10)))) # [1, 3, 5, 7, 9]
```

* map
```python
def testMap(x):
  return x+1

print(list(map(testMap,range(1,5)))) # [2, 3, 4, 5]
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

str1.count(sub, beg= 0,end=len(string)) # sub在 str1 出现的次数
str1.find(sub, beg=0, end=len(string)) # 返回索引值或-1
str1.rfind(sub, beg=0, end=len(string)) # 从右开始找
str1.index(sub, beg=0, end=len(string)) # sub不存在会报异常
str1.rindex(sub, beg=0, end=len(string)) # 从右开始找
```

* 替换
```python
str2 = str1.replace(old, new, max) # old 换成 new，替换不超过 max 次, 返回一个新的字符串，

trantab = str.maketrans("aeiou", "12345")   # 字符串映射表
str1 = "this is string example....wow!!!"
str1.translate(trantab) # 翻译
```

* 操作
```python
len(str1) # 长度
max(str1) # W
min(str1) # e
```

* 方法

```python
str1.capitalize() # 首字母大写
str1.islower() # 小写
str1.isupper() # 大写
str1.lower() # 转小写
str1.upper() # 转大写
str1.wapcase() # 大小写互转
str1.title() # 所有单词首字母大写

str1.isalnum() # 字母或数字
str1.isalpha() # 字母或中文
str1.isdigit() # 数字 123
str1.isnumeric() # 数字字符 "123"
str1.isdecimal() # 十进制字符
str1.isspace() # 空白
str1.endwith(sub)
str1.startwith(sub)

str1.split(str="", num=string.count(str))
str1.join(seq) # 拼接 H-E-L-L-O

str1.strip(sub) # 截掉 空格 或 sub
str1.rstrip(sub) # 截掉 右空格 或 sub
str1.rstrip(sub) # 截掉 右空格 或 sub

str1.encode(encoding='UTF-8',errors='strict') # 编码
bytes.decode(encoding="utf-8", errors="strict") # 解码
str1.expandtabs(tabsize=8) # tab 转空格 
```

* 正则

```python
import re

if (re.match('Actual_sales_2[01][0-9][0-9][0-9][0-9].xlsx', 'Actual_sales_202303.xlsx')):
  print('File exist')
```

## Date 日期

```python
import datetime

utc=datetime.datetime.utcnow() # UTC = datetime.datetime.today()
utc8=datetime.datetime.today()+datetime.timedelta(hours=8) # UTC8 北京时间
today=utc8.strftime("%Y-%m-%d") # 2023-02-16
weekday=utc8.strftime("%w") # '4' (周日0 ~ 周六6)
yesterday=utc8 - datetime.timedelta(days=1) # 昨天
lastMonday=(utc8 - datetime.timedelta(days = utc8.weekday() + 7)).strftime("%Y-%m-%d") # 上周一
begindate=datetime.datetime.strptime("2022-01-01","%Y-%m-%d") # 指定一天
begindate=datetime.datetime.strptime("202201","%Y%m") # 指定一天 2022-01-01 00:00:00
```

## 循环

* For

for 循环可以遍历任何可迭代对象，如一个列表或者一个字符串

for [variable] in [sequence]:
    (statements)
else:
    (statements)

```python
for x in range(6):
  print(x) # 0 1 2 3 4 5
  if x == 3:
    break
else:
  print("Finished!")
```

* While

while 判断条件(condition)：
    执行语句(statements)

```python
a = 1
while a < 10:
  print(a)
  a += 2
else:
  print ("a >= 10")
```

## 异常处理

* 异常捕获

```python
try:
  ...
except Exception as FailReaon:
  print(str(FailReaon))
  ...
else:
  ...
```

* 抛出异常
```python
raise Exception('Error message');
```
