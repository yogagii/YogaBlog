Title: JS note
Date: 2020-04-01
Category: Javascript
Tags: JS
Author: Riz

## Prototype

历史：没做这个class

```js
class A {
    ...
}

// Guozhe 用A ->
const a = new A()
a......

// Riz 
class A {
    ...
    sb: ''
    calc() {
        //sb ->
    }
}
```

面向对象
```js
//Riz
class B extends A {
    sb: ''
    ....
}

const b = new B

A = function () {
    let sb: ''
}

const b = new A
// A 定义的一些闭包属性就不会被影响
b.prototype.calc = function () {
    
}
```

所以才有原型链

// 本质就是 Dom -> Js.Object
// JQuery -> 10 dom $('#....').html() // 
$('#....').html() // 重绘重排
$('#....').html()
$('#....').html()*10


// {type: 'div', children: [{type: 'div'}]}

## shadow dom

// 重绘重排

function () {
    state: {sample: '1'}
    setState({sample: '2'})
    setState({})
}

this.state->

// Security

// xss + sql
```html
<input />
<div id="abc"></div>

['; show databases; select * from user where 1']
```

//csrf
React


## 防抖

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