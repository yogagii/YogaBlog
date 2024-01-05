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
}),
TypeOrmModule.forRoot({
  name: 'db2' // 当连接多个db时需要name
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
  imports: [TypeOrmModule.forFeature([User], 'db2')],
  providers: [UsersService],
  controllers: [UsersController],
})

// users.service.ts
constructor(
  @InjectRepository(User, 'db2')
  private usersRepository: Repository<User>,
) {}
```

### 创建Entity

| 装饰器 | description | extr
| - | - | -
@Column | 添加表列 | @Column({ length: 100 })
@PrimaryColumn | 创建主列 | 每个实体必须至少有一个主键列
@PrimaryGeneratedColumn | 自动生成的列 | @PrimaryGeneratedColumn('uuid')
@CreateDateColumn | 创建时间 | _注意可能与手动写入 new Date()有时差_
@UpdateDateColumn | 更新时间

数据类型

```ts
@PrimaryColumn('varchar', { length: 36 }) // varchar(36)
sku_code: string; // 字符串

@Column()
lead_time: number; // 整数


@Column('float') // double is available for mysql, not mssql
bo_value: number; // 小数

@Column()
last_modified_date: Date;  // 日期
```

https://typeorm.io/entities#column-types-for-mssql

复合主键：拼合多列作为主键

```ts
@Entity()
export class FooBar {
  @PrimaryColumn()
  public fooid?: number;

  @PrimaryColumn()
  public barid?: number;

  @Column({ unique: true }) // 创建重复会报错，大小写不敏感
  email: string;

  @ManyToOne(type => Foo, foo => foo.fooBars)
  @JoinColumn({ name: "fooid"})
  public foo: Foo | null = null;

  @ManyToOne(type => Bar, bar => bar.fooBars)
  @JoinColumn({ name: "barid"})
  public bar: Bar | null = null;
}
```

_踩坑：拼合太多主键时报错 QueryFailedError: ER_TOO_LONG_KEY: Specified key was too long; max key length is 3072 bytes_
_解决: @PrimaryColumn('varchar', { length: 36 })_

### Repository

```ts
userRepository.find({
  select: ["firstName", "lastName"]
  join: {
    alias: "user",
    leftJoinAndSelect: {
      photo: "user.photos",
    }
  },
  where: [
    { 
      firstName: "Timber",
      region: region ? In(region.split(',')) : Not(IsNull()), // 多选过滤
    },
    { firstName: ILike(`%${name}%`), } // 模糊搜索，不区分大小写
  ] // or
  order: {
    name: "ASC",
    id: "DESC"
  },
  skip: 5,
  take: 10,
  cache: true // 缓存
});
```

_踩坑： 每个 entity 必须有 primaryColumn，当 primary 重复时，find 主键重复的行只会返回一遍，QueryBuilder 会全部返回，可以用复合主键让主键唯一_

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
    user.create_time
    hp.ecode,
    hp.ename  // 踩坑：报错信息不会告诉你此处不能有，
  `,
  )
  .where('user.id IN (:...userIdList)', { userIdList })
  .andWhere('user.create_time >= :START_DATE', { START_DATE })
  // .distinct(true)
  .limit(10)
  .getRawMany(),

// debug
const sql = this.usersRepository
  .createQueryBuilder('user')
  ...
  .getQuery();
console.log(sql);
```

使用查询构建器查询可以获得两种类型的结果：

* entities: getOne / getMany
* raw results: getRawOne / getRawMany

**子查询**

```ts
import { getConnection } from 'typeorm';

const posts = await getConnection()
  .createQueryBuilder()
  .select("user.name", "name")
  .from(subQuery => {
    return subQuery
      .select("user.name", "name")
      .from(User, "user")
  }, "user")
  .getRawMany();
```
踩坑：'getConnection' is deprecated. Connection was renamed to DataSource. Old Connection is still there, but now it's deprecated. 

```ts
import { InjectDataSource } from '@nestjs/typeorm';
import { DataSource } from 'typeorm';

constructor(
  @InjectDataSource('dadb')
  private datasource: DataSource,
) {}

const posts = await this.datasource
  .createQueryBuilder()
  ...
```

**插入**

```ts
const newSKUs = await this.ugSKUsRepository
  .createQueryBuilder()
  .insert()
  .values(skuList)
  .execute();
```

### 多对多关系

一个课程有多位讲师
```ts
// entities/event.ts
import {
  Column,
  Entity,
  PrimaryColumn,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToMany,
  JoinTable,
} from 'typeorm';
import { Doctor } from './doctor';

@Entity()
export class Event {
  @PrimaryColumn()
  event_id: string;

  @Column({ default: null }) // 默认值
  course_name: string;

  @ManyToMany(() => Doctor, (doctor) => doctor.events)
  @JoinTable() // 指定这是关系的所有者方
  doctors: Doctor[];

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
```

一个讲师可以上多门课程
```ts
// entities/doctor.ts
import { Event } from './event';

@Entity()
export class iqvia_doctor {
  @PrimaryColumn()
  doctor_id: string;

  @Column()
  name: string;

  @ManyToMany(() => Event, (event) => event.doctors, {
    onDelete: 'CASCADE', // 删除讲师时会删除对应关系
  })
  events: Event[];
}
```
运行后，ORM 将创建Event_doctors_Doctor联结表。

_有关联的数据若需要删除，建议用flag标记而不是直接删除，若不加‘CASCADE’，直接删除时会报 Cannot delete or update a parent row: a foreign key constraint fails_

创建数据

```ts
doctor = new iqvia_doctor();
doctor.doctor_id = '1';
doctor.name = 'Doctor1';
doctorList.push(doctor);
await this.doctorRepository.save(doctor);

event = new iqvia_event();
event.event_id = '588873';
event.course_name = 'Wound Clousure';

event.doctors = doctorList;

await this.eventRepository.save(event);

const eventWithDoctor = await this.eventRepository.findOne('588873', {
  relations: ['doctors'],
  where: {
    doctors: {
      first_name: 'Yoga' // 过滤关联表
    }
  }
});
```

### 一对多关系

一个城市有多家医院
```ts
// entities/city.ts
import { Entity, PrimaryColumn, OneToMany } from 'typeorm';
import { Hospital } from './hospital';

@Entity()
export class City {
  @PrimaryColumn()
  city_name: string;

  @OneToMany(() => Hospital, (hospital) => hospital.city)
  hospitals: Hospital[];
}
```

一家医院只能在一个城市
```ts
// entities/hospital.ts
import { Entity, PrimaryColumn, Column, ManyToOne, JoinColumn } from 'typeorm';
import { City } from './city';

@Entity()
export class Hospital {
  @PrimaryColumn()
  hco_code: string;

  @Column()
  hco_name: string;

  @ManyToOne(() => City, (city) => city.hospitals)
  @JoinColumn({ name: 'city_name' })
  city: City;
}
```

创建数据
```ts
const city = new iqvia_city();
city.city_name = '枣庄';
await this.cityRepository.save(city);

const hospital = new iqvia_hospital();
hospital.hco_code = 'MDMC1';
hospital.hco_name = '中山医院';
hospital.city = city;
await this.hospitalRepository.save(hospital);

const city_list = await this.cityRepository.findOne('枣庄', {
  relations: ['hospitals'],
});
```

_踩坑：entity 修改后报错 TypeORM Error: Entity metadata for Users#majors was not found. Check if you specified a correct entity_

My guess is that the strict equals (===) is colliding with a cache and thinking that the different relative import paths refer to different classes.
先从其他路径引入Entity，成功后可改回原路径
```ts
// src/entities.ts:
import { Users } from './userManagement/entities/users.entity';
import { Majors } from './userPreference/entities/majors.entity';

export { Users, Majors };

// userManagement/entities/users.entity
import { Majors } from 'src/entities'
```

https://stackoverflow.com/questions/59468756/error-object-metadata-not-found-after-adding-many-to-many-relationships

### 日志 Logging

* logging: true 启用所有查询和错误的记录
* logging: ["query", "error", "schema", "warn", "info", "log"] 启用不同类型的日志记录
* logging: "all" 启用所有日志记录

app.module.ts
```ts
import { CustomLogger } from './common/utils/customLogger';
@Module({
  imports: [
    TypeOrmModule.forRoot({
      ...
      logging: ['info'],
      logger: new CustomLogger(), // 使用自定义记录器
      maxQueryExecutionTime: 1, // 记录耗时长 > 1 的查询
    }), 
  ]
})
```
/common/utils/customLogger.ts
```ts
import { Logger, QueryRunner, QueryRunnerAlreadyReleasedError } from 'typeorm';

export class CustomLogger implements Logger {
  private queryTime = 0

  logQuery(query: string, parameters?: any[], queryRunner?: QueryRunner): void {
    const sql =
      query +
      (parameters && parameters.length
        ? ` -- PARAMETERS: ${JSON.stringify(parameters)}`
        : '');
    // console.log(`[Query] ${sql}`);
  }

  logQueryError(
    error: string,
    query: string,
    parameters?: any[],
    queryRunner?: QueryRunner,
  ): void {
    // console.error(`[Query Error] ${error}`);
  }

  logQuerySlow(
    time: number,
    query: string,
    parameters?: any[],
    queryRunner?: QueryRunner,
  ): void {
    this.queryTime += time;
    // console.warn(`[Query Slow] Execution time: ${time} ms - ${query}`);
    let tableName = '';
    if (query.includes('FROM') && query.includes('WHERE')) {
      tableName = query.split('FROM')[1].split('WHERE')[0];
    }
    console.warn(`[Query Slow] Execution time: ${time} ms - ${tableName} - ${this.queryTime}`);
    // 当前 query 耗时 - 查询表名 - 累计耗时
  }

  logSchemaBuild(message: string, queryRunner?: QueryRunner): void {
    // console.log(`[Schema Build] ${message}`);
  }

  logMigration(message: string, queryRunner?: QueryRunner): void {
    // console.log(`[Migration] ${message}`);
  }

  log(
    level: 'log' | 'info' | 'warn',
    message: any,
    queryRunner?: QueryRunner,
  ): void {
    // console.log(`[${level}] ${message}`);
  }

  logTransactionStart(queryRunner?: QueryRunner): void {
    // console.log(`[Transaction Start]`);
  }

  logTransactionCommit(queryRunner?: QueryRunner): void {
    // console.log(`[Transaction Commit]`);
  }

  logTransactionRollback(queryRunner?: QueryRunner): void {
    // console.log(`[Transaction Rollback]`);
  }
}
```

### 缓存 Cache

app.module.ts
```ts
TypeOrmModule.forRoot({
  synchronize: true, // 首次启用缓存时，必须同步数据库架构 
  cache: {
    duration: 1000 * 60, //  默认缓存生存期为1000 ms
  },
})
```

默认情况下，TypeORM 使用一个名为query-result-cache的单独表，并在那里存储所有查询和结果。
```ts
cache: {
  type: "database",
  tableName: "configurable-table-query-result-cache" // 配置表名
}
```
手动建表
```sql
-- mysql
CREATE TABLE `query-result-cache` (
  `id` int NOT NULL AUTO_INCREMENT,
  `identifier` varchar(255) DEFAULT NULL,
  `time` bigint NOT NULL,
  `duration` int NOT NULL,
  `query` text NOT NULL,
  `result` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

将缓存类型更改为"redis"
```ts
cache: {
  type: 'redis',
  options: {
    // host: 'localhost',
    // port: 6379
    url: 'redis://10.xx.xx.xx:6379'
  }
}
```
踩坑：host和post不生效, use redis url instead
```js
// node_modules/@redis/client/dist/lib/client/index.js
const { hostname, port, protocol, username, password, pathname } = new url_1.URL(url)
```

在query中启用缓存
```ts
const users = await connection.getRepository(User).find({
  where: { isAdmin: true },
  cache: true
});
```
踩坑：.query(’select * from table’) 原始 SQL 查询 无法缓存

```ts
async getLatestDate(): Promise<Date> {
  return new Date(
    (
      await this.workspaceRepository
        .createQueryBuilder()
        .select('max(last_modified_date) as date')
        .cache(60 * 1000 * 15) // 15min
        .getRawMany()
    )[0].date,
  );
}

const latestDate = await this.getLatestDate();
const totalWorkspace = await this.workspaceRepository.find({
  where: {
    last_modified_date: latestDate,
  },
  cache: true,
});
```
时间缓存踩坑：

1. 当本地和dev共用同一个redis时，不能缓存 max(last_modified_date)，本地得到的时间与dev得到的时间有时差，当用本地用dev缓存下的last_modified_date来执行 select * from sku_workspace where last_modified_date=@1 时，会缓存下空数据

2. 从缓存中取得的数据为字符串类型，写进 where 语句时需转换为 Date 类型 where: { last_modified_date: new Date(latestDate) }

3. new Date()获取到的时间类型为 'datetime' 精确到毫秒, 若数据库中 last_moified_date 类型为 'datetime2(7)' 精确到微秒，会使返回结果为空 
    ```ts
    @PrimaryColumn({ type: 'datetime2' })
    last_modified_date: Date;
    ```
    法一：修改数据库格式：
    ```sql
    ALTER TABLE sku_workspace ALTER COLUMN last_modified_date datetime;
    ```
    法二：获取到的时间减1秒
    ```ts
    latestDate.setMinutes(latestDate.getMinutes() - 1);
    // 原本获取的时间会丢失微秒的部分，直接用=匹配不上，得用>
    where: {
      last_modified_date: MoreThanOrEqual(latestDate),
    },
    ```