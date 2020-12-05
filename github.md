小技巧：

提升github上clone 或 push 慢的原因：不是 [github.com](http://github.com/) 的域名被限制了，而是 [github.global.ssl.fastly.net](http://github.global.ssl.fastly.net/) 这个域名被限制了，最终导致git的速度最高只能达到 20KB/S，通过以下方法解决：

修改hosts文件

1.1 首先通过[DNS](http://tool.chinaz.com/dns)查询工具，查询域名的解析，输入"[github.global.ssl.fastly.net](http://github.global.ssl.fastly.net/)"，查到""TTL"值最小的，以北京【联调】IP为例：151.101.229.194；

1.2 在mac总端执行：sudo vim /etc/hosts，在后面追加"151.101.229.194 [github.global.ssl.fastly.net](http://github.global.ssl.fastly.net/)"，点击保存。