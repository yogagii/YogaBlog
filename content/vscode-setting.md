Title: 解决VS Code在ubuntu下terminal无法显示下划线的问题
Date: 2018-10-07 20:47
Category: Configuration
Tags: vscode
Author: 张本轩

### Solution

输入`ctrl + shift + P` 打开命令面板搜索 `Open User Settings` - `Open settings.json`

添加`"editor.fontFamily": "'Ubuntu Mono', monospace"`即可

### VS Code显示数学公式

输入`ctrl + shift + X`搜索** Markdown+Math **安装即可。一共有4种形式的texmath语法，我们可以按照自己的需求选择,可以通过下列代码修改

```
"mdmath.delimiters": "dollars" // 这里输入你需要的语法
```

### Reference

[https://github.com/Microsoft/vscode/issues/38133](https://github.com/Microsoft/vscode/issues/38133)

