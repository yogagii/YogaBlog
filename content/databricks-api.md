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
  }
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
