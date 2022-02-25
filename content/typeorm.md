Title: TypeORM
Date: 2022-2-15
Category: Backend
Tags: nest, database
Author: Yoga

## ORM（Object Relactional Mapping，对象关系映射）

ORM是一种解决面向对象与关系型数据库存在的互不匹配的现象的技术，实现面向对象技术和关系型数据库的一种映射。

ORM可以自动对Entity对象与数据库中的Table进行字段与属性的映射。

类---->表

类的属性------->表中的字段

类的对象------->表中的行

### ORM框架：

* Sequelize：基于promise的关系型数据库ORM框架，这个库完全采用javascript并且能够用在Node.JS环境中，易于使用。支持关系型数据库（MySQL/MSSQL/PostgreSQL/SQLite）

* TypeORM：采用TypeScript编写的基于node.js的ORM框架，支持使用ts或js(ES5,ES6,ES7)开发。 支持数据库：mysql & mariadb、postgresql、sqlite、sqlserver和oracle

* Bookshelf：基于knex的ORM框架

* Waterline：Sails框架衍生出来的ORM框架

* Mongoose：仅支持 MongoDB

## Nest 集成 TypeORM

为了与 SQL和 NoSQL 数据库集成，Nest 提供了 @nestjs/typeorm 包。Nest 使用TypeORM是因为它是 TypeScript 中最成熟的对象关系映射器( ORM )。

* forRoot: createConnection

```ts
TypeOrmModule.forRoot({
  type: 'mysql',
  host: config.host,
  port: 3306,
  username: config.username,
  password: config.password,
  database: config.database,
  entityPrefix: options?.entityPrefix ?? '',
  entities,
  synchronize: config.synchronize,
  ssl: config.ssl
    ? {
        rejectUnauthorized: true,
        ca: readFileSync(
          join(resolve(), 'private/DigiCertGlobalRootCA.crt.pem'),
        ),
      }
    : undefined,
  name: options?.name,
})
```
_踩坑：_

DBeaver配置:

SSL -> CA certificate -> 选择文件

驱动属性 -> enabledTLSProtocols: TLSv1,TLSv1.1,TLSv1.2

("TLS version used does not meet minimal requirements for this server")

(Client with IP address '199.65.xxx.xxx' is not allowed to connect to this MySQL server.)

* forFeature: 定义在当前范围中注册哪些存储库。这样，我们就可以使用 @InjectRepository()装饰器将 UsersRepository 注入到 UsersService 中
```ts
// users.module.ts
@Module({
  imports: [TypeOrmModule.forFeature([User])],
  providers: [UsersService],
  controllers: [UsersController],
})

// users.service.ts
constructor(
  @InjectRepository(User)
  private usersRepository: Repository<User>,
) {}
```

装饰器 | description | extr
| - | - | -
@Column | 添加表列 | @Column({ length: 100 })
@PrimaryColumn | 创建主列 | 每个实体必须至少有一个主键列
@PrimaryGeneratedColumn | 自动生成的列 |

### QueryBuilder

使用 QueryBuilder 构建几乎任何复杂性的 SQL 查询

```ts
this.usersRepository
  .createQueryBuilder('user')
  .leftJoinAndSelect(bc_r_hospital, 'hp', 'user.hospital_id = hp.id')
  .select(
    `
    user.id,
    user.real_name,
    hp.ecode,
    hp.ename  // 踩坑：报错信息不会告诉你此处不能有，
  `,
  )
  .getRawMany(),
```