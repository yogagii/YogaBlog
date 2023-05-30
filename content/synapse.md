Title: Synapse SQL
Date: 2023-5-30
Category: Backend
Tags: database
Author: Yoga


1. 无法插入多条数据

```sql
INSERT INTO "user_generated_events" (event_id)
VALUES
('1'), ('2')
```

error: QueryFailedError: Error: Parse error at line: 1, column: 325: Incorrect syntax near ','.

That's because Azure Synapse SQL does not support multi-row insert via the values constructor. 

解决1：union

One work around is to chain "select (value list) union all". Your pseudo SQL should look like so:

```sql
INSERT INTO "user_generated_events" (event_id)
select '1' union select '2';
```

解决2：逐行插入

```ts
return await Promise.all(
  skuList.map((record) => this.ugSKUsRepository.save(record)),
)
```

2. 不支持OFFSET

```sql
select * from <TABLE> OFFSET 10;
```

error: Incorrect syntax near 'OFFSET'.

解决1：
```sql
SELECT TOP (${pageSize}) * FROM (SELECT TOP(${skip}) * from <TABLE>)
```

解决2：totalResults.splice(skip, take)
