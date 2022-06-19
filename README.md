# Django - DRF

#### 介绍
详细的实例了DRF中所涉及到的所有基本操作，能让初学者对DRF建立一个基本的认识！

#### 软件架构
基本的Django项目结构
* DRF : 主目录
    * setting.py : 本项目所有的setting在此设置
    * url.py : 本项目所有的url在此定义
* sers : 业务目录
    * models.py : 模型层，涉及到本次用到的所有的表
    * view： 该目录下的每一个文件放了一种方法的业务代码
    * views.py : 将view目录下的所有的方法进行了集合

* manage.py : 启动文件
#### 安装教程

1. 在setting中修改数据库的配置（本项目设置的数据库名为DRF，请确保库在您本地已经建立）
2. 下载依赖：因为不是新建的项目虚拟环境，所以库比较多，就不在这里生成依赖文件，主要的版本如下：
       Django==4.0.5
       django-import-export==2.8.0
       djangorestframework==3.13.1
       python==3.9
3. 使用命令生成数据库迁移文件：python manage.py makemigrations
4. 使用命令进行数据库迁移：python manage.py migrate
5. 运行，就可以启动，端口5000

#### 使用说明

1. 本项目将DRF中所涉及到的所有的知识点进行了汇总，具体请看view目录下文件中的注释，注释中详细的写了用到的类，方法的作用
2. 所用的数据库表的数据需要用户自行添加
3. 未经允许，请勿转发，请勿用作商业用途
4. 著作权归作者所有，联系邮件：chenchenchenmyl@163.com


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)