import os

os.system("javac -source 8 -target 8 src/artsploit/AwesomeScriptEngineFactory.java")
os.system("jar -cvf yaml-payload.jar -C src/ .")