# mkhost

一个修复misskey关注关系脚本，在日常使用中，有些实例会更换域名，导致关注关系出现异常。在现行版本的misskey中，更换域名后的用户会被当成一个全新用户，原有的关注与被关注关系会全部丢失。外站用户的活动并不能正确显示在本地用户的timelines中，本地用户的活动也不会发送到新的域名上。这个脚本可以在一定程度上重建关注关系，解决相应的问题。

脚本首先列出域名更换牵涉到的关注关系，与所涉及的外站用户的相关信息，并通过对比用户名的方式找到并确认在新域名下该用户的相关信息，最后在`following`表中添加相关信息。


## 使用方法

0. 安装好psycopg2-binary和base36

```bash
pip3 install psycopg2-binary
pip3 install base36
```

1. 在`conf.py`中配置好postgress数据库的连接信息

2. 运行

```bash
python3 mkhost.py old_host new_host
```

