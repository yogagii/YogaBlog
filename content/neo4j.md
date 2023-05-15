Title: NEO4J
Date: 2023-04-28
Category: Backend
Tags: database
Author: Yoga

## Neo4j Desktop

https://neo4j.com/download/

## 图数据库

Neo4j是一个高性能的,NOSQL图形数据库，它将结构化数据存储在网络上而不是表中。

图是一组节点和连接这些节点的关系。 
在Neo4j中，节点和关系都可以包含属性。

* 节点 Node
* 关系 Relationship
    * 一个关系连接两个节点，必须有一个开始节点和结束节点。
    * 关系具有方向：单向和双向。
    * 关系可以将节点组织成任意的结构
* 属性
    * 节点和关系都可以设置自己的属性。
    * 属性是用于表示数据的键值对。
    * 属性值是要么是原始值，要么是原始值类型的一个数组。

* 遍历 Traversal
    * 进行数据库查询：通过一种算法，从一些开始节点开始查询与其关联的节点

* 路径
    * 路径由至少一个节点，通过各种关系连接组成
    * 经常是作为一个查询或者遍历的结果。

为节点和关系建立索引：通过某一给定的属性值找到节点或者关系。

## CQL

* CREATE 创建节点、关系、标签

创建一个没有属性的节点
```SQL
CREATE (<node-name>:<label-name>) --节点名:标签名，可有多个标签名

CREATE (emp:Employee)
```
创建具有属性的节点
```SQL
CREATE (
  <node-name>:<label-name>
  { 	
    <Property1-name>:<Property1-Value>
    ........
    <Propertyn-name>:<Propertyn-Value>
  }
)

CREATE (emp:Employee{id:123,name:"Lokesh"})

CREATE (:Person { name:'Tester',age:10 })
```
单个标签到关系
```SQL
CREATE (<node1-name>:<label1-name>)-
	[<relationship-name>:<relationship-label-name>]
	->(<node2-name>:<label2-name>)

CREATE (p1:Profile1)-[r1:LIKES]->(p2:Profile2)
```

* MATCH 获取节点，关系和属性的数据

```SQL
MATCH (n:Person { name:'Tester',age:10 }) RETURN n

-- where
MATCH (p:Person)
WHERE p.name = "Tester"
RETURN p

-- 返回部分属性
MATCH (dept: Dept)
RETURN dept.deptno,dept.dname
```

* WHERE

```SQL
WHERE emp.name = 'Abc' OR emp.name = 'Xyz'

MATCH (cust:Customer),(cc:CreditCard) 
WHERE cust.id = "1001" AND cc.id= "5001" 
CREATE (cust)-[r:DO_SHOPPING_WITH{shopdate:"12/12/2014",price:55000}]->(cc) 
RETURN r
```
_Warning: 
This query builds a cartesian product between disconnected patterns._

_笛卡尔积警告: 时间复杂度为(number of Foo nodes) x (number of Bar nodes)_

created the index: uses a WITH clause to force the first MATCH clause to execute first, avoiding the cartesian product.

* DELETE 删除节点、关系

```SQL
DELETE <node-name-list> -- 用逗号分隔节点名

MATCH (e: Employee) DELETE e

MATCH (cc: CreditCard)-[rel]-(c:Customer) 
DELETE cc,c,rel
```

* REMOVE 删除属性、标签

```SQL
REMOVE <property-name-list>

MATCH (book { id:122 })
REMOVE book.price -- 删除属性
RETURN book

MATCH (m:Movie) 
REMOVE m:Picture -- 删除标签
```

* SET 添加、更新属性

```SQL
MATCH (book:Book)
SET book.title = 'superstar'
RETURN book
```

* ORDER BY 排序

```SQL
ORDER BY <property-name-list> [DESC] -- 默认升序ASC

match (c:Customer) return c ORDER BY c.id DESC
```

* UNION 合并

---
## Nestjs

```bash
npm install neo4j-driver nest-neo4j
```

```ts
// app.module.ts
import { Module } from '@nestjs/common';
import { Neo4jModule } from 'nest-neo4j';

@Module({
  imports: [
    Neo4jModule.forRootAsync({
      imports: [ConfigModule],
      useFactory: () => ({
        scheme: 'neo4j',
        host: 'xxx.xxx.com', // 踩坑：不要带neo4j://
        port: 7687,
        username: process.env.DATABASE_N4_USERNAME,
        password: process.env.DATABASE_N4_PASSWORD,
        database: process.env.DATABASE_N4_DATABASE,
        config: {
          disableLosslessIntegers: true, 
        },
      }),
    }),
  ],
  controllers: [AppController],
  providers: [AppService]
})
export class AppModule {}
```

_disableLosslessIntegers：Integer常量池--low,high限定范围。Enabling this option can result in a loss of precision and incorrect numeric values being returned if the database contains integer numbers outside of the range [Number.MIN_SAFE_INTEGER, Number.MAX_SAFE_INTEGER]._

```ts
import { Injectable } from '@nestjs/common';
import { Neo4jService } from 'nest-neo4j/dist';

@Injectable()
export class SupplyLaneService {
  constructor(private readonly neo4jService: Neo4jService) {}

  findAll() {
    return this.neo4jService
      .read(
        `
          match (src:xx) -[r:xx]->(dst:xx) return src,r,dst
        `,
      )
      .then((res) => {
        if (!res.records.length) return undefined;
        return res.records.map((record) => {
          src: record.get('src').properties,
          dst: record.get('dst').properties,
          lt: record.get('r').properties,
        });
      });
  }
}

```
