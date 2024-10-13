from flask import Flask, request

app = Flask(__name__)
app.debug = True

@app.route("/vulntest")
def vulntest():
	print("###############################################")
	print("Request Header")
	print("###############################################")
	print(request.headers)
	print("###############################################")
	return ''

if __name__ == "__main__":
	app.run(port=12345, threaded=True)  # localhost only
