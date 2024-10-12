curl https://pyenv.run | bash
python3 -m ensurepip --upgrade
python3 -m pip install -r ../requirements.txt
python3 ../main.py
