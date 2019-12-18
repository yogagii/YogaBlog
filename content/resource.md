Title: Resource
Date: 2019-09-21
Category: React-Admin
Tags: React-Admin
Author: Yoga

Resource allows you to define a component for each CRUD operation, using the following prop names:

* list (if defined, the resource is displayed on the Menu)
* create
* edit
* show

```javascript
import React from 'react';
import { Admin, Resource } from 'react-admin';
import jsonServerProvider from 'ra-data-json-server';

import { PostList, PostCreate, PostEdit, PostShow, PostIcon } from './posts';
import { UserList } from './posts';
import { CommentList, CommentEdit, CommentCreate, CommentIcon } from './comments';

const App = () => (
  <Admin dataProvider={jsonServerProvider('http://jsonplaceholder.typicode.com')}>
    <Resource name="posts" list={PostList} create={PostCreate} edit={PostEdit} show={PostShow} icon={PostIcon} />
    <Resource name="users" list={UserList} />
    <Resource name="comments" list={CommentList} create={CommentCreate} edit={CommentEdit} icon={CommentIcon} />
    <Resource name="tags" />
  </Admin>
);
```

Resource also accepts additional props:

* name
* icon
* options

React-admin uses the name prop both to determine the API endpoint (passed to the dataProvider), and to form the URL for the resource.

React-admin will render the icon prop component in the menu.

options.label allows to customize the display name of a given resource in the menu.

```javascript
<Resource name="v2/posts" options={{ label: 'Posts' }} list={PostList} icon={PostIcon} />
```