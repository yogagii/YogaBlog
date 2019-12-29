Title: DVA.js
Date: 2019:12:27 14:33
Category: Data
Tags: DVA
Author: Riz

## 目录

### hr重构

#### 类dva

##### redux怎么变成dva的反向

```js
// dva结构
export default {
    state: {},
    reducers: {},
    effects: {}, //这一层是saga做的
}

// redux结构
import { createStore } from 'redux'

const state = { num: 1 }; 
const reducers = function (state, action) {

    if (action.type === 'ADD') {
         return {
            ...state,
            num: action.num
         }
    }

    return {
        ...state
    }
    //state.num = 3
    //return state
}

const store = createStore(reducers, state);

// 应用
store.dispatch({type: 'ADD', num: 0});

// 包装
const CustomContextProvider = ({ children }) => {
  const [state, dispatch] = useReducer(reducers, initState);
  // return <Context.Provider value={{ state, dispatch }}>{children}</Context.Provider>;
};

//我们写Dva的时候用的肯定不止一个model  
//多个Store的核心概念是 有多少个model， store.state就有多少个model 

const user = model
const message = model
const announcement = model
const comment = model
state = {
    user,
    message,
    announcement,
    comment
}

// 默认比较
var refEquality = function refEquality(a, b) {
  return a === b;
};

```

1. Context.Provider 只能放一个state
2. 所以state的结构里面全都是model，这样能全部安放
3. 默认的比较方法是 顶级state 不是原来的引用，就render
4. 修改状态一定会返还一个新的顶级state
5. 所以默认情况下一定render

浅比较 ShadowEquals 
dispatch触发 reducer
```js
function (state, action) {
    return {
        ...state,
        ...action['modelName']: {newData: {}}
    }
}
// 理解上面的代码，我只需要user的情况下， ...state里面的announcement还是原来的announcement
```

关于浅比较
```js
var hasOwn = Object.prototype.hasOwnProperty;

function is(x, y) {
  if (x === y) {
    return x !== 0 || y !== 0 || 1 / x === 1 / y;
  } else {
    return x !== x && y !== y;
  }
}

export default function shallowEqual(objA, objB) {
  if (is(objA, objB)) return true;

  if (typeof objA !== 'object' || objA === null || typeof objB !== 'object' || objB === null) {
    return false;
  }

  var keysA = Object.keys(objA);
  var keysB = Object.keys(objB);
  if (keysA.length !== keysB.length) return false;

  for (var i = 0; i < keysA.length; i++) {
    if (!hasOwn.call(objB, keysA[i]) || !is(objA[keysA[i]], objB[keysA[i]])) {
      return false;
    }
  }

  return true;
}
```


```js
const Context = createContext();
// Context.Provider => 指定在子组件可以调用里面的state
// Content.Consumer => 在这个指定Provider组件下都可以调用里面state 
const { state, dispatch } = useContext(Context);
```

```js
dva的概念就是把 state 并入到 rootState 
dispatch

const reducers = (state, action) => {
  const [modelName, reducerName] = action.type.split('/');
  const model = reducersPool[modelName];

  if (!model) {
    throw new Error(`can't find the model [${modelName}]`);
  }

  const reducer = model[reducerName];
  if (!reducer) {
    throw new Error(`can't find the model [${modelName}] reducer [${reducerName}]`);
  }

  const newState = reducer(state[modelName], { ...action });

  return {
    ...state,
    [modelName]: newState,
  };
};

```
### 极限性能记录
