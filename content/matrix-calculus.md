Title: Matrix Calculus
Date: 2018-10-20 16:03
Category: Math
Tags: matrix, calculus
Author: 张本轩
Summary: 这篇文章总结矩阵微积分中使用的一些公式

## Matrix Calculus 

### Vector-by-Vector

* $\frac{\partial a}{\partial x} = 0$
* $\frac{\partial x}{\partial x} = I$
* $\frac{\partial x}{\partial x} = A$
* $\frac{\partial x^TA}{\partial x} = A^T$
* $\frac{\partial au(x)}{\partial x} = a\frac{\partial u}{\partial x}$

### Scalar-by-Vector

* $\frac{\partial a^Tx}{\partial x} = a^T$
* $\frac{\partial u^Tv}{\partial x} = u^T\frac{\partial v}{\partial x} + v^T\frac{\partial u}{\partial x}$
* $\frac{\partial u^TAv}{\partial x} = u^TA\frac{\partial v}{\partial x} + v^TA^T\frac{\partial u}{\partial x}$
* $\frac{\partial x^TAx}{\partial x} = x^T(A^T + A)$

## Reference

[Matrix calculas](https://en.wikipedia.org/wiki/Matrix_calculus)