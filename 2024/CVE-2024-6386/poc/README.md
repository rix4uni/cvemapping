# How to run
## Preparing
WordPress doesn't allow us to edit posts and many other things via REST or with help of scripts.

To bypass this i used a [Selenium](https://www.selenium.dev).
It's included into `requirements.txt` so it will be automatically installed in `Run sploit` part. 

Nevertheless to run sploit u need to install a chromedriver.
You can find a chromedriver for your OS [here](https://googlechromelabs.github.io/chrome-for-testing/).

Afer installing a chromedriver you can run sploit.
## Run sploit
Make a virtual environment and activate it: 
```
python3 -m venv venv
source venv/bin/activate
```

Install requirements:
```
pip3 install -r requirements.txt
```

Run a sploit:
```
python3 sploit.py
```
