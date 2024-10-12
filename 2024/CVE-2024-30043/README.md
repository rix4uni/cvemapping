# CVE-2024-30043-XXE
# Credit

The impact of the vulnerability is limited at present, but thanks to https://x.com/chudyPB for providing a clever bypass idea.

>https://x.com/chudyPB

> https://www.zerodayinitiative.com/blog/2024/5/29/cve-2024-30043-abusing-url-parsing-confusion-to-exploit-xxe-on-sharepoint-server-and-cloud

>https://x.com/chudyPB/status/1797707100421751007

# Usage

change these:

![](https://cdn.jsdelivr.net/gh/W01fh4cker/blog_image@main/image-20240607023526043.png)

```shell
pip install requests requests_ntlm flask
python CVE-2024-30043-XXE.py
```

test on `Microsoft Sharepoint Server 2019`(`16.0.10409.20027`):

![](https://cdn.jsdelivr.net/gh/W01fh4cker/blog_image@main/image-20240607023535435.png)
