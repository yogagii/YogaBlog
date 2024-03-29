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

---

### Hyperparameter 超参数

* gradient descent batch size: 64 梯度下降样本数
* number of epochs: 10 迭代次数
* learning rate: 0.0003 学习率（初次训练0.01尽快到最优解附近，后续训练降低学习率微调）
* entropy: 0.01 熵
* discount factor: 0.999 折扣率 learning rate = epoch * discount factor 使学习率逐渐下降
* loss type: huber

### Action space
* continus action space 连续 (由算法决定)
    * steering angel range: -30 - 30 转弯角度范围（取决于地图）
    * speed: 0.1 - 4 速度范围
* discrete action space 离散 (手动输入：角度越大，速度越慢)

https://github.com/dgnzlz/Capstone_AWS_DeepRacer/blob/master/Compute_Speed_And_Actions/RaceLine_Speed_ActionSpace.ipynb

### Reward function

https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-reward-function-input.html#reward-function-input-distance_from_center

* Follow the center line in time trials
```js
if distance_from_center <= marker_1:
    reward = 1
elif distance_from_center <= marker_2:
    reward = 0.5
elif distance_from_center <= marker_3:
    reward = 0.1
else:
    reward = 1e-3  # likely crashed/ close to off track

return reward
```

* Stay inside the two borders in time trials
```js
if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
    reward = 1.0
```

* Prevent zig-zag in time trials
```js
# Steering penality threshold, change the number based on your action space setting
ABS_STEERING_THRESHOLD = 15 

# Penalize reward if the car is steering too much
if abs_steering > ABS_STEERING_THRESHOLD:
    reward *= 0.8
```

Params dictionary
```python
{
    "all_wheels_on_track": Boolean,        # flag to indicate if the agent is on the track
    "x": float,                            # agent's x-coordinate in meters
    "y": float,                            # agent's y-coordinate in meters
    "distance_from_center": float,         # distance in meters from the track center 
    "is_left_of_center": Boolean,          # Flag to indicate if the agent is on the left side to the track center or not. 
    "is_offtrack": Boolean,                # Boolean flag to indicate whether the agent has gone off track.
    "is_reversed": Boolean,                # 反向
    "heading": float,                      # 朝向
    "progress": float,                     # progress尽可能大，steps尽可能小
    "steps": int,                          # 1 秒15个steps
    "speed": float,                        # agent's speed in meters per second (m/s)
    "steering_angle": float,               # 轮子角度
    "track_length": float,                 # 轨道长度
    "track_width": float,                  # 轨道宽度
    "closest_waypoints": [int, int],       # 最近的两点
    "waypoints": [(float, float), ]        # 地图信息
}
```

原始轨道：https://github.com/aws-deepracer-community/deepracer-race-data/tree/main/raw_data/tracks

最优路径：https://github.com/cdthompson/deepracer-k1999-race-lines

```python
## Define the default reward ##
reward = 1

progress = params['progress']
steps = params['steps']
TOTAL_NUM_STEPS = 10 * 15
if (steps % 15) == 0 and progress/100 > (steps/TOTAL_NUM_STEPS):
    reward += 2.22 #for each second faster than 45s projected
    # reward += progress - (steps/TOTAL_NUM_STEPS)*100

## Reward if car goes close to optimal racing line ##
DISTANCE_MULTIPLE = 2.5
dist = dist_to_racing_line(optimals[0:2], optimals_second[0:2], [x, y])
distance_reward = max(1e-3, 1 - (dist/(track_width*0.5)))
reward += distance_reward * DISTANCE_MULTIPLE

## Reward if speed is close to optimal speed ##
SPEED_DIFF_NO_REWARD = 1
SPEED_MULTIPLE = 2
speed_diff = abs(optimals[2]-speed)
if speed_diff <= SPEED_DIFF_NO_REWARD:
    # we use quadratic punishment (not linear) bc we're not as confident with the optimal speed
    # so, we do not punish small deviations from optimal speed
    speed_reward = (1 - (speed_diff/(SPEED_DIFF_NO_REWARD))**2)**2
else:
    speed_reward = 0
reward += speed_reward * SPEED_MULTIPLE


# Zero reward if obviously wrong direction (e.g. spin)
direction_diff = racing_direction_diff(
    optimals[0:2], optimals_second[0:2], [x, y], heading)
if direction_diff > 30:
    reward = 1e-3
    
# Zero reward of obviously too slow
speed_diff_zero = optimals[2]-speed
if speed_diff_zero > 0.5:
    reward = 1e-3
    
## Incentive for finishing the lap in less steps ##
REWARD_FOR_FASTEST_TIME = 500 # should be adapted to track length and other rewards
STANDARD_TIME = 12  # seconds (time that is easily done by model)
FASTEST_TIME = 9  # seconds (best time of 1st place on the track)
if progress == 100:
    finish_reward = max(1e-3, (-REWARD_FOR_FASTEST_TIME /
                (15*(STANDARD_TIME-FASTEST_TIME)))*(steps-STANDARD_TIME*15))
else:
    finish_reward = 0
reward += finish_reward

## Zero reward if off track ##
if all_wheels_on_track == False:
    reward = 1e-3
```

Best-route strategy: https://github.com/dgnzlz/Capstone_AWS_DeepRacer

AWS Deepracer Community: https://github.com/aws-deepracer-community/deepracer-analysis

https://zhuanlan.zhihu.com/p/635604595?utm_id=0
