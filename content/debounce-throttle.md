Title: 防抖和节流
Date: 2020-04-01
Category: Javascript
Tags: JS
Author: Riz

## 函数防抖

> 防抖：将多次执行变为最后一次执行

当持续触发事件时，一定时间段内没有再触发事件，事件处理函数才会执行一次，如果设定时间到来之前，又触发了事件，就重新开始延时。

```js
// use.js
let timeout;
export function useDebounce(func, delay) {
  return function() {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      func.apply(this, arguments);
    }, delay);
  };
}

// search.js
import { useDebounce } from '@/services/use.js';

let lastFetchId = 0;

const [options, setOptions] = useState<OptionProps[]>([]);
const [fetching, setFetching] = useState(false);

const handleSearch = useDebounce((value: string) => {
  if (value) {
    lastFetchId += 1;
    const fetchId = lastFetchId;
    setFetching(true);
    dispatch({ ...fetchOption, payload: { query: { q: value } } }).then((res: OptionProps[]) => {
      if (fetchId === lastFetchId) {
        setFetching(false);
        setOptions(res);
      }
    });
  }
}, 800);

return (
  <Select
    showSearch
    onSearch={handleSearch}
  />
)
```

## 函数节流

> 节流：将多次执行变为每隔一段时间执行

防抖的问题：如果在限定时间段内，不断触发滚动事件，只要不停止触发，理论上就永远不会输出当前距离顶部的距离。

当持续触发事件时，保证在一定时间内只调用一次事件处理函数，意思就是说，假设一个用户一直触发这个函数，且每次触发小于既定值，函数节流会每隔这个时间调用一次

```js
function throttle(fn, delay) {
  let valid = true
  return function () {
    if (!valid) {
      //休息时间 暂不接客
      return false
    }
    // 工作时间，执行函数并且在间隔期内把状态位设为无效
    valid = false
    setTimeout(() => {
      fn()
      valid = true
    }, delay)
  }
}
```
