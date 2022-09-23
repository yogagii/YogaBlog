Title: Linux 服务器配置
Date: 2022-04-21
Category: Programming
Author: Yoga

## 安装node

1. 到 node 官网

http://nodejs.cn/download/

https://registry.npmmirror.com/binary.html?path=node/ 

去下载一个 linux 可用的 node 版本

2. 传输到服务器 /home/jyu36 并解压

```bash
xz -d node-v14.18.2-linux-x64.tar.xz
tar -xvf node-v14.18.2-linux-x64.tar
```

3. 软连接 (不确定是否必须)

ln -s /home/nodejs/node-v14.18.2-linux-x64/bin/npm /usr/local/bin
ln -s /home/nodejs/node-v14.18.2-linux-x64/bin/node /usr/local/bin

4. 配置环境变量

```bash
vi /etc/profile

export NODEJS_HOME=/home/v-jyu36/node-v14.18.2-linux-x64
export PATH=$PATH:$NODEJS_HOME/bin

source /etc/profile
```

## 安装git

```
yum -y install git 
git --version
```

## 安装pm2

```
npm install pm2 -g
```

## 操作

* 删除单行
```
dd
```

* 删除全部
```
dG
```

* 快速定位
```
/正则匹配
```
---

## 安装Anaconda

```bash
df -h # 查看磁盘空间
du -sh *

cd /home/v-jyu36/ # 不要用root安装
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh 
chmod +x Anaconda3-2022.05-Linux-x86_64.sh
./Anaconda3-2022.05-Linux-x86_64.sh
rm Anaconda3-2022.05-Linux-x86_64.sh

# 修改环境变量
vi ~/.bashrc
export PATH="/home/v-jyu36/anaconda3/bin:$PATH" 
source ~/.bashrc
which python # ~/anaconda3/bin/python 

# 安装包
pip install tensorflow

```
### Tmux

```python
# 安装分屏
sudo su -
sudo yum install tmux 
exit # 退出root

tmux new -s <session-name> # 新建会话
tmux split-window # 划分上下两个窗格
tmux select-pane -U # 光标切换窗格 
ctrl+b 方向键下 # 光标切换窗格 

ipython
%run YogaModel-ChopModel.py 

free # 查看内存
top # 观察cpu、内存使用情况
top -p <进程id>

tmux ls # 查看当前所有的 Tmux 会话
tmux attach -t 0 # 用于重新接入某个已存在的会话
ctrl+b d # 退出
tmux kill-session -t 0 # 杀死某个会话
```

---

## 基本命令

* 显示当前路径
```bash
pwd
```

* 移动文件：mv+源文件/源目录 目标文件/目标目录 
```bash
mv home/v-jyu36/DigiCertGlobalRootCA.crt.pem /var/www/iqvia_data/private
```

* 删除文件或目录
```bash
rm -rf src_path
```

* 修改权限
```bash
chmod 777 src_path
```

* 删除5天前的文件 
```bash
find ./excel -name "*" -mtime +5 -exec rm -rfv {} \;
```

* 查看文件所占空间
```bash
du -sh # 总和
du -d 1 # 当前目录下所有一级子目录所占空间大小
df -h /var # 指定目录挂载磁盘剩余空间
```

## 连接

1. 硬链接：ln/mount

 硬链接的文件是使用同一个inode结构,每一个硬链接使inode的使用计数加一,删除文件时,使用计数减一,当使用计数为零时,才真正删除文件。

 硬连接的作用是允许一个文件拥有多个有效路径名，这样用户就可以建立硬连接到重要文件，以防止“误删”的功能。

 mount：用于挂载Linux系统外的文件。操作的对象是设备
 
 Ln：操作对象是文件

 2. 软链接：ln -s

 软链接的文件内,不是存的数据,而是存的一个文件的全路径名,使用此链接时,会根据此路径找到目标文件，和windows里到快捷方式一样。


