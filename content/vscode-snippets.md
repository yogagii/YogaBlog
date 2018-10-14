Title: 利用VS Code Snippets生成C++头文件保护符
Date: 2018-10-07 20:54
Category: Programming
Tags: vscode, c++ 
Author: stupidfish

### Solution

将下列代码贴入你的`snippets`中，然后在`cpp`文件中输入`pre`+`tab`即可自动生成相关头文件

    {
        "Preprocessor of cpp file":{
            "prefix": "pre",
            "body": [
                "#ifndef ${TM_FILENAME/(.*)(\\.)+(.*)/${1:/upcase}_${3:/upcase}/}",
                "#define ${TM_FILENAME/(.*)(\\.)+(.*)/${1:/upcase}_${3:/upcase}/}",
                "class ${TM_FILENAME/([a-z])(.*)(\\.)+(.*)/${1:/upcase}${2}/} {",
                    "$1",
                "};",
                "#endif"
            "description": "Preprocessor of cpp and hpp file"
        }
    }

每一个`snippet`由`prefix`, `body`和`description`组成,其中`prefix`表示你的快捷键符，`body`是你的`snippet`内容。
`$TM_FILENAME`是系统定义的变量，表示当前文件的完整文件名，然后利用正则表达式生成对应的头文件保护符。

### Reference

[https://code.visualstudio.com/docs/editor/userdefinedsnippets#_global-snippets](https://code.visualstudio.com/docs/editor/userdefinedsnippets#_global-snippets)

