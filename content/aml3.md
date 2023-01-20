Title: Azure Machine Learning Studio - Notebooks
Date: 2023-01-19
Category: Cloud
Author: Yoga
Tags: Azure, ML

### Import all the required libraries and formatting.

```python
import pandas as pd
import numpy as np
import matplotlib.pylab as pylab
%matplotlib inline
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 20, 6
import warnings
import itertools
warnings.filterwarnings("ignore")
import pandas as pd
import statsmodels.api as sm
import matplotlib
```

### Load Workspace

```python
from azureml.core import Workspace
ws = Workspace.get(name="myworkspace", subscription_id='<subscription_id>', resource_group='myresourcegroup')

ws = Workspace.from_config()
ws.get_details()
```

### Load data to Workspace

```python
ds = ws.datasets['data_name']
df = ds.to_pandas_dataframe()
```

### 读取csv

```python
df_raw = pd.read_csv(filepath_or_buffer = './test.csv', header = 0)
```

### Upload data to container

```python
default_store = ws.get_default_datastore() 
greenTaxiData='csvdata/green/part-00000'

default_store.upload_files(
    [greenTaxiData], 
    target_path = 'green', 
    overwrite = True, 
    show_progress = True
)
```

### Show data

```python
df.head(5) # 显示前5行
df.dtypes # 表字段和类型
df.describe() # summary statistics: count, mean, std, min, max
combined_df.transpose() # 转置

df['Column'].min() # min
df['Column'].max() # max
```

### 数据清洗

```python
# 过滤空行
df1 = df_raw.dropna(axis=0, how="all", thresh=None, subset=None, inplace=False)
latlong_filtered_df1 = combined_df.dropna(subset=["field1", "field2"], axis = 0, how = "any")

# 重命名字段
green_df2 = green_df1.rename(
columns = {
    "cost": "field1", "distance": "field2",
})

# 保留有用字段
useful_columns = ["cost", "distance"]
green_df = green_df_raw[useful_columns]
green_df = green_df_raw[green_df_raw.columns[green_df_raw.columns.isin(useful_columns)]]

# Union两张表
combined_df = pd.concat([green_df, yellow_df], axis=0)

# 查找有空值的列
combined_df.isnull().any()
print(filtered_df.isnull().sum())

# 过滤行
filtered_df = df1[
    (df1['pickup_longitude'] <= -73.72) 
    & (filtered_df1['pickup_longitude'] >= -74.09)  
]

# 替换，填充
filtered_df['store_forward'] = filtered_df['store_forward'].replace([0], 'N')
filtered_df['store_forward'] = filtered_df['store_forward'].fillna('N')

# 删除列
df = df.drop(['pickup_second', 'dropoff_second'], axis=1)
```

### 数据格式转换

```python
# 数值类型
df['distance'] = df['distance'].replace(".00", '0').apply(pd.to_numeric, errors='coerce')

# 日期类型
df['Month'] = pd.to_datetime(df['Month'])
df["pickup_datetime"] = df["pickup_datetime"].apply(pd.to_datetime)

# 拆分date和time 8/12/2013 10:06
df['pickupday'] = [d.date() for d in df['pickup_datetime']]
df['pickuptime'] = [d.time() for d in df['pickup_datetime']]

df['pickup_weekday'] = df['pickup_datetime'].dt.dayofweek
df['pickup_month'] = df['pickup_datetime'].dt.month
df['pickup_hour'] = df['pickup_datetime'].dt.hour
df['pickup_minute'] = df['pickup_datetime'].dt.minute
df['pickup_second'] = df['pickup_datetime'].dt.second
```

### 导出csv

```python
final_df.to_csv("final_df.csv")
```

### Split data

```python
features_df = final_df[['pickup_weekday','pickup_hour', 'distance','passengers', 'vendor']] # 特征
label_df = final_df['cost'] # 标签

from sklearn.model_selection import train_test_split

feature_train, feature_test, label_train, label_test = train_test_split(features_df, label_df, test_size=0.2, random_state=223)
# flatten y_train to 1d array
label_train.values.flatten()
```

### auto-train 自动化训练

Used the automated machine learning to find the best run and the best fitted model

```python
automl_settings = {
    "iteration_timeout_minutes" : 10,
    "iterations" : 30, 
    "primary_metric" : 'spearman_correlation',
    "featurization" : 'auto', 
    "verbosity" : logging.INFO, 
    "n_cross_validations": 
}

from azureml.train.automl import AutoMLConfig

# local compute
automated_ml_config = AutoMLConfig(
    task = 'regression',
    debug_log = 'automated_ml_errors.log',
    blocked_models =['XGBoostRegressor'],
    path = '.',
    X = feature_train.values,
    y = label_train.values.flatten(),
    **automl_settings
)

# Run the experiment locally
from azureml.core.experiment import Experiment

experiment=Experiment(ws, 'myAutoMLRegressionExp2')
local_run = experiment.submit(automated_ml_config, show_output=True)

```

### 比较不同算法结果

```python
from azureml.widgets import RunDetails
RunDetails(local_run).show()

# 法一：View the run details in Job -> Models
# 法二：View the results in local run variable
children = list(local_run.get_children())
metricslist = {}
for run in children:
    properties = run.get_properties()
    metrics = {k: v for k, v in run.get_metrics().items() if isinstance(v, float)}
    metricslist[int(properties['iteration'])] = metrics

rundata = pd.DataFrame(metricslist).sort_index(1) # 按index横向排序
rundata

# 选取效果最好的模型
best_run, fitted_model = local_run.get_output()
print(best_run) #Print Run ID, Type and Status
print(fitted_model) #Print Pipeline
# 根目录下自动生成 model.pkl
```

### Train Model

自定义模型

```python
from sklearn.linear_model import ElasticNet
from azureml.core import run

regr = ElasticNet(random_state=0)
regr.fit(feature_train, label_train)

model = "ElasticNet int %.2f coefs %s" % (regr.intercept_, print(regr.coef_))

yhat_train = regr.predict(feature_train)
yhat_test = regr.predict(feature_test)
```

### Score Model

```python
label_predict = fitted_model.predict(feature_test.values)
```

### Evaluate Model

```python
from sklearn.metrics import mean_squared_error
from math import sqrt

rmse = sqrt(mean_squared_error(label_actual, label_predict))
rmse
```

### Save Model

```python
import joblib

joblib.dump(fitted_model, 'automl_model.pkl')
```

### Deploy Model

```python
from azureml.core.model import Model

# register a model
model = Model.register(
    model_path = "nyc_taxifare_elasticnet_model.pkl",
    model_name = "nyc_taxifare_elasticnet_mdl",
    tags = {'area' : "cost", 'type' : "regression"},
    description = "Regression model",
    workspace = ws
)

# List models registered in the workspace
model_list = Model.list(workspace=ws)
```
Scoring File
```python
%%writefile score.py # 创建文件

...
```
environment configuration (yml) file
```python
MyModelEnv = CondaDependencies.create(conda_packages=['scikit-learn'])
with open("nyc_taxifare_model_env.yml","w") as f:
    f.write(MyModelEnv.serialize_to_string())
```

```python
aciconfig = AciWebservice.deploy_configuration(...)
inference_config = InferenceConfig(...)
service = model.deploy(...)
service.wait_for_deployment(...)
```

### Test Webservice

```python
import requests

test_input2 = json.dumps({'data': [[2,4,15,3,5]]})

headers = {'Content-Type':'application/json'}
resp = requests.post(service.scoring_uri, test_input2, headers=headers)

prediction = json.loads(resp.text)
print(prediction)
```

