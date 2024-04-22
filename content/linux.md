Title: Linux 服务器配置
Date: 2022-04-21
Category: Programming
Author: Yoga

## 安装node

1. 到 node 官网

http://nodejs.cn/download/

https://registry.npmmirror.com/binary.html?path=node/ 

去下载一个 linux 可用的 node 版本

2. 传输到服务器 /home/jyu 并解压

scp ~/Desktop/node-v18.16.0-linux-x64.tar.xz jyu@xx.xx.xx.xx:~

```bash
xz -d node-v14.18.2-linux-x64.tar.xz
tar -xvf node-v14.18.2-linux-x64.tar
```

3. 软连接 (步骤3,4二选一)

```bash
ln -s /home/jyu/node-v14.18.2-linux-x64/bin/npm /usr/local/bin
ln -s /home/jyu/node-v14.18.2-linux-x64/bin/node /usr/local/bin
```

4. 配置环境变量

env 查看环境变量 PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin

```bash
vi /etc/profile

export NODEJS_HOME=/home/jyu/node-v14.18.2-linux-x64
export PATH=$PATH:$NODEJS_HOME/bin

source /etc/profile
```

## 更新node

node -v

```bash
sudo su -
npm cache clean -f
npm install -g n
n stable
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
tmux split-window # 划分上下两个窗格 ctrl+b "
tmux split-window -h # 划分左右两个窗格 ctrl+b %
tmux select-pane -U # 光标切换窗格 
ctrl+b 方向键下 # 光标切换窗格 
ctrl+b x # 关闭当前窗格 

ipython
%run YogaModel-ChopModel.py 

free # 查看内存
top # 观察cpu、内存使用情况
top -p <进程id>
htop # ubuntu: apt install htop

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

* 显示问价大小
```bash
ls -lh
```

* 显示文件数量
```bash
ls ./excel -l|grep "^-"| wc -l 
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

 ## netstat 网络相关信息

* 查看所有占用端口号
```
netstat -tunlp
```

* 查看占用端口号27999的进程
```
netstat -pan | grep 27999
// tcp6  0  0  :::27999  :::*  LISTEN  15460/node
```

## ps 进程信息 Process Status

* 查看指定进程详情
```
ps -aux | grep 15460
// root 15460  0.0  0.2 867324 42508 pts/5 Sl+ 10:14 0:00 node index
```
* 杀死指定进程
```
kill 15460
```

* 检查高 CPU / 内存消耗进程
```
ps -eo pid,ppid,user,cmd,%mem,%cpu --sort=-%cpu|head -n 10
```

## 文本操作

* 定位首行

```
gg
```

* 定位尾行

```
G
```

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

## 连接

1. 硬链接：ln/mount

 硬链接的文件是使用同一个inode结构,每一个硬链接使inode的使用计数加一,删除文件时,使用计数减一,当使用计数为零时,才真正删除文件。

 硬连接的作用是允许一个文件拥有多个有效路径名，这样用户就可以建立硬连接到重要文件，以防止“误删”的功能。

 mount：用于挂载Linux系统外的文件。操作的对象是设备
 
 Ln：操作对象是文件

 2. 软链接：ln -s

 软链接的文件内,不是存的数据,而是存的一个文件的全路径名,使用此链接时,会根据此路径找到目标文件，和windows里到快捷方式一样。

--

## 开机启动

* 列出所有启动项命令，开启的和未开启的。开启的会绿色显示为enabled。
```bash
systemctl list-unit-files
systemctl list-unit-files | grep enabled
```
* 查看某个.service服务的状态信息 
```bash
systemctl status mysqld.service
systemctl nginx status
service nginx status
```

* 查看某个服务是否设置开机启动
```bash
systemctl is-enabled mysqld.service
systemctl is-enabled docker.service
systemctl is-enabled nginx.service 
```

* 启用和禁用服务开机启动
```bash
systemctl enable mysqld.service
systemctl enable docker.service
systemctl enable nginx.service 
systemctl disable mysqld.service
chkconfig nginx on
```

* 启动、停止、重启一个服务
```bash
systemctl start mysqld.service
systemctl stop mysqld.service
systemctl restart mysqld.service
service nginx start
```

_踩坑：Unit nginx.service not found._

vim /lib/systemd/system/nginx.service
```bash
[Unit]
Description=The nginx HTTP and reverse proxy server
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/run/nginx.pid
# Nginx will fail to start if /run/nginx.pid already exists but has the wrong
# SELinux context. This might happen when running `nginx -t` from the cmdline.
# https://bugzilla.redhat.com/show_bug.cgi?id=1268621
ExecStartPre=/usr/bin/rm -f /run/nginx.pid
ExecStartPre=/usr/sbin/nginx -t # 换成nginx安装路径
ExecStart=/usr/sbin/nginx # 换成nginx安装路径
ExecReload=/bin/kill -s HUP $MAINPID
KillSignal=SIGQUIT
TimeoutStopSec=5
KillMode=mixed
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```
