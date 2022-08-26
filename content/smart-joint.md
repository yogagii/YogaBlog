Title: Smart Joint
Date: 2022-08-17
Category: Project
Tags: Deep Learning
Author: Yoga

## 关键点检测

### Step1: Keras模型

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

### Step2: 构造神经网络的layers函数

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

### Step3: 编译

```python
model.compile(optimizer='adam', # 优化器
              loss='mean_squared_error', # 损失函数
              metrics=['mae']) # 网络评价指标

```

loss 损失函数：

* 回归损失函数
  * 均方差 mean_squared_error
  * 平均绝对误差 mean_absolute_error
  * Huber loss huber_loss
* 分类损失函数
  * 交叉熵损失函数 categorical_crossentropy
  * 合页损失 hinge

Metric 评价指标：
* mae -> history: mean_absolute_error, val_mean_absolute_error
* acc -> history: val_loss, val_acc, loss, acc

### Step4: 训练

```python
history = model.fit(X_train,y_train,epochs =10,batch_size = 256,validation_split = 0.2)
```
输入：
* x 输入的x值
* y 输入的y标签值
* batch_size 每次梯度更新的样本数即批量大小，默认为32
* epochs=1 迭代次数
* validation_split=0.0, 浮点数0-1之间，用作验证集的训练数据的比例

输出：

* history.epoch 训练轮数
* history.history 内容是由compile参数的metrics确定

### Step5: 预测

## 霍夫变换

霍夫变换是图像处理中识别几何形状（直线，圆，椭圆）的一种方法，核心思想是把笛卡尔坐标系中的点集映射到霍夫空间（极坐标系）的一个点上

```python
img = cv2.imread('circle.jpg')
# 将图像转换为灰度图像
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 高斯滤波降噪
gaussian_img = cv2.GaussianBlur(gray_img, (7, 7), 0)
# 利用Canny进行边缘检测
edges_img = cv2.Canny(gaussian_img, 80, 180, apertureSize=3)
# 自动检测圆
circles1 = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, 1, 1000, param1=100, param2=20, minRadius=5, maxRadius=95)
circles = circles1[0, :, :]
circles
```

## 边缘检测（模糊度）

Laplacian（拉普拉斯）算子是一种二阶导数算子，其具有旋转不变性，可以满足不同方向的图像边缘锐化（边缘检测）的要求。

blur the picture
```python
blur_img = cv2.blur(gray_img, (9,9)) # 均值滤波
median_img = cv2.medianBlur(gray_img, 9) # 中值滤波
gaussian_img = cv2.GaussianBlur(gray_img, (9,9), 0) # 高斯滤波
```

```python
def getImageVar( image ):
    img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
    return imageVar # 图像越清晰越大

img = cv2.imread('blur_hip.jpeg')
getImageVar(img)
```


## 图像处理

1. 读取图像

```python
from pylab import *

img=imread('../9000099L.png')
print(str(img.flatten().tolist())[1:-1].replace(',',''))
```
imread(): 读取图像，返回值 Mat 类型 （二维数组）

flatten(): 降维，只能适用于numpy对象，即array或者mat，返回一个一维数组

tolist(): [a, b, ..., f] -> [a, ,b, c, d, e, f]

str(): list转str [1:-1] 去掉首位中括号

```python
import cv2

img = cv2.imread('../hip_circle.jpeg')
print(img.shape) # (1978, 1152, 3)  彩色图3通道
```

2. 热图绘制
```python
fig=plt.figure(figsize=(4,3) # 图像大小
plt.imshow(X_train[0].reshape(224,224),cmap='gray')
plt.show()
```

在窗口中显示图像

```python
cv2.namedWindow("img",cv2.WINDOW_NORMAL)
cv2.imshow('img', edges_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

3. 添加文字

```python
cv2.putText(img, str(i), (123,456)), font, 2, (0,255,0), 3)
```
各参数依次是：图片，添加的文字，左上角坐标，字体，字体大小，颜色，字体粗细

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



