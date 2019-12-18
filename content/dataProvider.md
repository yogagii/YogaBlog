Title: Data Provider
Date: 2019-09-21
Category: React-Admin
Tags: React-Admin
Author: Yoga

Action | Expected API request  
-|-
Get list | 	GET http://my.api.url/posts?sort=['title','ASC']
Get one record | GET http://my.api.url/posts/123
Get several records | GET http://my.api.url/posts?filter={ids:[123,456,789]}
Update a record	| PUT http://my.api.url/posts/123 
Create a record	| POST http://my.api.url/posts/123
Delete a record | DELETE http://my.api.url/posts/123

## Simple REST

npm install ra-data-simple-rest

```javascript
import { fetchUtils, Admin, Resource } from 'react-admin';
import simpleRestProvider from 'ra-data-simple-rest';

const httpClient = (url, options = {}) => {
  options.user = {
    authenticated: true,
    token: 'SRTRDFVESGNJYTUKTYTHRG'
  }
  return fetchUtils.fetchJson(url, options);
}
const dataProvider = simpleRestProvider('http://path.to.my.api/', httpClient);

const App = () => (
  <Admin dataProvider={dataProvider}>
    <Resource name="posts" list={PostList} />
  </Admin>
);
```

Instead of writing your own Data Provider, you can enhance the capabilities of an existing data provider. To enhance a provider with the upload feature, compose addUploadFeature function with the data provider function:

```javascript
import simpleRestProvider from 'ra-data-simple-rest';
import addUploadFeature from './addUploadFeature';

const dataProvider = simpleRestProvider('http://path.to.my.api/');
const uploadCapableDataProvider = addUploadFeature(dataProvider);

const App = () => (
  <Admin dataProvider={uploadCapableDataProvider}>
    <Resource name="posts" list={PostList} />
  </Admin>
);
```

## Request Format

Data queries require a type (e.g. GET_ONE), a resource (e.g. ‘posts’) and a set of parameters.

```javascript
dataProvider(GET_LIST, 'posts', {
  pagination: { page: 1, perPage: 5 },
  sort: { field: 'title', order: 'ASC' },
  filter: { author_id: 12 },
});

dataProvider(GET_ONE, 'posts', { id: 123 });

dataProvider(CREATE, 'posts', { data: { title: "hello, world" } });

dataProvider(UPDATE, 'posts', {
  id: 123,
  data: { title: "hello, world!" },
  previousData: { title: "previous title" }
});

dataProvider(UPDATE_MANY, 'posts', {
  ids: [123, 234],
  data: { views: 0 },
});

dataProvider(DELETE, 'posts', {
  id: 123,
  previousData: { title: "hello, world" }
});

dataProvider(DELETE_MANY, 'posts', { ids: [123, 234] });

dataProvider(GET_MANY, 'posts', { ids: [123, 124, 125] });

dataProvider(GET_MANY_REFERENCE, 'comments', {
  target: 'post_id',
  id: 123,
  sort: { field: 'created_at', order: 'DESC' }
});
```

## Response Format

```javascript
dataProvider(GET_LIST, 'posts', {
    pagination: { page: 1, perPage: 5 },
    sort: { field: 'title', order: 'ASC' },
    filter: { author_id: 12 },
})
.then(response => console.log(response));
// {
//     data: [
//         { id: 126, title: "allo?", author_id: 12 },
//         { id: 127, title: "bien le bonjour", author_id: 12 },
//         { id: 124, title: "good day sunshine", author_id: 12 },
//         { id: 123, title: "hello, world", author_id: 12 },
//         { id: 125, title: "howdy partner", author_id: 12 },
//     ],
//     total: 27
// }

dataProvider(GET_ONE, 'posts', { id: 123 })
.then(response => console.log(response));
// {
//     data: { id: 123, title: "hello, world" }
// }

dataProvider(CREATE, 'posts', { data: { title: "hello, world" } })
.then(response => console.log(response));
// {
//     data: { id: 450, title: "hello, world" }
// }

dataProvider(UPDATE, 'posts', {
    id: 123,
    data: { title: "hello, world!" },
    previousData: { title: "previous title" }
})
.then(response => console.log(response));
// {
//     data: { id: 123, title: "hello, world!" }
// }

dataProvider(UPDATE_MANY, 'posts', {
    ids: [123, 234],
    data: { views: 0 },
})
.then(response => console.log(response));
// {
//     data: [123, 234]
// }

dataProvider(DELETE, 'posts', {
    id: 123,
    previousData: { title: "hello, world!" }
})
.then(response => console.log(response));
// {
//     data: { id: 123, title: "hello, world" }
// }

dataProvider(DELETE_MANY, 'posts', { ids: [123, 234] })
.then(response => console.log(response));
// {
//     data: [123, 234]
// }

dataProvider(GET_MANY, 'posts', { ids: [123, 124, 125] })
.then(response => console.log(response));
// {
//     data: [
//         { id: 123, title: "hello, world" },
//         { id: 124, title: "good day sunshise" },
//         { id: 125, title: "howdy partner" },
//     ]
// }

dataProvider(GET_MANY_REFERENCE, 'comments', {
    target: 'post_id',
    id: 123,
    sort: { field: 'created_at', order: 'DESC' }
});
.then(response => console.log(response));
// {
//     data: [
//         { id: 667, title: "I agree", post_id: 123 },
//         { id: 895, title: "I don't agree", post_id: 123 },
//     ],
//     total: 2,
// }
```

## Request Processing && Response Processing

Data Providers often use a switch statement, and finish by a call to fetch(). 

```javascript
import { stringify } from 'query-string';
import {
  GET_LIST,
  GET_ONE,
  CREATE,
  UPDATE,
  DELETE,
  GET_MANY,
  GET_MANY_REFERENCE,
} from 'react-admin';

const apiUrl = 'http://path.to.my.api/';

export default (type, resource, params) => {
  let url = '';
  const options = {
    headers : new Headers({
      Accept: 'application/json',
    }),
  };
  switch (type) {
    case GET_LIST: {
      const { page, perPage } = params.pagination;
      const { field, order } = params.sort;
      const query = {
        sort: JSON.stringify([field, order]),
        range: JSON.stringify([
            (page - 1) * perPage,
            page * perPage - 1,
        ]),
        filter: JSON.stringify(params.filter),
      };
      url = `${apiUrl}/${resource}?${stringify(query)}`;
      break;
    }
    case GET_ONE:
      url = `${apiUrl}/${resource}/${params.id}`;
      break;
    case CREATE:
      url = `${apiUrl}/${resource}`;
      options.method = 'POST';
      options.body = JSON.stringify(params.data);
      break;
    case UPDATE:
      url = `${apiUrl}/${resource}/${params.id}`;
      options.method = 'PUT';
      options.body = JSON.stringify(params.data);
      break;
    case UPDATE_MANY:
      const query = {
        filter: JSON.stringify({ id: params.ids }),
      };
      url = `${apiUrl}/${resource}?${stringify(query)}`;
      options.method = 'PATCH';
      options.body = JSON.stringify(params.data);
      break;
    case DELETE:
      url = `${apiUrl}/${resource}/${params.id}`;
      options.method = 'DELETE';
      break;
    case DELETE_MANY:
      const query = {
        filter: JSON.stringify({ id: params.ids }),
      };
      url = `${apiUrl}/${resource}?${stringify(query)}`;
      options.method = 'DELETE';
      break;
    case GET_MANY: {
      const query = {
        filter: JSON.stringify({ id: params.ids }),
      };
      url = `${apiUrl}/${resource}?${stringify(query)}`;
      break;
    }
    case GET_MANY_REFERENCE: {
      const { page, perPage } = params.pagination;
      const { field, order } = params.sort;
      const query = {
        sort: JSON.stringify([field, order]),
        range: JSON.stringify([
          (page - 1) * perPage,
          page * perPage - 1,
        ]),
        filter: JSON.stringify({
          ...params.filter,
          [params.target]: params.id,
        }),
      };
      url = `${apiUrl}/${resource}?${stringify(query)}`;
      break;
    }
    default:
      throw new Error(`Unsupported Data Provider request type ${type}`);
  }

  return fetch(url, options)
    .then(res => {
        headers = res.headers;
        return res.json();
    })
    .then(json => {
      switch (type) {
        case GET_LIST:
        case GET_MANY_REFERENCE:
          if (!headers.has('content-range')) {
            throw new Error(
              'The Content-Range header is missing in the HTTP Response.'
            );
          }
          return {
            data: json,
            total: parseInt(
              headers
                .get('content-range')
                .split('/')
                .pop(),
                10
            ),
          };
        case CREATE:
          return { data: { ...params.data, id: json.id } };
        case DELETE_MANY:
          return { data: json || [] };
        default:
          return { data: json };
      }
    });
};
```