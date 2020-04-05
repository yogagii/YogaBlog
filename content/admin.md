Title: Admin
Date: 2019-09-21
Category: React-Admin
Tags: React-Admin
Author: Yoga

The <Admin> component creates an application with its own state, routing, and controller logic. <Admin> requires only a dataProvider prop, and at least one child <Resource> to work:

```html
const App = () => (
    <Admin dataProvider={simpleRestProvider('http://path.to.my.api')}>
        <Resource name="posts" list={PostList} />
    </Admin>
);
```

All the props accepted by the <Admin> Component:

* dataProvider
* title
* dashboard
* catchAll
* menu
* theme
* appLayout
* customReducers
* customSagas
* customRoutes
* authProvider
* loginPage
* logoutButton
* initialState
* history
* locale
* i18nProvider

## title

title="My Custom Admin"

## dashboard

By default, the homepage of an admin app is the list of the first child 'Resource'. But you can also specify a custom component instead. To fit in the general design, use Material UI's 'Card' component, and react-admin's 'Title' component to set the title in the AppBar:

dashboard={Dashboard}

```javascript
// in src/Dashboard.js
import React from 'react';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import { Title } from 'react-admin';
export default () => (
  <Card>
    <Title title="Welcome to the administration" />
    <CardContent>Lorem ipsum sic dolor amet...</CardContent>
  </Card>
);
```

## catchAll

When users type URLs that don't match any of the children <Resource> components, they see a default "Not Found" page. You can customize this page to use the component of your choice by passing it as the catchAll prop. 

## theme

Material UI supports theming. This lets you customize the look and feel of an admin by overriding fonts, colors, and spacing. You can provide a custom material ui theme by using the theme prop:

```javascript
const theme = createMuiTheme({
  palette: {
    type: 'dark', // Switching the dark mode on is a single property value change.
  },
});
```

## menu
 This prop is deprecated废弃的. To override the menu component, use a custom layout instead.

## appLayout

Custom layout component: deeply customize the app header, the menu, or the notifications. It must contain a {children} placeholder, where react-admin will render the resources. And finally, if you want to show the spinner in the app header when the app fetches data in the background, the Layout should connect to the redux store.

Your custom layout can simply extend the default <Layout> component if you only want to override the appBar, the menu, the notification component, or the error page. 

```javascript
// in src/App.js
import MyLayout from './MyLayout';

const App = () => (
  <Admin appLayout={MyLayout} dataProvider={simpleRestProvider('http://path.to.my.api')}>
  // ...
  </Admin>
);

// in src/MyLayout.js
import { Layout } from 'react-admin';
import MyAppBar from './MyAppBar';
import MyMenu from './MyMenu';
import MyNotification from './MyNotification';

const MyLayout = (props) => <Layout
  {...props}
  appBar={MyAppBar}
  menu={MyMenu}
  notification={MyNotification}
/>;

export default MyLayout;
```
### customReducers

The Admin app uses Redux to manage state. The state has the following keys:

```
{
    admin: { /*...*/ }, // used by react-admin
    form: { /*...*/ }, // used by redux-form
    routing: { /*...*/ }, // used by react-router-redux
}
```

If your components dispatch custom actions, you probably need to register your own reducers to update the state with these actions. 

To register this reducer in the 'Admin' app, simply pass it in the customReducers prop:

```javascript
// in src/bitcoinRateReducer.js
export default (previousState = 0, { type, payload }) => {
  if (type === 'BITCOIN_RATE_RECEIVED') {
    return payload.rate;
  }
  return previousState;
}

// in src/App.js
import React from 'react';
import { Admin } from 'react-admin';

import bitcoinRateReducer from './bitcoinRateReducer';

const App = () => (
    <Admin customReducers={{ bitcoinRate: bitcoinRateReducer }} dataProvider={simpleRestProvider('http://path.to.my.api')}>
        ...
    </Admin>
);

export default App;
```

## customRoutes

To register your own routes, create a module returning a list of react-router <Route> component. Then, pass this array as customRoutes prop in the <Admin> component.

```javascript
// in src/customRoutes.js
import React from 'react';
import { Route } from 'react-router-dom';
import Foo from './Foo';
import Bar from './Bar';
import Baz from './Baz';

export default [
  <Route exact path="/foo" component={Foo} />,
  <Route exact path="/bar" component={Bar} />,
  <Route exact path="/baz" component={Baz} noLayout />,
];

// in src/App.js

<Admin customRoutes={customRoutes} 
  // ...
</Admin>
```

 When a user browses to /baz, the component will appear outside of the defined Layout, leaving you the freedom to design the screen the way you want.

 ## Declaring resources at runtime

 You might want to dynamically define the resources when the app starts. The Admin component accepts a function as its child and this function can return a Promise.

 ```javascript
 import React from 'react';

import { Admin, Resource } from 'react-admin';
import simpleRestProvider from 'ra-data-simple-rest';

import { PostList } from './posts';
import { CommentList } from './comments';

const knownResources = [
  <Resource name="posts" list={PostList} />,
  <Resource name="comments" list={CommentList} />,
];

const fetchResources = permissions =>
  fetch('https://myapi/resources', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(permissions),
  })
  .then(response => response.json())
  .then(json => knownResources.filter(resource => json.resources.includes(resource.props.name)));

const App = () => (
  <Admin dataProvider={simpleRestProvider('http://path.to.my.api')}>
    {fetchResources}
  </Admin>
);
```


