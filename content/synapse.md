Title: Synapse SQL
Date: 2023-5-30
Category: Backend
Tags: database
Author: Yoga

## Synapse SQL

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

Error: Insert values statement can contain only constant literal values or variable references

insert语句中必须包含entity中定义的所有column！

2. 不支持OFFSET

```sql
select * from <TABLE> OFFSET 10;
```

error: Incorrect syntax near 'OFFSET'.

同理 只能find不能findOne

解决1：
```sql
SELECT TOP (${pageSize}) * FROM (SELECT TOP(${skip}) * from <TABLE>)
```

解决2：totalResults.splice(skip, take)

## Synapse vs Sql Server

Fundamentally Synapse is not built for transactional (web based/unpredictable) workloads – it’s built for OLAP .

Sql Server is built for OLTP/transactional workloads.

* Synapse performs extremely well for massive data volumes, by using clustered column stores & distributing data and CPU up to 60 nodes.
However, out largest datasets for SWIFT are around 90k. Synapse can handle Billions….
* We are not using/needing any distribution, hashing, clustered indexes for SWIFT.
* Synapse really needs a predictable workload to tune it appropriately, for example data loads 4 times a day, visulation reads (refreshes) also 4 times a day.
As we’re essentially pointing a website directly at this database – and letting users essentially trigger sql queries against it – the workload is unpredictably and aligns with a transactional workload requirement.
Synapse will bottleneck very quickly based on scale of users triggering queries. For example right now in production we can only handle 20 concurrent queries (DW500c):
https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/memory-concurrency-limits

| Service Level | Maximum concurrent queries | Min % supported for REQUEST_MIN_RESOURCE_GRANT_PERCENT | Cost USD per month |
| --- | --- | --- | --- |
| DW100c | 4 | 25% | 1100 (1.51 USD/hour) |
| DW200c | 8 | 12.5% |  |
| DW300c | 12 | 8% | 3307 (4.53 USD/hour) |
| DW400c | 16 | 6.25% |  |
| DW500c | 20 | 5% | 5511 (7.55 USD/hour) |

Synapse is a very expensive solution that will not give us the scalability we need.

* Sql Server can easily accommodate the data volumes we’ve seen to date.
* It is far more cost effective.
* It is far more scalable from a concurrency/user perspective.
* It also has a lot of things that can be done to optimise performance. Partitioning, indexing, ect..
* It is designed for OLTP workloads.

Regarding integration, nothing much needs to change from an web/backend perspective.
It should be as simple as a JDBC url change.
The underlying syntax for Synapse Vs. Sql Server is extremely similar. Perhaps the driver may need to be updated too…
