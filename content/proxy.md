Title: Proxy
Date: 2022-11-03
Category: Programming
Author: Yoga

## VPN

cd 文件目录

./v2ray

SwitchyOmega

proxy:
 - 代理协议：SOCKS5
 - 代理服务器：127.0.0.1
 - 代理端口：10808

auto switch:
  - 规则列表网址：https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt

---

### Whistle 抓包工具

```bash
npm install -g whistle
w2 start
w2 stop
```

配置规则：http://localhost:8899/#rules

```
dashboard.xxx.cn/carto-data/report localhost:3009/report
```

SwitchyOmega

新建情景模式 whistle:
 - 代理协议：HTTP
 - 代理服务器：127.0.0.1
 - 代理端口：8899