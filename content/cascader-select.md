Title: Cascader Select
Date: 2021-11-10
Category: Frontend
Author: Yoga

## 层级搜索

在 ant-design3.0 的 select component 基础上，用 dropdownRender 自定义搜索选项

```jsx
const ellipsePath: taxonomyType[] = useMemo(() => {
  let ePath = clone(path)
  const len = path.length
  if (path.length > 2) {
    ePath = [path[len - 2], path[len - 1]]
    ePath.unshift({
      id: 'home',
      name: '...',
    })
  }
  return ePath
}, [path])

return (
  <Select
    mode={mode}
    value={checkedList}
    onChange={handleChange}
    dropdownRender={(menu) => (
      <div>
        {ellipsePath?.length ? (
          <div className={styles.pathWrapper}>
            <span key='home' onMouseDown={(e) => e.preventDefault()} onClick={() => prevLevel('home')}>
              <img src={homeImg} alt='home' />
            </span>
            {ellipsePath.map((p) => (
              <span key={p.id} onMouseDown={(e) => e.preventDefault()} onClick={() => prevLevel(p.id)}>
                {`${p.name} / `}
              </span>
            ))}
          </div>
        ) : null}
        {optionList.length ? (
          <ul>
            {optionList.map((op, index) => (
              <li>
                {op.name}
                {op.hasCascader ? <span onClick={() => nextLevel(op.id, op.name)} /> : null}
              </li>
            ))}
          </ul>
        ) : null}
      </div>
    )}
  >
    {optionList}
  </Select>
)
```

## 模拟搜索框

隐藏 ant-design 自带的搜索框，将原搜索框中的值填入模拟搜索框

```jsx
const [searchValue, setSearch] = useState('')
const [lastSearch, setLastSearch] = useState('')

const filterOption = (inputValue: string) => {
  const originSearch = document.querySelector(`#${popupContainer} .ant-select-search__field`)
  if (originSearch && !originSearch?.getAttribute('spellcheck')) {
    originSearch.setAttribute('spellcheck', 'false')
    originSearch.setAttribute('unselectable', 'on')
  }
  if (inputValue.length < lastSearch.length) {
    setLastSearch(inputValue)
  } else {
    setSearch(inputValue.slice(lastSearch.length))
  }
}
const clearSearch = (needRefreshHierarchy = true) => {
  const originSearch = document.querySelector(`#${popupContainer} .ant-select-search__field`)
  if (originSearch?.getAttribute('value')) {
    setLastSearch(originSearch?.getAttribute('value') || '')
  }
  setSearch('')
}

return (
  <Select
    onBlur={() => clearSearch(true)}
    showSearch
    onSearch={filterOption}
    autoClearSearchValue
    dropdownRender={(menu) => (
      <div>
        <Search
          placeholder='input search text'
          value={searchValue}
          allowClear
          onChange={clearSearch}
          onChange={() => clearSearch(true)}
        />
        {optionList}
      </div>
    )}
  >
    {optionList}
  </Select>
)
```

## 滚动加载

当 optionlist 中的选项超过 3000 个，用户点击选择框会有明显的延时

### 1. onscroll

先加载 10 个选项，用 onScroll 事件监听用户滚动到列表底部后，加载后 10 个选项

```jsx
const handleOptionScroll = (e: any) => {
  e.persist()
  const { scrollTop, offsetHeight, scrollHeight } = e.target
  const current = optionList.length
  if (scrollTop + offsetHeight >= scrollHeight && current < options.length) {
    setOptionList(options.slice(0, current + 10))
  }
}

return (
  <Select
    dropdownRender={(menu) => (
      <ul id='optionlist' className='ant-select-dropdown-menu' onScroll={handleOptionScroll}>
        {optionList.map((op, index) => (
          <li>{op.name}</li>
        ))}
      </ul>
    )}
  >
    {optionList}
  </Select>
)
```

缺点：

- 进度条会慢慢变长，所以用户无法直接拖动进度条到列表底部
- 滚动加载会有一点点卡壳

### 2. react-virtualized 只渲染可视框内的选项

```
npm i --save @types/react-virtualized
```

Required Property:

| Property | Type | Required | Description |
| - | - | - | - |
height | number | y | list height
width | number | y | list width
rowCount | number | y | list length
rowHeight | number or func | y | row height
rowRenderer | func | y | item content
overscanRowCount | number | n | 可视区域前后预渲染行数，默认10


```jsx
import { AutoSizer, List } from 'react-virtualized'

return (
  <Select
    dropdownRender={(menu) => (
      <AutoSizer>
        {({ width }) => (
          <List
            height={250}
            width={width}
            rowCount={optionlist.length}
            rowHeight={20}
            rowRenderer={({ key, index }) => <li key={key}>{op.name}</li>}
          />
        )}
      </AutoSizer>
    )}
  >
    {optionList}
  </Select>
)
```

缺点：

- width为必须参数，且只能传数字不’100%‘，需要撑满整行时需要包一层AutoSizer
- rowHeight为必须参数，需要自适应高度时需要用list.get(index % list.size)计算
- 滑动快时列表下方有空白，渲染慢


https://www.npmjs.com/package/react-virtualized

https://github.com/bvaughn/react-virtualized/blob/master/docs/List.md

### 3. react-virtuoso 只渲染可视框内的选项

```
npm install react-virtuoso
```

Property:

| Property | Type | Required | Description |
| - | - | - | - |
data | readonly D[] | n | data list
itemContent | ItemContent<D> | n | Set the callback to specify the contents of the item.
totalCount | number | n | If data is set, the total count will be inferred from the length of the array.

```jsx
import { Virtuoso } from 'react-virtuoso'

return (
  <Select
    dropdownRender={(menu) => (
      <Virtuoso
        data={optionList}
        style={{ height: '250px' }}
        itemContent={(index, op) => <li>{op.name}</li>}
        onMouseDown={e => e.preventDefault()} // 否则无法拖动滚动条
      />
    )}
  >
    {optionList}
  </Select>
)
```

优点：

- 没有required property, 最少传个data和itemContent就能看到效果
- 不需要width和rowHeight, 自适应能力强
- 滚动相当流畅

https://virtuoso.dev/

https://virtuoso.dev/virtuoso-api-reference/
