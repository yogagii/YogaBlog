Title: Microsoft Azure Databricks API
Date: 2023-05-15
Category: Cloud
Author: Yoga
Tags: Azure, ETL

https://docs.databricks.com/api-explorer/workspace/jobs

### Step1: Connection variables

Databricks workspace → User Settings → Access tokens tab → Generate new token.

* Personal_TOKEN: xxxxx

Compute → Cluster → Configuration → Advanced options → JDBC/ODBC

* Databricks_HOST: adb-xxx.azuredatabricks.net

* HTTP Path: sql/protocolv1/o/6201908139262714/xxxx

* Cluster_ID: xxxx

* Notebook_path: Databricks workspace → create a notebook → Copy file path

```python
import json;

key = dbutils.widgets.get("key")
dbutils.notebook.exit(json.dumps({
    "status": "ok",
    "params": key
}))
```

### Step2: Create and trigger a one-time run

POST https://adb-{{Databricks_HOST}}.azuredatabricks.net/api/2.1/jobs/runs/submit

Header: Authorization: Bearer Bearer {{Personal_TOKEN}}

可以用all-purpose cluster：existing_cluster_id：xxx

也可以用job cluster，job cluster会在job运行结束后停止且不能重启，需要每次创建 new_cluster

Body: 

```json
{
  "run_name": "Test_Run_postman",
  "existing_cluster_id": "{{Cluster_ID}}",
  "notebook_task": {
    "notebook_path": "{{Notebook_path}}",
    "base_parameters": {
      "key": "test_key"
    }
  },
  "timeout_seconds": 30, // Maximum completion time for this task. The default behavior is no timeout.
}
```

Result:

```json
{
  "run_id": 5455
}
```

### Step3: Get the output for a single run

GET https://adb-{{Databricks_HOST}}.azuredatabricks.net/api/2.1/jobs/runs/get-output?run_id=5455

Header: Authorization: Bearer Bearer {{Personal_TOKEN}}

注意如果是job的运行结果，run_id是Task run ID不能是Job run ID

Result:
```json
{
  "metadata": {
    "job_id": 727829565007789,
    "run_id": 5455,
    "state": {
      "life_cycle_state": "TERMINATED",
      "result_state": "SUCCESS",
      // ...
    },
    // ...
  },
  "notebook_output": {
    "result": "{\"status\": \"ok\", \"params\": \"test_key\"}",
  }
}
```

* 超时：

Maximum completion time for this task. The default behavior is no timeout. If you configure both Timeout and Retries, the timeout applies to each retry.

If the task does not complete in this time, Azure Databricks sets its status to “Timed Out”.

  life_cycle_state: “TERMINATED”,

  result_state: “TIMEDOUT”

* 并发：

A workspace is limited to 1000 concurrent task runs. A `429 Too Many Requests` response is returned when you request a run that cannot start immediately.

The number of jobs a workspace can create in an hour is limited to 10000 (includes “runs submit”). This limit also affects jobs created by the REST API and notebook workflows.

Maximum concurrent runs: Set this value higher than the default of 1 if you want to be able to perform multiple runs of the same job concurrently.

* 通知：

配置里面只能写死邮箱，不能根据谁提交的job就把邮件发给谁

You can monitor job runs by configuring notifications when a job run starts, completes successfully, or fails. Notifications can be sent to one or more email addresses or system destinations such as webhook destinations or Slack.

* 集群：

all-purpose cluster可以设定关闭时间，Job Clusters的话job跑完就关了

get out-put 接口不会触发集群启动就能拿到结果

The Azure Databricks job scheduler creates *a job cluster* when you run a [job](https://learn.microsoft.com/en-us/azure/databricks/workflows/jobs/create-run-jobs) on a *new job cluster* and terminates the cluster when the job is complete. You *cannot* restart a job cluster.

**New Job Clusters** are dedicated clusters for a job or task run. A shared job cluster is created and started when the first task using the cluster starts and terminates after the last task using the cluster completes. The cluster is not terminated when idle but terminates only after all tasks using it have completed. 

https://learn.microsoft.com/en-us/azure/databricks/workflows/jobs/use-compute

---

### Databricks SQL Driver for Node.js

https://docs.databricks.com/dev-tools/nodejs-sql-driver.html

npm i @databricks/sql

```ts
import { DBSQLClient } from '@databricks/sql';
import IDBSQLSession from '@databricks/sql/dist/contracts/IDBSQLSession';
import IOperation from '@databricks/sql/dist/contracts/IOperation';

const client: DBSQLClient = new DBSQLClient();

client.connect(
  {
    host:  process.env.DATABRICKS_SERVER_HOSTNAME,
    path:  process.env.DATABRICKS_HTTP_PATH,
    token: process.env.DATABRICKS_TOKEN
  }).then(
    async client => {
      const session: IDBSQLSession = await client.openSession();

      const queryOperation: IOperation = await session.executeStatement(
        'SELECT * FROM default.diamonds LIMIT 2',
        {
          runAsync: true,
          maxRows: 10000 // This option enables the direct results feature.
        }
      );

      const result = await queryOperation.fetchAll({
        progress: false,
        callback: () => {},
      });

      await queryOperation.close();

      console.table(result);

      await session.close();
      client.close();
}).catch((error) => {
  console.log(error);
});
```
