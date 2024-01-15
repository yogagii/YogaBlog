Title: Reinforcement learning
Date: 2024-01-15
Category: Analytics
Author: Yoga
Tags: ML

### Summit Training

Rule-based VS ML

* Rule-based approach: Decision rules are clearly defined by humans

* Machine Learning: Trained from examples. Rules are note defined by humans but learned by the machine fron data.

AI VS ML VS DL

* Artificial Intelligence: A concept of machines to make human intelligence. Ability to solve different kinds of work from managing schedule to analyizing marketing trends.

* Machine Learning: A method for computers to learn from data. A scale in making prediction based on past experience. Using past sales data and learn to predict future sales trends baesd on patterns it observes.

    1. Supervised Learning: learn the relationship of given inputs to a given output
        * linear regression
        * logistic regression (output is binary)
        * naive bayes
        * support vector machine (non linear problem)
        * ada boost
        * decision tree
        * random forest
        * simple neural network
    2. Un-supervised Learning: without and explicit output
        * K Means Clustering: puts data into groups
        * Hierarchal Clustering
        * Gaussian Mixture 
        * Recommender System
        * Apriori algorithm
    3. Reinforcement Learning: learning through interaction with an environment and rewards/punishments

* Deep Learning: Specialized technique using neural networks to process data deeply A specialty in deeply analysizing data to understand even a tiniest enfluences on sales. Not just understang which product sales well, but also recognizing many patterns, such as how weather changes might influence sales.

---

种群的勘探(Exploration)与开发(Exploitation)

Exploration：当算法发散时，种群个体之间维数值的差异增大，意味着种群个体在搜索环境中是分散的。通过Exploration，算法能够访问搜索环境中不可见的邻域，以最大限度地提高找到全局最优位置的效率。

Exploitation：当种群收敛时，差异减小，种群个体聚集到一个集中区域。Exploitation可以使群体个体成功地收敛到一个潜在的领域，并极有可能获得全局最优解。

https://blog.csdn.net/jieyanping/article/details/129189230
