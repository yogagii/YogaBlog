Title: Git命令整理
Date: 2018-10-14 15:31
Category: Programming
Tags: git
Author: 张本轩 & Yoga


1. 首先需要明确三个概念，Git中的文件有三种状态: 已提交(commited), 已修改(modified)和已暂存(staged), 这里前两个概念比较好理解，已提交表示数据已保存(执行git commit指令后)，已修改表示修改了文件但还没有保存数据，而已暂存表示已经对当前经过修改的文件做了标记（执行git add filename指令后)

2. 与之相对的Git项目有三个不同的工作区的概念: Git仓库、工作目录和暂存区域，之间的关系可以参考Git基础

## 在首次使用Git前需要进行一些简单的配置:

* 设置提交中使用的用户名: 
```
git config --global user.name "yourname"
```
* 设置提交中使用的邮件地址: 
```
git config --global user.email "youremail@emai.com"
```
```
git config remote.origin.url "https://jyu36@sourcecode.jnj.com/scm/asx-xxxx/fpa_frontend.git"
```
* 你可以使用以下指令检查你的配置: 
```
git config --list
```

## 常用指令
* 初始化仓库: 
```
git init
```
* 跟踪文件(或者添加文件到暂存区): 
```
git add filename
git add .  //添加所有文件
```
* 提交文件(将暂存区文件保存到本地): 
```
git commit -m "your commit message"
```
* 克隆仓库: 
```
git clone url
git clone --recursive url //下载所有submodule
```
* 查看当前文件处于哪个状态: 
```
git status
```
* 忽略文件: 

修改.gitignore文件，可控制不希望被Git管理的文件
```
// 根目录下
vim .gitignore_global
// *~
// .DS_Store
vim .gitconfig
// [user]
// 	name = xx
//	email = xx@xx.com
// [core]
// 	excludesfile = /Users/jyu36/.gitignore_global
git config --list
```
* 查看文件中具体更新细节: 
```
git diff  // 比较工作目录当前文件与暂存区域之间的差异
git diff --staged  // 查看已暂存的将要添加到下次提交里的内容
```
* 跳过暂存区域直接提交: 
```
git commit -a -m "your commit message"
```
* 删除本地文件和暂存区文件: 
```
git rm filename
```
* 删除暂存区文件但保留本地文件: 
```
git rm --cached filename
```
* 查看提交历史: 
```
git log
```
* 重新提交: 
```
git commit --amend
```
* 取消暂存的文件(注意与`git rm --cached`的区别): 
```
git reset HEAD filename
```
* 撤销对文件的修改: 
```
git checkout -- filename
```
* 将所有untracked file删除: 
```
git  clean  -f
```
* 查看远程仓库: 
```
git remote -v
```
* 添加远程仓库: 
```
git remote add <shortname> <url>
```
* 从远程仓库抓取文件但是不合并: 
```
git fetch [remote-name]
```
* 从远程仓库抓取文件并合并: 
```
git pull
```
* 推送到远程仓库: 
```
git push [remote-name] [branch-name]
```
* 查看远程仓库: 
```
git remote show [remote-name]
```
* 远程仓库重命名: 
```
git remote rename [original-name] [new-name]
```
* 移除远程仓库: 
```
git remote rm [original-name]
```

## 分支指令
* 创建分支: 
```
git branch [branch-name]
```
* 切换分支: 
```
git checkout [branch-name]
```
* 新建并切换分支: 
```
git checkout -b [branch-name]
git checkout --orphan [branch-name] //创建一个全新分支，分支历史从零开始
```
* 合并到当前分支: 
```
git merge [branch-name]
```
* 删除分支: 
```
git branch -d [branch-name]
```
* 重命名分支:
```
git branch -m [new-branch-name]
```
* 推送分支: 
```
git push [remote] [branch]
```
* 避免输入密码: 
```
git config --global credential.helper cache
```
* 跟踪远程分支: 
```
git checkout -b [branch-name] [remote-name]/[branch-name]
git checkout --track [remote-name]/[branch-name]
```
* 将本地分支与远程分支关联: 
```
git branch --set-upstream-to=origin/dev
```
* 修改上游分支: 
```
git checkout -u [remote-name]/[branch-name]
```
* 查看所有跟踪分支: 
```
git branch -vv
```
* 变基: 
```
git rebase [branch-name]
```

## 部署

* 打tag:
```
git tag 2019-R6
git push --tag
```
* 拷贝本地文件去服务器:
```
scp ~/Desktop/m/index.html root@47.100.43.192:~/deployf
fpa_share_doc jyu36$ scp ~/Desktop/userAvatar.png root@47.100.43.192:~/www/chatbot_hackathon/img
```
* 配置文件:

cd /etc/nginx/sites-available

vim 网址

```
// build
server {
    server_name hr_hackathon.jnjadc.com;
    root /usr/share/nginx/fpa_share_doc/dist;
    location / {
      try_files $uri $uri/ /index.html;
    }
  }
// 单页
server {
  server_name project_organization.jnjadc.com;
  root /root/www/project_organization;
  index dateBar.html;
}
```

* 软连接:
```
ln -s /etc/nginx/sites-available/hr_hackathon.jnjadc.com /etc/nginx/sites-enabled
```
* Nginx:
```
// 测试
nginx -t
// 重启
service nginx restart
```
* 改变文件权限:
```
chmod 777 ./build.sh
```
* 执行脚本:
```
./build.sh
```

## netstat

* 查看占用端口号27999的进程
```
netstat -pan | grep 27999
// tcp6  0  0  :::27999  :::*  LISTEN  15460/node
```
* 查看指定进程详情
```
ps -aux | grep 15460
// root 15460  0.0  0.2 867324 42508 pts/5 Sl+ 10:14 0:00 node index
```
* 杀死指定进程
```
kill 15460
```

## PM2进程管理工具

* 启动index.js（node index）并起名:
```
pm2 start index.js --name wxAuthorize
```
* 列表 PM2 启动的所有的应用程序:
```
pm2 list
```
* 删除指定应用 id 0:
```
pm2 delete 0
```
* 停止指定应用:
```
pm2 stop 0
pm2 stop wxAuthorize
```
* 重启指定应用:
```
pm2 restart wechat_auth
```
* 显示log:
```
pm2 log wxAuthorize
```
* 重新加载指定应用:
```
pm2 reload wechat_auth
```

## less

* 显示CSV的行数:
```
cat data.csv | wc -l // wordcount -line
```

* 高级的cat:

大写G文件尾，小写g到文件头，小写q退出, /搜索关键字
```
less data.csv
```

* 显示行号
```
less -N data.csv 
```

## Linux

```
sudo su -
su f1nance
cd ~/fpa_backend/
pm2 reload app
```


