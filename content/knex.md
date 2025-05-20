Title: Knex
Date: 2024-04-15
Category: Backend
Tags: database
Author: Yoga

https://knexjs.org/guide/

Knex can be used as an SQL query builder. The primary target environment for Knex is Node.js.

```bash
$ npm install knex --save
$ npm install mysql2 # pg, mysql, mysql2, oracledb, sqlite3...
```

### Configuration Options

```ts
import { Knex, knex } from "knex";
import { readFileSync } from "fs";
import { join } from "path";

const certFile = readFileSync(join(__dirname, "../../../certs/RootCA.crt.pem"));

export function getClient() {
  const config: Knex.Config = {
    client: "mysql2",
    connection: {
      database: process.env.DB_NAME,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      host: process.env.DB_HOST,
      port: Number(process.env.DB_PORT),
      ssl: { ca: certFile },
    },
    pool: {
      min: 2,
      max: 10,
    },
    migrations: {
      directory: "./migrations",
      extension: "ts",
    },
  };
  return knex(config);
}

export function getDBClient<T extends {}>(
  config: IConfig,
  tableName: string,
  schema: string = config.db.schema
) {
  const clientConfig = getClient(config);
  return clientConfig<T>(tableName).withSchema(schema);
}
```

### Query Builder

https://knex.nodejs.cn/guide/query-builder.html

- select
- where / whereIn
- first
- distinct

```ts
async function getUserInfo(userid: string) {
  const config = await getConfig();
  const dbclient = getDBClient(config, "employee_table", config.db.userSchema);
  return dbclient.where("id", userid).select().first();
}
```

- groupBy
- max

```ts
knex.max('age', { as: 'a' })
knex.max('age as a')
knex.max({ a: 'age' })
```

- timeout

```ts
knex.select().from("books").timeout(1000, {
  cancel: true, // MySQL and PostgreSQL only
});
```

- insert

  A conflict occurs when a table has a PRIMARY KEY or a UNIQUE index on a row being inserted has the same value as a row which already exists in the table in those column(s). The default behaviour in case of conflict is to raise an error and abort the query.

```ts
dbclient
  .insert([
    {
      course_id: "1", // primary key
      user_id: "1", // primary key
      name: "test",
    },
  ])
  .onConflict(["course_id", "user_id"])
  .merge(); // 主键未存在insert，主键已存在upsert
```

- stream

```ts
// data package
async function getStreamByQuarter(quarter: string) {
  const config = await getConfig();
  const stream = getDBClient(config, "tablename")
    .distinct("id")
    .where("date", quarter)
    .stream();

  stream.on("error", async (error: Error) => {
    stream.destroy();
    throw new BaseError({
      code: "ACTION_STREAM_ERROR",
      message: `Error in process unsigned commitment data stream: ${JSON.stringify(
        error
      )}`,
    });
  });

  return stream;
}
```

- transaction

```ts
export async function dataSync() {
  await dbClient.transaction(async (trx) => {
    const tableExists = await trx.schema.hasTable(tableName);
    if (!tableExists) return;
    await trx(tableName).truncate();
    await syncTableStream(dbClient, trx, tableName as TableName);
  });
}
```

### Schema

- Create table: knex migrate:make createTableName

```ts
import { Knex } from "knex";

export async function up(knex: Knex): Promise<void> {
  return await knex.schema
    .withSchema(`${process.env.SCHEMA_NAME}`)
    .createTable("TABLE_NAME", (table) => {
      table.increments("id").primary(), table.string("name", 255).notNullable();
      table.string("email", 255);
    });
}

export async function down(knex: Knex): Promise<void> {
  return knex.schema
    .withSchema(`${process.env.SCHEMA_NAME}`)
    .dropTable("TABLE_NAME");
}
```

- Update table: knex migrate:make updateTableName

```ts
import { Knex } from "knex";

export async function up(knex: Knex): Promise<void> {
  return await knex.schema
    .withSchema(`${process.env.SCHEMA_NAME}`)
    .alterTable("TABLE_NAME", (table) => {
      table.datetime("updated_date").defaultTo(knex.fn.now()).notNullable();
    });
}

export async function down(knex: Knex): Promise<void> {
  return knex.schema
    .withSchema(`${process.env.SCHEMA_NAME}`)
    .dropTable("updated_date");
}
```

### DB Migration

```bash
knex migrate:make user_info # 新建文件
knex migrate:latest --env development # 同步数据库
```

```json
// packahes.json
"db-migration:migrate": "knex migrate:latest --env development"
```

```bash
npm run db-migration:migrate
npx dotenv -e .env.local npm run db-migration:migrate
```

_踩坑：若有冲突_
1. 删除所有不需要运行的文件
2. 删除cp_persona中knex_migrations表和knex_migrations_lock表

#### Deployment

```yaml
deploy:
  enabled: false
  type: multi
  parallel: false
  stages:
    dbMigration:
      enabled: false
      type: script
      script: project/_scm_jenkins/dbMigration.groovy
```

### Unit test
```js
const getByUser = async (user_id: string) => {
  try {
    return await getDBClient<DBSettings>("settings")
      .where("settings.user_id", user_id)
      .andWhere("settings.deleted_at", null)
      .leftJoin("types", "types.id", "settings.type_id")
      .leftJoin("values", "values.id", "settings.value_id")
      .select("settings.id")
      .select("settings.custom_value")
      .select("types.type")
      .select("values.value");
  } catch (error) {
    Logger.error("Data.Settings.get", error.message);
    throw new DataError(DataErrorType.DATABASE_ERROR, error);
  }
};
```
解决链式调用中多次select后返回mock数据的问题: 计数器实现
* 链式调用需要保持方法返回this
* 最终select需要返回Promise.resolve结果
```js
describe("getByUser", () => {
  it("should fetch settings by user ID", async () => {
    const mockSettings = [
      { id: 1, custom_value: "value1", type: "type1", value: "value1" },
    ];
    let selectCount = 0;
    const mockChainInstance = {
      where: jest.fn().mockReturnThis(),
      andWhere: jest.fn().mockReturnThis(),
      leftJoin: jest.fn().mockReturnThis(),
      select: jest.fn().mockImplementation(() => {
        selectCount++;
        return selectCount === 4
          ? Promise.resolve(mockSettings)
          : mockChainInstance;
      }),
    };
    (getDBClient as jest.Mock).mockReturnValue(mockChainInstance);

    const result = await Settings.getByUser(mockUserId);
    expect(result).toEqual(mockSettings);
    expect(getDBClient).toHaveBeenCalledWith("settings");
  });
});
```