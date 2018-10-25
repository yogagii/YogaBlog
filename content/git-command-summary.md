Title: Git命令整理
Date: 2018-10-14 15:31
Category: Programming
Tags: git
Author: 张本轩


1. 首先需要明确三个概念，Git中的文件有三种状态: 已提交(commited), 已修改(modified)和已暂存(staged), 这里前两个概念比较好理解，已提交表示数据已保存(执行git commit指令后)，已修改表示修改了文件但还没有保存数据，而已暂存表示已经对当前经过修改的文件做了标记（执行git add filename指令后)

2. 与之相对的Git项目有三个不同的工作区的概念: Git仓库、工作目录和暂存区域，之间的关系可以参考Git基础

3. 在首次使用Git前需要进行一些简单的配置:
    * 设置提交中使用的用户名: 
        * `git config --global user.name "yourname"`
    * 设置提交中使用的邮件地址: 
        * `git config --global user.email "youremail@emai.com"`
    * 你可以使用以下指令检查你的配置: 
        *` git config --list`

4. 常用指令
    * 初始化仓库: 
        * `git init`
    * 跟踪文件(或者添加文件到暂存区): 
        * `git add filename`  `git add . `                   //添加所有文件
    * 提交文件(将暂存区文件保存到本地): 
        * `git commit -m "your commit message"`
    * 克隆仓库: 
        * `git clone url`
        * `git clone --recursive url`下载所有submodule
    * 查看当前文件处于哪个状态: 
        * `git status`
    * 忽略文件: 
        * 修改.gitignore文件，可控制不希望被Git管理的文件
    * 查看文件中具体更新细节: 
        * `git diff`      // 比较工作目录当前文件与暂存区域之间的差异
        * `git diff --staged`   // 查看已暂存的将要添加到下次提交里的内容
    * 跳过暂存区域直接提交: 
        * `git commit -a -m "your commit message"`
    * 删除本地文件和暂存区文件: 
        * `git rm filename`
    * 删除暂存区文件但保留本地文件: 
        * `git rm --cached filename`
    * 查看提交历史: 
        * `git log`
    * 重新提交: 
        * `git commit --amend`
    * 取消暂存的文件(注意与`git rm --cached`的区别): 
        * `git reset HEAD filename`
    * 撤销对文件的修改: 
        * `git checkout -- filename`
    * 查看远程仓库: 
        * `git remote -v`
    * 添加远程仓库: 
        * `git remote add <shortname> <url>`
    * 从远程仓库抓取文件但是不合并: 
        * `git fetch [remote-name]`
    * 从远程仓库抓取文件并合并: 
        * `git pull`
    * 推送到远程仓库: 
        * `git push [remote-name] [branch-name]`
    * 查看远程仓库: 
        * `git remote show [remote-name]`
    * 远程仓库重命名: 
        * `git remote rename [original-name] [new-name]`
    * 移除远程仓库: 
        * `git remote rm [original-name]`

5. 分支指令
    * 创建分支: 
        * `git branch [branch-name]`
    * 切换分支: 
        * `git checkout [branch-name]`
    * 新建并切换分支: 
        * `git checkout -b [branch-name]`
        * `git checkout --orphan [branch-name]` 创建一个全新分支，分支历史从零开始
    * 合并到当前分支: 
        * `git merge [branch-name]`
    * 删除分支: 
        * `git branch -d [branch-name]`
    * 重命名分支:
        * `git branch -m [new-branch-name]`
    * 推送分支: 
        * `git push [remote] [branch]`
    * 避免输入密码: 
        * `git config --global credential.helper cache`
    * 跟踪远程分支: 
        * `git checkout -b [branch-name] [remote-name]/[branch-name]`
        * `git checkout --track [remote-name]/[branch-name]`
    * 修改上游分支: 
        * `git checkout -u [remote-name]/[branch-name]`
    * 查看所有跟踪分支: 
        * `git branch -vv`
    * 变基: 
        * `git rebase [branch-name]`