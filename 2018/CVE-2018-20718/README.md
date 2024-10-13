# CVE-2018-20718
This is a POC for CVE-2018-20718. It is a PHP Object injection vulnerability. The vulnerability affect all version of Pydio before 8.2.1 and leads to Unauthenticated Remote Code Execution. It was originaly found by RIPS.

I found a gadget in Pydio\Core\Controller\ShutdownScheduler which allows remote code execution if combined with the already known GuzzleHttp\Psr7\FnStream gadget.

**Exemple of exploitation**

![image](https://user-images.githubusercontent.com/8191240/61220331-63620c80-a716-11e9-9656-932f51553541.png)
![image](https://user-images.githubusercontent.com/8191240/61220336-65c46680-a716-11e9-9180-9fa5225e3da2.png)

**Technical details**

https://blog.ripstech.com/2018/pydio-unauthenticated-remote-code-execution/
