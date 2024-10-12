import redis
def spray():
    for i in range(0,500):
        user_connection.set("fillerA"+str(i),"A"*256)
        user_connection.set("fillerB"+str(i),"B"*256)
        user_connection.set("fillerC"+str(i),"C"*256)

def create_group( skey, gname ):
    try:
        user_connection.xgroup_create( name=skey, groupname=gname, id="$", mkstream=True )
    except redis.ResponseError as e:
        print(f"raised: {e}")


user_connection = redis.Redis(host='localhost', port=6379,  password='', decode_responses=True)
x = user_connection.ping()
if x == True:
    create_group("s:foo","g:foo")
    user_connection.xadd("s:foo",{"foo":1},maxlen=1,approximate=True)
    user_connection.xadd("s:foo",{"foo":2},maxlen=1,approximate=True)
    user_connection.xadd("s:foo",{"foo":3},maxlen=1,approximate=True)
    user_connection.xadd("s:foo",{"foo":4},maxlen=1,approximate=True)
    user_connection.xadd("s:foo",{"foo":5},maxlen=1,approximate=True)
    print(user_connection.xreadgroup("g:foo","c:1",count=1,streams={"s:foo":">"}))
    print(user_connection.xreadgroup("g:foo","c:1",count=1,streams={"s:foo":">"}))
    print(user_connection.xreadgroup("g:foo","c:1",count=1,streams={"s:foo":">"}))
    print(user_connection.xreadgroup("g:foo","c:1",count=1,streams={"s:foo":">"}))
    print(user_connection.xreadgroup("g:foo","c:1",count=1,streams={"s:foo":">"}))
    user_connection.xtrim("s:foo",maxlen=1)
    print(user_connection.xreadgroup("g:foo","c:1",count=10,streams={"s:foo":"0"}))
    user_connection.xautoclaim("s:foo","g:foo","c:1",10,0,count=100000000000000000)
    #spray()
    #for i in range(200,500,i+2):
       # user_connection.delete("fillerA"+str(i))
