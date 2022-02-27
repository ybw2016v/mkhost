import base36
import time

SDOG=946684800000

def gen_dog_id():
    """
    生成10位时间戳(伪)
    """
    tdog=int(1000*time.time())-SDOG
    strdog=base36.dumps(tdog)
    return strdog+'01'

def findid(id,oldhost,newhost,db):
    """
    查找用户对应id
    """
    db.execute("""SELECT username,host FROM public.user WHERE "id"=%s""",(id,))
    userinfo=db.fetchone()
    if userinfo[1]!=oldhost:
        return None
    username=userinfo[0]
    db.execute("""SELECT id,"inbox","sharedInbox","username" FROM public.user WHERE "host"=%s AND "username"=%s""",(newhost,username))
    userinfo2=db.fetchone()
    
    if userinfo2 is None:
        return None
    usernid=userinfo2[0]
    reinfo={"oid":id,"nid":usernid,"Inbox":userinfo2[1],"sharedInbox":userinfo2[2],"username":"{}@{}".format(userinfo2[3],newhost)}
    return reinfo

def add_follower(uix,db):
    """
    添加关注关系
    """
    fid=gen_dog_id()
    if uix["type"]=="E":
        db.execute("""INSERT INTO public.following (id,"createdAt","followerId","followeeId","followeeHost","followeeInbox","followeeSharedInbox") VALUES (%s,%s,%s,%s,%s,%s,%s)""",(fid,uix["createdAt"],uix["followerId"],uix["followeeId"],uix["host"],uix["Inbox"],uix["sharedInbox"]))
        # db.commit()
    if uix["type"]=="R":
        db.execute("""INSERT INTO public.following (id,"createdAt","followerId","followeeId","followerHost","followerInbox","followerSharedInbox") VALUES (%s,%s,%s,%s,%s,%s,%s)""",(fid,uix["createdAt"],uix["followerId"],uix["followeeId"],uix["host"],uix["Inbox"],uix["sharedInbox"]))
        # db.commit()
    

