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
@CreateDateColumn | 创建时间
@UpdateDateColumn | 更新时间

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

  @ManyToMany(() => Event, (event) => event.doctors)
  events: Event[];
}
```
运行后，ORM 将创建Event_doctors_Doctor联结表。

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
