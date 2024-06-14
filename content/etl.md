Title: Data Governance
Date: 2023-03-01
Category: Programming
Author: Yoga

| \ | 数据仓库 | 数据湖
| - | - | -
特点 | 面向主题的、集成的、随时间变化的、非易失的数据集合 | 容量大、格式多
数据 | 来自事务系统、运营数据库和业务线应用程序的关系数据 | 来自 IoT设备、网站、移动应用程序、社交媒体和企业应用程序的非关系和关系数据
模式 | 写时模式，数据写入前已经定义好schema，更改schema成本较高 | 读时模式，数据在利用的时候再定义schema，灵活方便

## 数据血缘 Data Lineage

https://blog.csdn.net/u011487470/article/details/126767328

数据血缘是在数据的加工、流转过程产生的数据与数据之间的关系。提供一种探查数据关系的手段，用于跟踪数据流经路径。

组成：
* 数据节点
    * 流出节点：源端节点，数据提供方。
    * 中间节点：血缘关系中类型最多的节点，既承接流入数据，又对外流出数据。
    * 流入节点：终端节点，一般为应用层，例如可视化报表、仪表板或业务系统。
* 节点属性
    * 表名
    * 字段
    * 注释
    * 说明
* 流转路径
    * 数据流动方向： 通过箭头的方式表明数据流动方向
    * 数据更新量级： 数据更新的量级越大，血缘线条越粗，说明数据的重要性越高。
    * 数据更新频率： 数据更新的频率越高，血缘线条越短，变化越频繁，重要性越高。
* 流转规则
    * 数据映射： 不对数据做任何变动，直接抽取。
    * 数据清洗： 表现数据流转过程中的筛选标准。例如要求数据不能为空值、符合特定格式等。
    * 数据转换： 数据流转过程中，流出实体的数据需要进行特殊处理才能接入到数据需求方。
    * 数据调度： 体现当前数据的调度依赖关系。
    * 数据应用： 为报表与应用提供数据。

应用场景：
* 流程定位，追踪溯源：可视化方展示目标表的上下游依赖
* 确定影响范围：避免出现上游表的修改导致下游表的报错。
* 评估数据价值、推动数据质量：重点关注输出数量较多的数据节点
* 数据安全审计：下游数据的安全等级不应该低于上游的安全等级

## 数据治理 Data Governance

数据治理 是指对数据资产的管理活动行使权力和控制的活动集合(规划、监控和执行)。

从范围来讲，数据治理涵盖了从前端业务系统、后端业务数据库再到业务终端的数据分析，从源头到终端再回到源头，形成的一个闭环负反馈系统。

从目的来讲，数据治理就是要对数据的获取、处理和使用进行监督管理。

数据治理 由元数据、数据标准、数据质量、数据集成、主数据、数据资产、数据交换、生命周期、数据安全等组成。

Principles:

* Accountability: people for decisions and monitoring 数据认责管理
* Standardization: aligning on the same definitions and talking same language 数据标准化
* Transparency: understand the lifecycle of data 数据透明度

> Data source -> Azure Purview -> Data consumer

Azure Purview enables unified data governance: 

* Data Map: automate and manage metadata at scale 数据地图
    * Automated Data discovery 数据扫描
    * Automated Data Classification
    * Automated Lineage Extraction
    * Simplified Configuration & Management (web, api, sdk)
* Data Catalog: enable effortless discovery for data consumers
    * Self-service Search & Browse 数据搜索
    * Curated & Standardized Business Glossaries
    * Interactive Lineage Visualization
    * Simplified Data Curation and Stewardship
* Data Insights: access data usage across your organization
    * Data Asset Distribution 数据被不同部门访问频率 -> 分担成本
    * Business Glossary
    * Data Classification & Labelling 数据分类和打标
    * Data Location & Movement (in progress) 

Data source: On-prem / Cloud / Saas Application

Data consumer: SQL Server / Power BI / Azure SQL / Microsoft 365

Data Use Governance - Polices: 

* Access policy 数据读写权限
* Encryption policy 数据加密
* Data Movement & Sharing policy 数据分享权限

## Data Democratization 数据民主化

Data democratization is the ability for information in a digital format to be accessible to Subject Matter Expert in JSC and data analysts/scientists.

授予员工访问数据的权限，确保信息易于查找、检索和理解。使决策权掌握在员工手中，并为员工提供一些他们所需的信息以辅助他们优化工作。
