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