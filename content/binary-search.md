Title: 二分搜索的各种写法
Date: 2018-10-14 21:04
Category: Programming
Tags: binary search, algorithm
Author: 张本轩

1. 对于已排序的数组x[0..n-1]，想查找数t，若t在x中则返回其下标（如有多个重复，返回其中之一)，若t不在x中则返回-1。
```cpp
    int binarysearch(vector<int> x, int t) {
    int n = x.size();
    int l = 0, u = n - 1, m;
    while (l <= u) {
        m = l + (u - l) / 2;
        if (x[m] < t) l = m + 1;
        else if (x[m] == t) return m;
        else u = m - 1;
    }
    return -1;
    }
```

2. 如果我们希望确定t在数组中第一次出现的位置，我们可以在循环中保持x[l]<t 且 x[u]>=t 的特性，我们可以做以下修改:
```cpp
    int binarysearch2(vector<int> x, int t) {
        int n = x.size();
        int l = -1, u = n;
        while (l + 1 != u) {
            // x[l] < t && x[u] >= t && l < u
            int m = l + (u - l) / 2;
            if (x[m] < t) l = m;
            else u = m;
        }
        // l + 1 = u && x[l] < t && x[u] >= t
        int p = u;
        if (p >= n || x[p] != t) p = -1;
        return p;
    }
```

3. 其实上述代码的p或者u就代表第一个大于或等于t的元素的位置，即STL里面的lower_bound函数。
```cpp
    int binarysearch3(vector<int> x, int t) {
        int n = x.size();
        int l = -1, u = n;
        while (l + 1 != u) {
            // x[l] < t && x[u] >= t && l < u
            int m = l + (u - l) / 2;
            if (x[m] < t) l = m;
            else u = m;
        }
        // l + 1 = u && x[l] < t && x[u] >= t
        return u;
    }
```

4. 最后如果要实现STL里面的upper_bound函数，即返回第一个大于t的元素的位置我们可以这样做:
```cpp
    int binarysearch4(vector<int> x, int t) {
        int n = x.size();
        int l = -1, u = n;
        while (l + 1 != u) {
            // x[l] <= t && x[u] > t && l < u
            int m = l + (u - l) / 2;
            if (x[m] > t) u = m;
            else l = m;
        }
        // l + 1 = u && x[l] <= t && x[u] > t
        return u;
    }
```
写二分搜索函数的关键是保持循环不变式，即保证t与区间两端点之间的大小关系不变，这样就可以根据区间两端的大小关系来判断其是否是你需要的结果了。