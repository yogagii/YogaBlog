Title: AWS Redshift
Date: 2023-11-30
Category: Cloud
Tags: AWS
Author: Yoga

Amazon Redshift AZ64、LZO、ZSTD字段的支持类型

| Type Category | Type | LZO | SZTD | AZ64
| - | - | - | - | - |
SMALLINT | INT2 | Yes | Yes | Yes
INTEGER | INT、INT4 | Yes | Yes | Yes
BIGINT | INT8 | Yes | Yes | Yes
DECIMAL | NUMERIC | Yes | Yes | Yes
REAL | FLOAT4 | No | Yes | No
DOUBLE PRECISION | FLOAT、FLOAT8 | No | Yes | No
BOOLEAN | BOOL | No | Yes | No
CHAR | CHARACTER、NCHAR、BPCHAR | Yes | Yes | No
VARCHAR | NVARCHAR、BPCHAR、TEXT | Yes | Yes | No
DATE、TIMESTAMP |  | Yes | Yes | Yes