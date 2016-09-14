http://write.blog.csdn.net/mdeditor#!postId=52503110
# 需求
- 情景需求：记忆力不好，许多事情不提醒容易忘记，需要每天都能够提醒，而现有的记事软件太过繁琐，每天一个邮件提醒是最方便的
- 需求一：创建一个任务，在指定完成时间未完成的每天进行提醒，达到指定时间还未完成的任务需要顺延
- 需求二：要求自己每天做一个总结和计划，第二天需要收到前15天的总结（仅仅是方便加深印象，在总结中可以贴出云笔记链接，方便随时查看）
- 需求三：最好有web界面和APP方便操作，需要有一个公网ip，任何地方都能访问。
# 设计
## 概要设计
- 数据库设计
- 逻辑设计
## 详细设计
![这里写图片描述](http://img.blog.csdn.net/20160911113607656)
# 总结
- 后台功能都已经实现，目前还没有Web界面，等有时间再引入web框架
- 通过命令可以创建、查询、修改和删除任务或者总结，中间的操作就是编辑文本，详细操作可以看部署章节
# 部署
##  新建database:memory; 新建tables: table_task, table_summary; 因为使用一次，手动执行了。
```
MariaDB [memory]> show tables;
+------------------+
| Tables_in_memory |
+------------------+
| table_summary    |
| table_task       |
+------------------+
2 rows in set (0.00 sec)

MariaDB [memory]> desc table_task;
+-----------+------------------------------------+------+-----+---------------------+-----------------------------+
| Field     | Type                               | Null | Key | Default             | Extra                       |
+-----------+------------------------------------+------+-----+---------------------+-----------------------------+
| id        | int(11)                            | NO   | PRI | NULL                | auto_increment              |
| classify  | enum('home','work','note','other') | YES  |     | work                |                             |
| priority  | enum('A','B','C','D')              | YES  |     | A                   |                             |
| beginTime | timestamp                          | NO   |     | CURRENT_TIMESTAMP   | on update CURRENT_TIMESTAMP |
| endTime   | timestamp                          | NO   |     | 0000-00-00 00:00:00 |                             |
| progress  | tinyint(4)                         | YES  |     | 0                   |                             |
| subject   | tinytext                           | YES  |     | NULL                |                             |
| summary   | text                               | YES  |     | NULL                |                             |
| details   | text                               | YES  |     | NULL                |                             |
| questions | text                               | YES  |     | NULL                |                             |
+-----------+------------------------------------+------+-----+---------------------+-----------------------------+
10 rows in set (0.01 sec)

MariaDB [memory]> desc table_summary;
+----------+-----------+------+-----+-------------------+-----------------------------+
| Field    | Type      | Null | Key | Default           | Extra                       |
+----------+-----------+------+-----+-------------------+-----------------------------+
| id       | int(11)   | NO   | PRI | NULL              | auto_increment              |
| datetime | timestamp | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
| subject  | tinytext  | YES  |     | NULL              |                             |
| summary  | text      | YES  |     | NULL              |                             |
| plan     | text      | YES  |     | NULL              |                             |
+----------+-----------+------+-----+-------------------+-----------------------------+
5 rows in set (0.00 sec)
```
## 暂时没有设计配置文件，需要手动修改程序
### 修改数据库密码
```
cat memory_general.py
def mariadb_cmd_ret(cmd):
    mariadb_connection = mariadb.connect(user='memory', password='????????',
                                         database='memory')
# ...
def mariadb_cmd(cmd):
    mariadb_connection = mariadb.connect(user='memory', password='????????',
                                         database='memory')
```
### 修改邮件配置
```
def send_email(mail_subject, mail_text):
    # 邮件需要显示发送方的地址
    sender = ("%s<??????@aws.com>") % (Header('sender header','utf-8'),)
    # 要发送的邮箱地址
    receivers = ['??????@icloud.com']
# ...
```
## 程序分析，以及添加数据
```
# 程序执行帮助
[root@ip-172-31-26-104 memory]# python memory -h
Usage:
       python memory list task/summary
       python memory show task/summary ID
       python memory update task/summary
       python memory new task/summary
       python memory insert task/summary
       python memory delete task/summary ID
       python memory send task/summary
       
# 打印任务task表中的数据，如果是表里没有数据，则没有输出。新建任务操作在下面
[root@ip-172-31-26-104 memory]# python memory list task
memory_list
13 每日功课提示

# 打印总结summary表中的数据
[root@ip-172-31-26-104 memory]# python memory list summary
memory_list
23 memory项目完成

# 打印总结表summary表中23号的详细信息
[root@ip-172-31-26-104 memory]# python memory show summary 23
memory_show
##########################
&& 23
&& 2016-09-08 11:22:09
&& memory项目完成
&& 1. 可以把总结写在有道，分享出连接，放到csdn
2. 把代码模型放到github（注意需要把个人信息数据库密码，邮箱信息隐藏）
3. 写一份使用说明
&& 加入python-web最好，这样就可以在浏览器上完成所有操作了，目前相当后台逻辑已经完成了。

# 同时详细信息也写在memory_tmp文件，方便更改操作
[root@ip-172-31-26-104 memory]# cat memory_tmp 
[table_summary]
id = 23
datetime = 2016-09-08 11:22:09
subject = memory项目完成
summary = 1. 可以把总结写在有道，分享出连接，放到csdn
	2. 把代码模型放到github（注意需要把个人信息数据库密码，邮箱信息隐藏）
	3. 写一份使用说明
plan = 加入python-web最好，这样就可以在浏览器上完成所有操作了，目前相当后台逻辑已经完成了。

# 你可以vim更新23号的信息并保存，这时候只需要执行下面更新命令即可
[root@ip-172-31-26-104 memory]# python memory update summary

# 当然，如果没有数据需要创建
[root@ip-172-31-26-104 memory]# python memory new summary
memory_new

# vim memory_tmp并保存即可
[root@ip-172-31-26-104 memory]# cat memory_tmp 
[table_summary]
id = 
datetime = 
subject = 
summary = 
plan = 

# 执行命令插入到数据库
[root@ip-172-31-26-104 memory]# python memory insert summary

# 发送邮件
[root@ip-172-31-26-104 memory]# python memory send summary

# 任务task的操作和总结summary的操作是类似的
```

## 创建memorySend命令
```
[root@ip-172-31-26-104 ~]# cat /usr/bin/memorySend 
#!/bin/sh

cd /root/memory
python memory send task
sleep 1s
python memory send summary
```

## 创建定时任务，每天发送邮件
```
[root@zengyifan memory]# crontab -e
[root@zengyifan memory]# crontab -l
20 21 * * * memorySend
```
