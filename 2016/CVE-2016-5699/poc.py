import urllib.request
import traceback

print("#######################################")
print("Testing HTTP Header injection in Python")
print("Origin : http://blog.blindspotsecurity.com/2016/06/advisory-http-header-injection-in.html")
print("bunseokbot@UpRoot")
print("#######################################")

while True:
	try:
		url = input("URL : ")
		info = urllib.request.urlopen(url).info()
		print(info)
	except KeyboardInterrupt as kie:
		print("KeyboardInterrupt event found!\nTerminating Program..")
		break
	except Exception as e:
		print(traceback.format_exc())

