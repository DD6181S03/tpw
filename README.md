# 济南公交实时位置查询

## For non-Chinese speakers
I think there are no English speaker will use this project, so I didn't write the documentation in English.  
If you need help, please contact me.

## 写在前面
本项目断断续续开发很久，由于初期技术生疏，中间有不少丑陋的代码实现，编码规范也基本上没遵守过，但还好也实现了一些基本的功能。  
为了学习新的技术，我打算将此项目使用Vue.js重写，同时可以获得更好的前端效果。即使将来此项目(Python版)由于各种原因不再可用，也可能不会及时更新。  
因为在博客上有所提及，也为了练习Docker的使用，我将这个版本略作修改后发布在Github并提供用Docker部署的方法。  

## 介绍
本项目基于Flask，可以实现济南公交的线路和站点搜索，线路和车辆实时情况查询。  

## 部署
推荐使用Docker部署，不过手动部署也不是不行，就这么几个文件，怎么着也能跑起来。

### 你需要有
- 高德地图的api key  
- Docker运行环境  
- （可选）一个web服务器，如Nginx  

### 获取Docker镜像并运行
```
docker pull dd6181s03/tpw

docker run -d -e MODE=simple -e CSRFTOKEN=dd -e AMAPKEY=aaa -p 5000:5000 --name tpw1 tpw
或
docker run -d -e MODE=proxy -e CSRFTOKEN=dd -e AMAPKEY=aaa -p 5374:5374 --name tpw1 tpw
```
环境变量解释：  
- MODE有两种，simple和uwsgi。
- simple模式会使用Flask自带的web服务器并运行在容器内5000端口，无需配合额外服务器，适合测试或轻量级使用。  
- uwsgi模式会在容器内5374端口提供一个uwsgi socket，需配合web服务器使用。如使用此方式，请看下节"配置web服务器" 。  
- CSRFTOKEN为防止CSRF攻击所必要的，请设置为随机字符串。  
- AMAPKEY为你的高德地图api key，请自行前往高德地图开发者平台获取。  
无论何种模式，皆可自行修改":"前面的端口，以将容器内特定端口映射到宿主机内的自定义端口。  
name后的首个参数为该容器的名称，可自行修改。  

### 配置web服务器(以Nginx为例)
```
server {
  listen 443;
  server_name f2.jn84.net;
  ssl on;
  ssl_certificate /path/to/your/cert/fullchain.pem;
  ssl_certificate_key /path/to/your/cert/privkey.pem;
  location / {
    uwsgi_pass 127.0.0.1:5347;
    include uwsgi_params;
  }
}
```
配置仅供参考，请根据实际情况修改。  

到这里为止，不出意外的话，部署就成功了。  

## 致谢
在WGS-84和GCJ-02的坐标转换中使用了之前从Github复制的代码，由于时间久远，而且只是部分复制，已经无法找到原repo了，在此致谢。  
