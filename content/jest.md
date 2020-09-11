Title: JEST
Date: 2020-08-20
Category: React
Tags: Unit test
Author: Yoga

```
umi test --coverage
umi test --watch
umi test \allWorkbooks
```

```js
// index.test.tsx
import 'jest';
import Index from '..';
import React from 'react';
import renderer, { ReactTestInstance, ReactTestRenderer } from 'react-test-renderer';

describe('Page: index', () => {
  it('Render correctly', () => {
    const wrapper: ReactTestRenderer = renderer.create(<Index />);
    expect(wrapper.root.children.length).toBe(1);
    const outerLayer = wrapper.root.children[0] as ReactTestInstance;
    expect(outerLayer.type).toBe('div');
  });
});
```

react 测试利器 enzyme 有三种渲染方式：shallow, mount, render。

- shallow 浅渲染，仅仅对当前 jsx 结构内的顶级组件进行渲染，而不对这些组件的内部子组件进行渲染，速度快
- mount 完整渲染，渲染结果和浏览器渲染结果一样，可以对内部子组件实现复杂交互功能的组件进行测试。
- render 完整渲染，只调用了组件的 render 方法，得到 jsx 并转码为 html，所以组件的生命周期方法内的逻辑都测试不到

## without state

```js
import React from 'react'
import SingleBireport from '../components/SingleReport/SingleBireport.tsx'
import { shallow } from 'enzyme'
import { singleReport } from './mockData'

jest.mock('react-redux', () => ({
  connect: () => jest.fn(),
  useSelector: jest.fn((fn) => fn()),
  useDispatch: () => jest.fn(),
}))

describe('Single Bireport', () => {
  const singleBireport = shallow(
    <SingleBireport workbook={singleReport} key='1' position={position} category={'category'} />
  )
  it('test Single Bireport has icon', () => {
    const icon = singleBireport.find('#titleIcon')
    expect(icon.at(0).exists()).toBe(true)
  })
})
```

## mock provider

```js
// MockProvider.js
import React from 'react'
import configureStore from 'redux-mock-store'
import { Provider } from 'react-redux'
import { mergeDeepRight } from 'ramda'
import { commonState, userState } from './mockData'

export const getMockProvider = (partialState) => {
  const mockStore = configureStore()
  const store = mockStore(
    mergeDeepRight(
      {
        common: commonState,
        user: userState,
      },
      partialState
    )
  )

  return {
    MockProvider: ({ children }) => {
      return <Provider store={store}>{children}</Provider>
    },
    store,
  }
}
```

## with state

```js
// service
import { useDispatch, useHistory, useLocation, useSelector, shallowEqual, useRouteMatch } from 'dva'
import { initialize } from '@/utils/common'
import { useEffect, useState } from 'react'

export const useConnect = (mapStateToProps, compare = shallowEqual) => {
  const dispatch = useDispatch()
  const history = useHistory()
  const location = useLocation()
  const state = useSelector(mapStateToProps, compare)
  const match = useRouteMatch()

  return {
    dispatch,
    history,
    location,
    match,
    ...state,
  }
}
```

```js
import React from 'react'
import AllWorkbooks from '../allWorkbooks/allWorkbooks'
import DashboardList from '../components/DashboardList/DashboardList'
import { mount } from 'enzyme'
import { getMockProvider } from './MockProvider'
import reports from '@/models/reports'

jest.mock('react-router', () => ({
  useHistory: jest.fn().mockReturnValue({ location: { pathname: '/reports/all' } }),
  useLocation: jest.fn().mockReturnValue({ pathname: '/reports/all' }),
  useRouteMatch: () => ({ match: '' }),
}))

jest.mock('umi/link', () => 'a')

const setup = (partialState) => {
  const { MockProvider } = getMockProvider(partialState)
  return {
    MockProvider,
  }
}

describe('allworkbook list', () => {
  const { MockProvider } = setup({
    reports: reportsState,
  })

  const workbookListWrapper = mount(
    <MockProvider>
      <AllWorkbooks />
    </MockProvider>
  )

  it('test workbook list', () => {
    const dashboardLists = workbookListWrapper.find(DashboardList)
    expect(dashboardLists.length).toBe(2)
  })
})
```

## dva reducers

```js
import React from 'react'
import AllWorkbooks from '../allWorkbooks/allWorkbooks'
import DashboardList from '../components/DashboardList/DashboardList'
import { mount } from 'enzyme'
import { getMockProvider } from './MockProvider'
import bireport from '@/models/bireport'
import reports from '@/models/reports'
import { bireportAll, externalData, permissions, siteConfig } from './mockData'

describe('allworkbook list', () => {
  const reports_initialState = {
    externalList: {},
  }

  const reportsState = reports.reducers.saveMarket(reports_initialState, {
    payload: {
      state: 'externalList',
      data: externalData.data,
    },
  })

  it('test reports reducer', () => {
    expect(Object.keys(reportsState.externalList).length).toBe(1)
  })

  const { MockProvider } = setup({
    reports: reportsState,
  })
})
```

## dva effects

```js
import bireport from '@/models/bireport'
import * as usersService from '@/services'
import { call } from 'ramda'
import { userState } from './mockData'

describe('Dashboard filter', () => {
  it('test fetchAll effects', () => {
    const actionCreator = {
      type: 'bireport/fetchAll',
      payload: {
        api: 'bireportAll',
        state: 'allWorkbooks',
      },
      storage: 'allMulti',
    }
    const generator = bireport.effects.fetchAll(actionCreator, { call: call, select: jest.fn() })
    let next = generator.next()
    next = generator.next({
      user: userState,
    })
    expect(next.value).toEqual(call(usersService.getItem, actionCreator.payload))
  })
})
```

## mock part of module

```js
jest.mock('@/services/use.js', () => {
  const useFunction = require.requireActual('@/services/use.js')
  return {
    ...useFunction,
    useDebounce: jest.fn((fn) => fn),
  }
})
```

## mock dispatch

```js
import * as service from '@/proxy-components/ProxyInput/service'

const mockDispatch = jest.fn().mockResolvedValue(() => {
  const { autoCompleteData } = require.requireActual('./mockData')
  return autoCompleteData
})

jest.mock('react-redux', () => ({
  connect: () => jest.fn(),
  useSelector: jest.fn((fn) => fn()),
  useDispatch: () => mockDispatch,
}))

const fetchData = jest.spyOn(service, 'fetchCompleteData')
// Simulate input keyword
expect(fetchData).toHaveBeenCalledWith(mockDispatch, 'test')
```

## react-dom/test-utils

```js
import ReactDOM from 'react-dom'
import { act, Simulate } from 'react-dom/test-utils'

describe('Autocomplete for search input', () => {
  let container

  beforeEach(() => {
    container = document.createElement('div')
    document.body.appendChild(container)
  })

  afterEach(() => {
    document.body.removeChild(container)
    container = null
  })

  it('test autocomplete effects', () => {
    act(() => {
      ReactDOM.render(<ProxyInput />, container)
    })
    const searchInput = container.querySelector('input')
    expect(searchInput.value).toBe('')

    // Simulate input keyword
    act(() => {
      Simulate.focus(searchInput)
      searchInput.value = 'test'
      Simulate.change(searchInput)
    })
    expect(searchInput.value).toBe('test')
  })
})
```

## setTimeout
```js
it('test autocomplete effects', (done) => {
  setImmediate(() => {
    const options = container.querySelector('#options')
    expect(options).toBeDefined()
    expect(options.children.length).toBe(3)
    options.children.forEach((item) => {
      expect(item.querySelector('img')).toBeDefined()
    })
    done()
  })
})
```
