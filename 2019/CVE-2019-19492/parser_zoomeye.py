import sys

try:
    with open(sys.argv[1],"r") as f:
        text = f.readlines()

    for i in text:
        line = ":".join(i.split())
        if "total" not in i and "ip" not in i:
            print(line)

except:
    print("Usage : python parse.py /path/to/file.txt")
    sys.exit(1)
