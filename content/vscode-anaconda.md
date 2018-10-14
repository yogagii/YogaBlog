Title: VS Code使用Anaconda Prompt作为默认terminal
Date: 2018-10-07 21:03
Category: Configuration
Tags: vscode 
Author: stupidfish

### Solution

在你自己的`User settings`中添加下列代码

    "terminal.integrated.shell.windows": "C:\\WINDOWS\\System32\\cmd.exe",
    "terminal.integrated.shellArgs.windows": [
        "/K", "C:\\Users\\ben\\Anaconda3\\Scripts\\activate.bat C:\\Users\\ben\\Anaconda3"       
    ]
其中`terminal.integrated.shellArgs.windows`后的参数可以通过右键点击`Anaconda Prompt`选择`属性`,复制目标一栏中后半部分路径获得

### Reference

[http://mscodingblog.blogspot.com/2017/08/setup-integrated-terminal-in-vs-code-to.html](http://mscodingblog.blogspot.com/2017/08/setup-integrated-terminal-in-vs-code-to.html)