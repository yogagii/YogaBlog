Title: C++ STL常用数据结构整理
Date: 2018-10-07 20:21
Category: Programming
Tags: c++, stl
Author: 张本轩

1. vector
    * 插入push_back(), 时间复杂度O(1)
    * 删除erase(iterator position), 时间复杂度O(n)取决于删除的位置
    * 支持随机访问
2. stack
    * 插入push(), 时间复杂度O(1)
    * 删除pop(), 时间复杂度O(1)
    * 不支持随机访问
3. queue
    * 插入push(), 时间复杂度O(1)
    * 删除pop(), 时间复杂度O(1)
    * 不支持随机访问
4. list(双向链表)
    * 插入push_front(), push_back(), 时间复杂度O(1)
    * 删除pop_front(), pop_back(), erase(iterator position), 时间复杂度O(1)
    * 不支持随机访问
5. forward_list(单链表)
    * 插入push_front(), insert_after(), 时间复杂度O(1)
    * 删除pop_front(), erase_after(), 时间复杂度O(1)
    * 不支持随机访问
6. deque(双端队列)
    * 插入push_front(), push_back(), 时间复杂度O(1)
    * 删除push_back(), pop_back(), 时间复杂度O(1)
    * 支持随机访问
    * 相对于list, deque在中间位置插入速读较慢
7. priority_queue(优先级队列)
    * 插入push(), 时间复杂度O(log(n))
    * 删除pop(), 时间复杂度O(log(n))
    * 内部实现支持随机访问，但是优先级队列不支持
8. set(集合)
    * 利用二叉搜索树实现
    * 插入insert(), 时间复杂度O(log(n)), 如果给出插入位置则时间复杂度为O(1)
    * 删除erase(position), 时间复杂度O(1); erase(val), 时间复杂度O(log(n))
    * 搜索find(), 时间复杂度O(log(n))
    * 支持lower_bound(), upper_bound(), equal_range()操作
9. unordered_set
    * 利用哈希表实现
    * 插入insert(), 时间复杂度平均情况O(1)，最坏情况O(n)
    * 删除erase(), 时间复杂度平均情况O(1), 最坏情况O(n)
    * 搜索find(), 时间复杂度平均情况O(1), 最坏情况O(n)
    * 不支持lower_bound(), upper_bound()操作
10. multiset
    * 能包括多个有相同值的元素
    * 利用二叉搜索树实现
    * 插入insert(), 时间复杂度O(log(n)), 如果给出插入位置则时间复杂度为O(1)
    * 删除erase(position), 时间复杂度O(1); erase(val), 时间复杂度O(log(n))
    * 搜索find(), 时间复杂度O(log(n))
    * 支持lower_bound(), upper_bound(), equal_range()操作
11. unordered_multiset
    * 能包括多个有相同值的元素
    * 利用哈希表实现
    * 插入insert(), 时间复杂度平均情况O(1)，最坏情况O(n)
    * 删除erase(), 时间复杂度平均情况O(1), 最坏情况O(n)
    * 搜索find(), 时间复杂度平均情况O(1), 最坏情况O(n)
    * 不支持lower_bound(), upper_bound()操作
12. map
    * 利用二叉搜索树实现
    * 插入insert(), 时间复杂度O(log(n)), 如果给出插入位置则时间复杂度为O(1)
    * 删除erase(position), 时间复杂度O(1); erase(val), 时间复杂度O(log(n))
    * 搜索find(), 时间复杂度O(log(n))
    * 支持lower_bound(), upper_bound(), equal_range()操作
    * key-value对，支持[]访问
13. unordered_map
    * 利用哈希表实现
    * 插入insert(), 时间复杂度平均情况O(1)，最坏情况O(n)
    * 删除erase(), 时间复杂度平均情况O(1), 最坏情况O(n)
    * 搜索find(), 时间复杂度平均情况O(1), 最坏情况O(n)
    * 不支持lower_bound(), upper_bound()操作
    * key-value对，支持[]访问
14. multimap
    * 能包括多个有相同值的元素
    * 利用二叉搜索树实现
    * 插入insert(), 时间复杂度O(log(n)), 如果给出插入位置则时间复杂度为O(1)
    * 删除erase(position), 时间复杂度O(1); erase(val), 时间复杂度O(log(n))
    * 搜索find(), 时间复杂度O(log(n))
    * 支持lower_bound(), upper_bound(), equal_range()操作
    * key-value对，不支持[]访问
15. unordered_multimap
    * 能包括多个有相同值的元素
    * 利用哈希表实现
    * 插入insert(), 时间复杂度平均情况O(1)，最坏情况O(n)
    * 删除erase(), 时间复杂度平均情况O(1), 最坏情况O(n)
    * 搜索find(), 时间复杂度平均情况O(1), 最坏情况O(n)
    * 不支持lower_bound(), upper_bound()操作
    * key-value对，不支持[]访问
