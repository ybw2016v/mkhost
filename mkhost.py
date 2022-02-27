import psycopg2
import conf
from core import findid,add_follower
import sys
import os

if len(sys.argv)!=3:
    print("使用方法: python mkhost.py [old hostname] [new hostname]")
    print("例如: python mkhost.py old.hostname.com new.hostname.com")
    os._exit(0)

hostold=sys.argv[1]
hostnew=sys.argv[2]



pgdog = psycopg2.connect(database=conf.database, user=conf.user, password=conf.password, host=conf.host, port=conf.port)
db=pgdog.cursor()

Follower_list=[]
Followee_list=[]
Follower_lost_list=[]
Followee_lost_list=[]
Follower_cf_list=[]
Followee_cf_list=[]

db.execute("""SELECT "followerId","id","followeeId","createdAt" FROM following WHERE "followerHost"=%s""",(hostold,))
flist=db.fetchall()
for fl in flist:
    lid=findid(fl[0],hostold,hostnew,db)
    if lid is None:
        Follower_lost_list.append(fl[0])
    else:
        felloweeid=fl[2]
        crt=fl[3]
        new_id=lid["nid"]
        db.execute("""SELECT "followerId","id","followeeId" FROM following WHERE "followerId"=%s and "followeeId"=%s""",(new_id,felloweeid))
        res=db.fetchone()
        lid["followeeId"]=felloweeid
        lid["followerId"]=new_id
        lid["createdAt"]=crt
        lid["type"]="R"
        lid["host"]=hostnew
        if res is None:
            Follower_list.append(lid)
        else:
            Follower_cf_list.append(lid)

print("**********************************************************")

db.execute("""SELECT "followerId","id","followeeId","createdAt" FROM following WHERE "followeeHost"=%s""",(hostold,))
flist=db.fetchall()
for fl in flist:
    lid=findid(fl[2],hostold,hostnew,db)
    if lid is None:
        Followee_lost_list.append(fl[2])
    else:
        fellowerid=fl[0]
        crt=fl[3]
        new_id=lid["nid"]
        db.execute("""SELECT "followerId","id","followeeId" FROM following WHERE "followeeId"=%s and "followerId"=%s""",(new_id,fellowerid))
        lid["followeeId"]=new_id
        lid["followerId"]=fellowerid
        lid["createdAt"]=crt
        lid["type"]="E"
        lid["host"]=hostnew
        
        res=db.fetchone()
        if res is None:
            Followee_list.append(lid)
        else:
            Followee_cf_list.append(lid)

print("**********************************************************")


print("共发现{}个关注关系{}个被关注关系可修复".format(len(Follower_list),len(Followee_list)))
print("共发现{}个关注关系{}个被关注关系已丢失".format(len(Follower_lost_list),len(Followee_lost_list)))
print("共发现{}个关注关系{}个被关注关系已存在".format(len(Follower_cf_list),len(Followee_cf_list)))
if len(Followee_list)>0:
    print("关注关系可修复列表:")
    for fitem in Followee_list:
        print("本地用户{}关注了{} |{}——>{}({})".format(fitem["followerId"],fitem["oid"],fitem["oid"],fitem["nid"],fitem["username"]))
if len(Follower_list)>0:
    print("被关注关系可修复列表:")
    for fitem in Follower_list:
        print("{}关注了本地用户{} |{}——>{}({})".format(fitem["oid"],fitem["followeeId"],fitem["oid"],fitem["nid"],fitem["username"]))
if len(Follower_lost_list)>0:
    print("关注关系丢失列表:")
    for fitem in Follower_lost_list:
        print("{}丢失".format(fitem))
if len(Followee_lost_list)>0:
    print("被关注关系丢失列表:")
    for fitem in Followee_lost_list:
        print("{}丢失".format(fitem))
if len(Followee_cf_list)>0:
    print("关注关系已存在列表:")
    for fitem in Followee_cf_list:
        print("本地用户{}关注了{} |{}——>{}({})".format(fitem["followerId"],fitem["oid"],fitem["oid"],fitem["nid"],fitem["username"]))
if len(Follower_cf_list)>0:
    print("被关注关系已存在列表:")
    for fitem in Follower_cf_list:
        print("{}关注了本地用户{} |{}——>{}({})".format(fitem["oid"],fitem["followeeId"],fitem["oid"],fitem["nid"],fitem["username"]))
# print(Follower_list)
Yn=input("是否开始修复?(Y/N)")
if Yn=="Y":
    for item in Followee_list:
        add_follower(item,db)
    for item in Follower_list:
        add_follower(item,db)
    pgdog.commit()
