Title: 矩阵复习
Date: 2018-10-20 20:48
Category: Math
Tags: matrix
Author: 张本轩

## 一些有用的结论

* 实对称阵可以正交对角化
* 特征值 $\lambda_i$的几何重数是$(\lambda I-A)x=0$的基础解系的个数
* 特征值 $\lambda_i$的代数重数$n_i$是$|\lambda I-A|=\Pi_{i=1}^s(\lambda-\lambda_i)^{n_i}$
* 矩阵的行列式是所有特征值的乘积
* 矩阵的迹是所有特征值的和
* A可逆 $\leftrightarrow$ 0不是A的特征值
* 任何特征值的几何重数不超过其代数重数
* 相似矩阵具有相同的特征多项式，也具有相同的特征值

### 特征向量

* 属于不同特征值的特征向量线性无关
* n阶矩阵A可以对角化 $\leftrightarrow$ A有n个线性无关的特征向量 $\leftrightarrow$ $F^n$有一组由A的特征向量组成的基 $\leftrightarrow$ A的每个特征值的几何重数等于代数重数，特别的，若A有n个不同的特征值，则A可以对角化

### 空间

* 设$\alpha_1, \alpha_2, \cdots, \alpha_n$是一组标准正交基，则矩阵$Q=(\alpha_1, \alpha_2, \cdots, \alpha_n)$称为酉矩阵，实的酉矩阵称为正交矩阵
* 酉矩阵的逆矩阵是其共轭转置矩阵
* 正交矩阵的逆矩阵是其转置矩阵
* 复共轭对称矩阵称为Hermite矩阵
* Hermite矩阵的特征值都为实数，且属于不同特征值的特征向量彼此正交
* 设A是n阶Hermite矩阵，则下列条件等价
    - A正定
    - A的特征值均为正实数