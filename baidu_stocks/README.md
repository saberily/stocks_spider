## 项目简介

* 本项目使用python scrapy,框架来实现,分为三个主要环节.

* 首先获取东方财富网的股票列表
  
    http://quote.eastmoney.com/stocklist.html
    
* 将得到的股票序号构造url,到百度股票网爬取详细股票信息。

    https://gupiao.baidu.com/
     
* 最后将得到的数据入库或者存储为其他格式的文件例如json csv 等。

## 平台兼容

* Windows
* Mac OS X
* Linux 基本上都可以只要有python环境

## 环境配置

#### Python3.6及以上
* 本人是在windows上创建运行的 以下所有说明都是针对windows的. 其他平台较为简单
  首先简单介绍一下python安装:
  选择下载anaconda自带python不用管环境的配置 较为轻松, 可以到官网下载也可以到清华镜像站
  后者速度快些,很多python库都可以到清华镜像站下载.

* 下载

   https://www.anaconda.com/download/


* 测试

   启用cmd命令行 输入python回车
   若提示版本信息，则安装成功。

## 准备工作

#### pythonIDE 下载

* 当然你也可以直接用命令行操作，pythonIDE很多，本人选取是pycharm。

####数据库下载及配置

* 本人选择的是mongodb也可以使用其他数据库如Redis、MySQL。
  下载比较容易，本人就不赘述了。还可以下载一个mongodb的可视化工具robomongo。
  
    https://robomongo.org/
    
* 我们找到mongodb存储路径，在与bin相同路径下新建一个data文件夹。然后在data文件下新建两个文件夹db和logs
  分别用来存储数据库和日志，然后回到bin目录下，在当前路径下打开cmd。
        
   ```
      mongod --dbpath 加刚才新建的db的路径
   ```
  
* 然后用管理员权限打开cmd在Windows下配置相关参数， 首先进入到bin目录下， 然后输入命令。
  
      
   ```
         mongod --bind_ip 0.0.0.0 --logpath log路径 --logappend --dbpath db路径 --port 27017
         --serviceName 'mongodb' --serviceDisplayName 'mongodb' --install
   ```
  
#### 相关python库的安装

* 打开cmd命令行， 输入pip， help然后回车就会出现pip命令相关介绍
  我们选择pip install 方法来安装python相关库。  
 
* 其中在scrapy安装较为繁琐， 因为需要许多依赖库。 可以使用anaconda自带的一个工具Navigator进行安装。
  也可以到镜像站去下载， 因为是国外的网站， 直接使用pip install scrapy可能出现timeout。

* 主要库的安装 pip 安装如下
  ```
  pip install requests
  pip install wheel
  pip install lxml
  pip install PyOepnssl
  pip install Twisted
  pip install Pywin32
  pip install scrapy
  ```

####相关库的说明

* requests是爬虫最常用的库之一， 常用的Method有get post。
  lxml是常用的html解析库， 其他都是scrapy的依赖库， 详细使用方法请参考官方文档。

* scrapy的官方文档网址
  
    https://docs.scrapy.org/en/latest/
   
******____******
## 本项目使用方法

####运行

* 可以直接使用cmd命令行， 不过要找到项目的相应路径。
  这里可以直接用pycharm打开， pycharm自带一个terminal终端，
  然后先后输入如下命令， 就可以看到程序运行了。
  如果无法运行， 可能前端页面更改了。 修改一下stock_Info.py中解析页面函数股票相关数据的
  xpath路径， 直接打开网页的源码复制xpath即可。
  或者查看一下settings.py下的ROBOTSTXT_OBEY是否为True， 若是True改成False。
  
  ```
  cd baidu_stocks
  scrapy crawl stock_Info
  ```

* 可以Ctrl+C终止程序运行， 检查一下输出的数据是否正确


####项目相关其他介绍

* scrapy框架较为灵活， 算是一个半成品， 用户主要编写解析相关页面及数据处理的函数和类，
  其他东西我们基本上不用考虑直接交给scrapy框架来执行。

* settings.py 中，有相应配置项。
  ROBOTSTXT_OBEY = True 是指遵循robots协议， 我们一般改为False以免爬不到数据。
  DEFAULT_REQUEST_HEADERS是指默认的请求数据头，
  当我们更改或重写了pipelines.py的类时， 我们要相应的修改settings.py
  下的ITEM_PIPELINES参数， 其他的默认参数我们一般不做修改。

##项目数据输出和入库

*  我们可以在pipelines定义item处理方法将得到数据保存为json csv等，
   这里本人介绍一种简便方法， 直接使用命令行来完成操作。
   
  ```
  scrapy crawl stock_Info -o stocks_Info.json
  ```
 
* 第二种数据处理就是入库， 官方文档提供了一种入库模板，
  十分灵活， 我们直接将mongourl和mongodb配置到settings.py下更加结构化。
  
  ``
  
      import pymongo
    
      class MongoPipeline(object):
    
            def __init__(self, mongo_uri, mongo_db):
                self.mongo_uri = mongo_uri
                self.mongo_db = mongo_db
        
            @classmethod
            def from_crawler(cls, crawler):
                return cls(
                    mongo_uri=crawler.settings.get('MONGO_URI'),
                    mongo_db=crawler.settings.get('MONGO_DATABASE')
                )
        
            def open_spider(self, spider):
                self.client = pymongo.MongoClient(self.mongo_uri)
                self.db = self.client[self.mongo_db]
        
            def close_spider(self, spider):
                self.client.close()
        
            def process_item(self, item, spider):
                self.db[self.collection_name].insert_one(dict(item))
                return item
    
      
  
  
  ```