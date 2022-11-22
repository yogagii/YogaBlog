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