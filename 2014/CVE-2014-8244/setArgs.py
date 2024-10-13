import argparse

parser = argparse.ArgumentParser()
#adding command line arguements
parser.add_argument("--target",help="single ip to scan")
parser.add_argument("--port",help="The port to scan",default=80)
parser.add_argument("--file",help="File with IPs to scan, make sure to add .txt")
parser.add_argument("--timeout", help="Time in seconds for timeout default is 5", default=5)
parser.add_argument("--checkPass",nargs='?',const=1,help="check if default password is in use")
parser.add_argument("--save", help=" File to save hits to, make sure to add .txt")
args = parser.parse_args()