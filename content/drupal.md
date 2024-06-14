Title: Drupal
Date: 2024-04-14
Category: Backend
Author: Yoga

## CMS

A content management system (CMS) is a software tool that lets users add, publish, edit, or remove content from a website.

Drupal is a flexible CMS based on the LAMP stack, with a modular design allowing features to be added and removed by installing and uninstalling modules, and allowing the entire look and feel of the website to be changed by installing and uninstalling themes.

Drupal 10 requires at least PHP 8.1

A content entity (or more commonly, entity) is an item of content data, which can consist of text, HTML markup, images, attached files, and other data that is intended to be displayed to site visitors. Within entity items, the data is stored in individual fields, each of which holds one type of data, such as formatted or plain text, images or other files, or dates. 

## Setup local environment

1. 安装 Docker
Rancher Desktop: https://docs.rancherdesktop.io/getting-started/installation/

2. Start Container

    Check `docker-compose.yml` Configuration

    Modify the `web(8080)`/`mysql(13306)` port if conflict with your local.

    ```yml
    version: '2'
    services:
      cp_mysql:
        image: mysql:8
        environment:
          - MYSQL_ROOT_PASSWORD=xxx
          - MYSQL_DATABASE=xxx
          - MYSQL_USER=xxx
          - MYSQL_PASSWORD=xxx
        volumes:
          - ./docker/mysql/data:/var/lib/mysql
        ports:
          - "13306:3306"
      cp_cms:
        build: docker/php-fpm
        working_dir: /application
        volumes:
          - .:/application
        depends_on:
          - cp_mysql
      cp_nginx:
        image: nginx:alpine
        working_dir: /application
        volumes:
          - .:/application
          - ./docker/nginx/nginx.conf:/etc/nginx/conf.d/default.conf
        ports:
          - "8080:80"
        depends_on:
          - cp_cms
    ```
    Start Project with Docker Compose
    ```bash
    cd /cp_cms
    docker compose up -d # 后台运行
    docker compose ps
    docker compose logs -f cp_mysql
    docker compose logs -f cp_cms
    docker compose down
    ```

3. Mysql Database

    Import Database from Dump files

    Dbeaver:
    * 右键 → 工具 → 恢复数据库 → 选择sql文件
    * 创建脚本 → 复制黏贴sql文件 → 整页运行(第三个按钮)

    Copy settings from template
    ```shell
    cp web/sites/default/docker-local.settings.php web/sites/default/settings.php
    ```

4. Update Packages and Use Drush to Sync Entity Schema

    Run these 2 command after pulling code everytime.

    Install/update PHP packages by `composer.json`
    ```shell
    # Install/update PHP packages by `composer.json`
    docker compose exec cp_cms composer install
    # The first time you run it, it will rebuild all tables.
    docker compose exec cp_cms cim
    # Import the listed configuration changes? (yes/no) [yes]: yes
    ```
    The first time you run it, 
    it will rebuild all tables.
    ```shell
    docker compose exec cp_cms drush cim
    ```

### Drupal Admin

    http://127.0.0.1:8080/user/login

    user: xxx
    password: xxx

    ```shell
    docker compose exec cp_cms drush user:password admin "admin"
    #  [success] Changed password for admin.

    Reset admin password when init or lost
    ```shell
    docker compose exec cp_cms drush user:password admin "admin"
    #  [success] Changed password for admin.
    ```

    http://127.0.0.1:8080/ → content → Add content
    http://127.0.0.1:8080/admin/content
    http://127.0.0.1:8080/node/1

### JSON:API

https://jsonapi.org/

> specification for how a client should request that resources be fetched or modified, and how a server should respond to those requests.

Drupal's datastructures, i.e. entity types, bundles, and fields, are incredibly well suited to the JSON:API.

example response
```json
{
  "links": {
    "self": "http://example.com/articles",
  },
  "data": [{
    "type": "articles",
    "id": "1",
    "attributes": {
      "title": "JSON:API paints my bikeshed!"
    },
    "relationships": {
      "author": {
        "links": {
          "self": "http://example.com/articles/1/relationships/author",
          "related": "http://example.com/articles/1/author"
        },
        "data": { "type": "people", "id": "9" }
      },
    },
    "links": {
      "self": "http://example.com/articles/1"
    }
  }],
  "included": [{
    "type": "people",
    "id": "9",
    "attributes": {
      "firstName": "Dan",
    },
    "links": {
      "self": "http://example.com/people/9"
    }
  }]
}
```

### Filtering

* detail with related content

  GET http://127.0.0.1:8080/jsonapi/node/course/xxx?include=field_related_content

* list

  GET http://127.0.0.1:8080/jsonapi/node/course

* list pagincation

  GET http://127.0.0.1:8080/jsonapi/node/course?page[offset]=0&page[limit]=20

* list search

  GET http://127.0.0.1:8080/jsonapi/node/course?filter[title][operator]=CONTAINS&filter[title][value]=test

* list filter by status = true

  GET http://localhost:8080/jsonapi/node/course?filter[status]=1

* array.includes('value')

  GET http://127.0.0.1:8080/jsonapi/node/course?filter[field_employee_list]=1528

* array=[]

  GET http://127.0.0.1:8080/jsonapi/node/course?filter[my-filter][condition][path]=field_employee_list&filter[my-filter][condition][operator]=IS NULL

* date>=today

  GET http://127.0.0.1:8080/jsonapi/node/course?filter[field_activated_date][operator]=%3E&filter[field_activated_date][value]='2024-04-12T18:46:30.954Z'

* group filter: (field_publish_status= 'draft' and field_created_by='tester') or (field_publish_status='published')

  GET http://127.0.0.1:8080/jsonapi/node/course?
  &filter[and-group][group][conjunction]=AND
  &filter[or-group][group][conjunction]=OR
  &filter[and-group][group][memberOf]=or-group

  &filter[published-filter][condition][path]=field_publish_status
  &filter[published-filter][condition][value]=published
  &filter[published-filter][condition][memberOf]=or-group

  &filter[draft-filter][condition][path]=field_publish_status
  &filter[draft-filter][condition][value]=draft
  &filter[draft-filter][condition][memberOf]=and-group

  &filter[created-by-filter][condition][path]=field_created_by
  &filter[created-by-filter][condition][value]=tester
  &filter[created-by-filter][condition][memberOf]=and-group

  ```json
  {
    "filter": {
      "and-group": {
        "group": {
          "conjunction": "AND",
          "memberOf": "or-group"
        }
      },
      "or-group": {
        "group": {
          "conjunction": "OR"
        }
      },
      "published-filter": {
        "condition": {
          "path": "field_publish_status",
          "value": "published",
          "memberOf": "or-group",
        }
      },
      "draft-filter": {
        "condition": {
          "path": "field_publish_status",
          "value": "draft",
          "memberOf": "and-group",
        }
      },
      "created-by-filter": {
        "condition": {
          "path": "field_created_by",
          "value": "tester",
          "memberOf": "and-group",
        }
      }
    }
  }
  ```

  https://www.drupal.org/docs/core-modules-and-themes/core-modules/jsonapi-module/filtering

* sort

  GET http://127.0.0.1:8080/jsonapi/node/compliance_policy?sort[sort_author][path]=changed&sort[sort_author][direction]=DESC

* create

  POST http://127.0.0.1:8080/jsonapi/node/course
  content-type: application/vnd.api+json

  {
    "data": {
      "type": "node--course",
      "attributes": {
        "title": "Test",
      },
      "relationships": {
        "field_related_content": {
          "data": [
            {
              "type": "node--exam",
              "id": "xxx"
            }
          ]
        }
      }
    }
  }

### Axios

```js
let api = `${hosts.businessCMS}/api/content/${type}`;
	try {
		const response = await axios.get(api, {
			params: {
        page,
				limit,
				filter, // 自动将object形式的filter转化为中括号字符串
				sort,
			},
		});
    console.info(">>> cms-api get:", hosts.businessCMS, response.request?.path);
		return response.data;
	} catch (error) {
		throw error;
	}
```