Title: Recommend system
Date: 2020-01-17
Category: Analytics
Tags: Algorithm
Author: Yoga

## 流程

ETL数据清洗(extract transfer 和load)
-> Feature engineering数据工程(高并发concurrency)
-> modeling建模 
-> data analysis 
-> data visualization数据可视化



## 热启动

> 核心：基于用户的协同过滤（Collaborative Filtering）找到和目标用户相似的用户,推荐该相似用户使用过但该用户没见过的物品。

User based: 根据用户浏览workbook数据聚类，把与用户常看相同一类workbooks的人，也喜欢看的其他workbooks推荐给用户

余弦相似度公式，衡量了用户向量i和用户向量j之间的向量夹角的大小，显然夹角越小，余弦相似度越大，用户相似度越大。

COS对象耦合性算法：名词性问题相似度计算，完整的表述是（Coupled Object Similarity，即COS)

X- 用户， y - 看表的次数 -> 多维向量在多维空间中的夹角越小则越相关

加权出推荐报表列表：其他用户和目标被推荐用户的相似度，加权各表的浏览次数，排序。

缺点：只能定性聚类，不能分析出喜欢程度的不同

## 冷启动

> 核心：关联性分析 association rules

首次登录的用户没有浏览的历史记录，不能做聚类分析，根据Period_day(1-25), Role(8), Sector(9), Region(5), Position(4)给用户打标签，根据"啤酒与尿布"的原理，相同标签的用户如果在看A类workbooks时也会看B类workbooks，则将AB两类workbooks一起推荐给新用户

数据池：

source: all users in portal

source format: people mask id, region, sector, function, role, finance day, viewed reports id


关联规则挖掘算法：

一般我们使用三个指标来度量一个关联规则，这三个指标分别是：支持度、置信度和提升度

- Support（支持度）：表示某个项集出现的频率，也就是包含该项集的交易数与总交易数的比例。
- Confidence（置信度）：表示当A项出现时B项同时出现的频率，记作{A→B}。置信度指同时包含A项和B项的交易数与包含A项的交易数之比。
- Lift（提升度）：指A项和B项一同出现的频率, 提升度>1且越高表明正相关性越高

apriori (support >= 5%)

association rules learning

回滚rollback：（查漏补缺）

* period_day 递减

* function_role 置空

* position

结果：一张完整的按上述纬度的recommendation_list

## 模型评估

问卷反馈 and RMSE（实际数和预测数 均方根误差）

rmse值在0.2-0.5之间,说明该模型能够较准确地预测数据,大于1就属于不正常,无法准确地预测数据,达到效果
