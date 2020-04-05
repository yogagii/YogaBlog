Title: React-Admin
Date: 2019-09-10
Category: React-Admin
Tags: React-Admin
Author: Yoga

## Setting Up

```javascript
npm install -g create-react-app
create-react-app test-admin
cd test-admin/
yarn add react-admin ra-data-json-server prop-types
yarn start
```

## Data Provider

```javascript
import React from "react";
import { Admin, Resource, ListGuesser } from "react-admin";
import jsonServerProvider from "ra-data-json-server";

const dataProvider = jsonServerProvider("http://jsonplaceholder.typicode.com");
const App = () => (
  <Admin dataProvider={dataProvider}>
    <Resource name="users" list={ListGuesser} />
  </Admin>
);

export default App;
```

name="users" informs react-admin to fetch the "users" records from the http://jsonplaceholder.typicode.com/users URL.

list={ListGuesser} means that react-admin should use the <ListGuesser> component to display the list of posts.

## Selecting Columns

The <ListGuesser> component is not meant to be used in production - it's just a way to quicky bootstrap an admin. ListGuesser dumps the code of the list it has guessed to the console:

```javascript
// in src/users.js
import React from "react";
import { List, Datagrid, TextField, EmailField } from "react-admin";

export const UserList = props => (
  <List {...props}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="name" />
      <TextField source="username" />
      <EmailField source="email" />
      <TextField source="address.street" />
      <TextField source="phone" />
      <TextField source="website" />
      <TextField source="company.name" />
    </Datagrid>
  </List>
);

// in src/App.js
import { Admin, Resource } from "react-admin";
import { UserList } from "./users";

const App = () => (
  <Admin dataProvider={dataProvider}>
    <Resource name="users" list={UserList} />
  </Admin>
);
```

Now, the app uses a component that you can customize. React-admin provides more Field components, mapping various data types: number, date, image, HTML, array, reference, etc.

## Customizing Styles

React-admin relies on material-ui, a set of React components modeled after Google's Material Design UI Guidelines. Material-ui uses JSS, a CSS-in-JS solution, for styling components.

```javascript
// in src/MyUrlField.js
import React from "react";
import { withStyles } from "@material-ui/core/styles";
import LaunchIcon from "@material-ui/icons/Launch";

const styles = {
  link: {
    textDecoration: "none"
  },
  icon: {
    width: "0.5em",
    paddingLeft: 2
  }
};

const MyUrlField = ({ record = {}, source, classes }) => (
  <a href={record[source]} className={classes.link}>
    {record[source]}
    <LaunchIcon className={classes.icon} />
  </a>
);

export default withStyles(styles)(MyUrlField);
```

In JSS, you define styles as a JavaScript object, using the JS variants of the CSS property names (e.g. textDecoration instead of text-decoration). To pass these styles to the component, wrap it inside a call to withStyles(styles).

高阶组件：

```javascript
import compose from "recompose/compose";
import { withStyles } from "@material-ui/core/styles";
const enhance = compose(
  withStyles(styles),
  translate
);
export default enhance(MonthlyRevenue);
```

## Handling Relationships

React-admin knows how to take advantage of these foreign keys to fetch references. ReferenceField component alone doesn't display anything. It just fetches the reference data, and passes it as a record to its child component (a TextField in our case).

```javascript
<ReferenceField source="userId" reference="users">
  <TextField source="name" />
</ReferenceField>
```

## Creation and Editing

Use the <EditGuesser> to help bootstrap it. Copy the PostEdit code dumped by the guesser in the console to the posts.js file so that you can customize the view. It issues PUT requests to the REST API upon submission.

```javascript
// in src/posts.js
// edit:
export const PostEdit = props => (
  <Edit {...props}>
    <SimpleForm>
      <DisabledInput source="id" />
      <ReferenceInput source="userId" reference="users">
        <SelectInput optionText="name" />
      </ReferenceInput>
      <TextInput source="title" />
      <LongTextInput source="body" />
    </SimpleForm>
  </Edit>
);
//creat:
export const PostCreate = props => (
  <Create {...props}>
    <SimpleForm>
      <ReferenceInput source="userId" reference="users">
        <SelectInput optionText="name" />
      </ReferenceInput>
      <TextInput source="title" />
      <LongTextInput source="body" />
    </SimpleForm>
  </Create>
);
```

<ReferenceInput> uses these props to fetch the API for possible references related to the current record. It then passes these possible references to the child component (SelectInput), which is responsible for displaying them (via their name in that case), and letting the user select one.

```javascript
// in src/App.js
import { Admin, Resource } from "react-admin";
import { PostList, PostEdit, PostCreate } from "./posts";
import { UserList } from "./users";

const App = () => (
  <Admin dataProvider={dataProvider}>
    <Resource
      name="posts"
      list={PostList}
      edit={PostEdit}
      create={PostCreate}
    />
    <Resource name="users" list={UserList} />
  </Admin>
);
```

React-admin automatically adds a "create" button on top of the posts list to give access to the <PostCreate> component. And the creation form works ; it issues a POST request to the REST API upon submission.

## Undo

When a user edits a record and hits the "Save" button, the UI shows a confirmation and displays the updated data before sending the update query to server. 

Benefit:

1. UI changes are immediate - no need to wait for the server response. 

2. Even though updates appear immediately due to Optimistic Rendering, React-admin only sends them to the server after a short delay (about 5 seconds). During this delay, the user can undo the action, and react-admin will never send the update.

## Filter

React-admin can use Input components to create a multi-criteria search engine in the list view. First, create a <Filter> component just like you would write a <SimpleForm> component, using input components as children. Then, add it to the list using the filters prop:

```javascript
// in src/posts.js
import { Filter, ReferenceInput, SelectInput, TextInput, List } from 'react-admin';

const PostFilter = (props) => (
    <Filter {...props}>
        <TextInput label="Search" source="q" alwaysOn />
        <ReferenceInput label="User" source="userId" reference="users" allowEmpty>
            <SelectInput optionText="name" />
        </ReferenceInput>
    </Filter>
);

export const PostList = (props) => (
    <List filters={<PostFilter />} {...props}>
        // ...
    </List>
);
```

## responsive

The best compromise would be to use <SimpleList> on small screens, and <Datagrid> on other screens. That's where the <Responsive> component comes in:

```javascript
// in src/posts.js
import React from 'react';
import { List, Responsive, SimpleList, Datagrid, TextField, ReferenceField, EditButton } from 'react-admin';

export const PostList = (props) => (
    <List {...props}>
        <Responsive
            small={
                <SimpleList
                    primaryText={record => record.title}
                    secondaryText={record => `${record.views} views`}
                    tertiaryText={record => new Date(record.published_at).toLocaleDateString()}
                />
            }
            medium={
                <Datagrid>
                    <TextField source="id" />
                    <ReferenceField label="User" source="userId" reference="users">
                        <TextField source="name" />
                    </ReferenceField>
                    <TextField source="title" />
                    <TextField source="body" />
                    <EditButton />
                </Datagrid>
            }
        />
    </List>
);
```




