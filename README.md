[中文](README.md) | [English](READMEen.md)

## 示例

https://www.jiangmiemie.com


## 目标

用纯Python构建一个**易于管理**、**低耦合**、**自由**的应用网站（包含应用演示与文档说明）其中Markdown是一等公民，用户只需放置md文件即可生成网页。

参考站点：
[docusaurus](https://docusaurus.io/zh-CN/docs/category/guides)
[pynecone](https://pynecone.io/)

## 使用

默认服务器已安装Python3.8或更高版本

### 准备
数据使用了默认为PGSQL，因此需要**新建一个数据库**。假设你的数据库信息如下：

database=reflexblog
user=reflexblog
password=yourpassword

那么，请在根目录新建一个`database.ini`文件，内容如下：

```
[postgresql]
host=localhost
database=reflexblog
user=reflexblog
password=yourpassword
```

如果你要使用一些应用，那么请同样的在根目录下新建一个文件`.env`，将相关的apikey可以放置其中。例如

```
OPENAIKEY = "sk-****************************"
```

### 下载依赖

`pip install -r requirements.txt`


### 域名

申请好前端域名和后端域名，并配置SSL。

修改[constants.py](blog/constants.py)
`MAIN_URL`为你的前端域名：前端展示于此。
`BACKEND_URL`为你的后端域名：后台服务运行于此，未正确配置会导致响应事件异常。

### 运行

切换到本文件夹所在目录，运行`bash run.sh`