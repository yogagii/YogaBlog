Title: Smart Joint
Date: 2022-08-17
Category: Project
Tags: Deep Learning
Author: Yoga

## 模型算法

### Keras模型

在Keras中有两种深度学习的模型：序列模型（Sequential）和通用模型（Model）

* Sequential：是实现全连接网络的最好方式。序列模型各层之间是依次顺序的线性关系
* model：通用模型（函数式模型）可以设计非常复杂、任意拓扑结构的神经网络，例如有向无环网络、共享层网络等。相比于序列模型只能依次线性逐层添加，通用模型能够比较灵活地构造网络结构，设定各层级的关系。

```python
from keras.models import Sequential
from keras.layers import Dense, Activation
 
# 通过列表制定网络结构
layers = [Dense(128, activation="relu"),
   Dropout(0.1),
]
model = Sequential(layers)

# 逐层添加网络结构
model = Sequential()
model.add(Dense(128, activation="relu"))
model.add(Dropout(0.1))
```

### 构造神经网络的layers函数

* layers.Flatten 用来将输入“压平”，即把多维的输入一维化，常用在从卷积层到全连接层的过渡。Flatten不影响batch的大小。
* layers.Dense 构建全连接层

  units：int型，表示全连接层的输出维度

  activation：str型，表示激活函数，一般采用的是"relu"，其他激活函数见之前的博客中

* layers.Conv2D 用来形成卷积层
* layers.Dropout 是构建过拟合时采用的丢弃层

  rate：丢弃率，表示每次训练中该层的灭活比，一般值是0~1（1会报错）

* layers.MaxPooling2D 是构建采用最大池化方法的池化层
* layers.AveragePooling2D 是构建采用平均池化方法的池化层
* layers.Rescaling 主要是构建缩放层，进行归一化或者标准化


## 图像处理

读取图像

```python
from pylab import *

img=imread('../input/knee-dataset/3_400/3_400/9000099L.png')
print(str(img.flatten().tolist())[1:-1].replace(',',''))
```
imread(): 读取图像，返回值 Mat 类型 （二维数组）

flatten(): 降维，只能适用于numpy对象，即array或者mat，返回一个一维数组

tolist(): [a, b, ..., f] -> [a, ,b, c, d, e, f]

str(): list转str [1:-1] 去掉首位中括号

热图绘制
```python
plt.imshow(X_train[0].reshape(224,224),cmap='gray')
plt.show()
```

## 数据处理

os.walk() 方法用于通过在目录树中游走输出在目录中的文件名


json_normalize() 将半结构化JSON数据规范化为平面表
```python
label_file=open('../label_json/9000099L.json','r',encoding='utf-8')
jsonData = json.load(label_file)

pd.json_normalize(
    jsonData,
    record_path = ['shapes'], # 解析嵌套列表
    meta = ['imagePath'], # 增加字段
    errors = 'ignore' # key不存在时忽略系统报错
    max_level = 3 # 解析多层数据
)
```

df2=df1.T 转置

df.loc[[行号], [列号]] 获取整行/整列

df.drop(index=1) 删除行

df.isnull().any() 判断哪些列包含缺失值

df.value_counts() 对Series里面每个值进行计数并排序

Python基本数据类型：

整型int，浮点型float，字符串str，列表list，字典dict，集合set，元组tuple，布尔值bool



