Title: 解决VS Code在ubuntu下terminal无法显示下划线的问题
Date: 2018-10-07 20:47
Category: Configuration
Tags: vscode
Author: stupidfish

### Solution

输入`ctrl + shift + P` 打开命令面板搜索 `Open User Settings` - `Open settings.json`

添加`"editor.fontFamily": "'Ubuntu Mono', monospace"`即可

### Reference

[https://github.com/Microsoft/vscode/issues/38133](https://github.com/Microsoft/vscode/issues/38133)

