### Problem description

- 假设有3台电脑A, B, C且它们都在同一个局域网内, 能够互相ping通. 现在电脑A可以直接访问外网如google, 但是B, C不能, 如果想让B, C也能访问外网有什么操作?

### Solution

- 当然最简单的就是A共享网络热点, B和C连接就可以了.
- 如果A不能共享网络热点呢? 我们可以在A机器上装一个代理的服务, 让B, C的流量都走A. 基本原理就是这样.

### Detailed steps

- 首先在A机器上装一个代理的服务. windows推荐CCproxy, linux推荐Tinyproxy.

- ```shell
  sudo apt-get update
  
  sudo apt-get install tinyproxy
  ```

- ```shell
  sudo vim /etc/tinyproxy.conf # 默认的配置文件
  
  Port 8888 # 预设是8888, 默认即可
  Allow 127.0.0.1 # 增加Allow 1.2.3.4,相当于这个ip允许访问我们的代理服务器
  Allow 1.2.3.4
  ```

- ```shell
  # 运行
  sudo service tinyproxy start
  
  # 重启
  sudo service tinyproxy restart
  
  # 停止
  sudo service tinyproxy stop
  ```

- ```shell
  # 连接测试
  # 其中IP和PORT是代理服务器的IP和代理端口，如果出现百度的源代码，则证明代理配置成功。
  curl -x <IP>:<PORT> www.baidu.com
  ```

---

- 代理服务器配置好了, 我们需要配置本地电脑的浏览器代理
- 这里以Chrome浏览器(Version 78.0.3904.108 (Official Build) (64-bit))为例, 其他的都一样.
- 我们需要给Chrome浏览器装个代理的插件: `Proxy SwitchyOmega`, [安装参考](https://github.com/Shadowsocks-Wiki/shadowsocks/blob/master/zh_CN/browser/chrome-setup-guide.md) 
- 最后添上代理服务器的ip, port, **Scheme**为(default), **Protocol**可能得试一试http or https.
- 如果一切正常, 这就ok了.
