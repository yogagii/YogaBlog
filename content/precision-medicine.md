Title: Precision Medicine -- iDiscover Data Platform
Date: 2023-11-08
Category: Project
Author: Yoga

## Business Value

Roll out a CRM platform specific to diagnostic labs in iConnect to:

• Enable field force teams to capture and create shared visibility of critical lab information, account manage, set objectives for each lab and associated HCP accounts across TAs

• Enable TA leaders and brand teams to understand current testing practice and uptake

## Data Flow

* Ingest objects from iConnect to iDiscover

* Conduct data transformation in Redshift

> Data Source (Salesforce) -> Data Ingestion (Data Lake - S3 Bucket) -> Data Transformation (Data Warehouse - Amazon Redshift) -> Data Consumption (Tableau)

### Dag: SFDC -> S3

**send_email_cluster_start >> emr_tasks[0] >> emr_tasks[1] >> emr_tasks[2] >> emr_tasks[3] >>  emr_tasks[4] >> send_email_cluster_termination >> end**

* S3 Bucket
    * context: 配置环境变量
    * metadata: 配置字段表
    * metadata/delta_filter: 配置增量字段
    * status: 生成日志文件
    * source: 存储目标文件(csv)
    * archive: 存储历史文件
    * script: 部署代码
* Secrets Manager
    * data source (SFDC) credentials
    * data target (s3) credentials
* Managed Apache Airflow
    * Dags: job list
    * Admin/Variables: dna_env_variables
* EMR
    * EMR on EC2/Clusters: 查看集群日志
* CloudWatch
    * Logs group: 运行日志
* Salesforce: iConnect DB
* Postgre: job metadata
* Bitbucket: 生成dags的python script
* Jenkins: CICD

Amazon Managed Workflows for Apache Airflow (MWAA) 是一项适用于 Apache Airflow 的托管编排服务

EMR适合跨平台的操作，可以发挥他的集群优势和算力优势；warehouse 内部操作 RS -> RS 去EMR绕一圈性能和性价比都很低，S3 -> Redshift都属于aws范畴内

### Dag: S3 -> Redshift

### Dag: Redshift -> Redshift

* stg -> itg
* itg -> dm
* dm -> dm

t1 >> end

* S3 Bucket
    * metadata: 配置sql语句，按country_code delete目标表数据，并插入新数据（调用存储过程）
* Redshift
    Procedure: LANGUAGE plpgsql

## Control-M

Control-M是BMC Software提供的企业级集中作业调度管理解决方案

建立工作流：将需要执行的任务按照逻辑顺序组织成一个工作流。

定义任务：针对不同的任务，可以给出各自相应的调度规则并指定参数。

创建日历：可设置各种类型的调度日历，来约束任务的执行时间。

配置资源：可为任务分配特定的资源，如服务器、数据库等。

运行和监控：将定义好的工作流提交到Control-M服务器上，系统会按照设定好的规则进行执行，并且实时监控任务的执行情况和运行状态。

https://blog.csdn.net/2301_76522810/article/details/131143824
