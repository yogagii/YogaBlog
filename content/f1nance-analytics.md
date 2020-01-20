Title: F1nance recommend system
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

根据用户浏览workbook数据聚类，把与用户常看相同一类workbooks的人，也喜欢看的其他workbooks推荐给用户

COS对象耦合性算法：名词性问题相似度计算，完整的表述是（Coupled Object Similarity，即COS

缺点：只能定性聚类，不能分析出喜欢程度的不同

## 冷启动

首次登录的用户没有浏览的历史记录，不能做聚类分析，根据Role, Sector, Region给用户打标签，根据"啤酒与尿布"的原理，相同标签的用户如果在看A类workbooks时也会看B类workbooks，则将AB两类workbooks一起推荐给新用户

关联规则挖掘算法：
* apriori
* association rules learning