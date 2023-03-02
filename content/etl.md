Title: 数据仓库技术
Date: 2023-03-01
Category: Programming
Author: Yoga

\ | 数据仓库 | 数据湖
| - | - | -
特点 | 面向主题的、集成的、随时间变化的、非易失的数据集合 | 容量大、格式多
数据 | 来自事务系统、运营数据库和业务线应用程序的关系数据 | 来自 IoT设备、网站、移动应用程序、社交媒体和企业应用程序的非关系和关系数据
模式 | 写时模式，数据写入前已经定义好schema，更改schema成本较高 | 读时模式，数据在利用的时候再定义schema，灵活方便

## 数据血缘

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