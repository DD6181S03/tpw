# 济南公交实时位置查询

## For non-Chinese speakers
I don't think anyone who speaks English will use this project, so I didn't write English documentation.
Please contact me if you need help.

## 写在前面
本项目断断续续开发很久，由于初期技术生疏，中间有不少丑陋的代码实现，编码规范也基本上没遵守过，但还好也实现了一些基本的功能。  
为了学习新的技术，我打算将此项目使用Vue.js重写，同时可以获得更好的前端效果。即使将来此项目(Python版)由于各种原因不再可用，也可能不会及时更新。  
因为在博客上有所提及，也为了练习Docker的使用，我将这个版本略作修改后发布在Github并提供用Docker部署的方法。  

## 介绍
本项目基于Flask，可以实现济南公交的线路和站点搜索，线路和车辆实时情况查询。  

## 测试站点
[https://f2.jn84.net:2053](https://f2.jn84.net:2053)

## 部署
推荐使用Docker部署，不过手动部署也行，就这么几个文件，怎么着也能跑起来。

## 你需要有
- 高德地图的api key  
- （可选）Docker运行环境  
- （可选）一个web服务器，如Nginx  

### Docker部署
```
docker pull dd6181s03/tpw
docker run -d -e CSRFTOKEN=aaa -e AMAPKEY=bbb -p 5000:5000 --name tpw1 dd6181s03/tpw
```
环境变量解释：  
- CSRFTOKEN为防止CSRF攻击所必要的，请设置为随机字符串。  
- AMAPKEY为你的高德地图api key，请自行前往高德地图开发者平台获取。  

此时会使用Flask自带的web服务器并运行在容器内5000端口，无需配合额外服务器，适合测试或轻量级使用。  
可自行修改":"前面的端口，以将容器内特定端口映射到宿主机内的自定义端口。  
name后的首个参数为该容器的名称，可自行修改。  

### 使用uwsgi的手动部署
#### 准备运行环境
```
git clone https://github.com/DD6181S03/tpw.git
cd tpw
pip install -r requirements.txt
pip install uwsgi
```
建议配合virtualenv等虚拟环境使用。  

#### 修改环境变量
将以下内容修改后加入你的.bashrc/.zshrc等shell初始化文件中：  
```
export CSRFTOKEN=aaa
export AMAPKEY=bbb
```  
关于两个环境变量的解释见上文。

#### 运行uwsgi服务器
`uwsgi uwsgiconf.ini`  

#### 配置web服务器(以Nginx为例)
```
server {
  listen 443;
  server_name f2.jn84.net;
  ssl on;
  ssl_certificate /path/to/your/cert/fullchain.pem;
  ssl_certificate_key /path/to/your/cert/privkey.pem;
  location / {
    uwsgi_pass 127.0.0.1:5374;
    include uwsgi_params;
  }
}
```
配置仅供参考，请根据实际情况修改。  

## 致谢
在WGS-84和GCJ-02的坐标转换中使用了之前从Github复制的代码，由于时间久远，而且只是部分复制，已经无法找到原repo了，在此致谢。  
