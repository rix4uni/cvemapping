# CVE-2024-22853
D-LINK Go-RT-AC750 GORTAC750_A1_FW_v101b03 has a hardcoded password for the Alphanetworks account, which allows remote attackers to obtain root access via a telnet session.

# PoC

https://www.dlink.com/se/sv/products/go-rt-ac750-wireless-ac750-dual-band-easy-router?revision=deu_reva#downloads

![image](https://github.com/FaLLenSKiLL1/CVE-2024-22853/assets/43922662/ebbc672f-9496-4969-86d3-aca4dea8016a)

![image](https://github.com/FaLLenSKiLL1/CVE-2024-22853/assets/43922662/95609d20-b461-446b-8d3f-6d3fff14e0c5)

![image](https://github.com/FaLLenSKiLL1/CVE-2024-22853/assets/43922662/5978844e-2f7b-45fb-9dd8-1dd151dae519)

```
binwalk GORTAC750_A1_FW_v101b03.bin -e
```

![image](https://github.com/FaLLenSKiLL1/CVE-2024-22853/assets/43922662/84abe358-4501-48f9-8a14-5395b96b1df2)

```
cat './go-rt-ac750_fw_reva_1-01b03_eu_multi_20141017/_GORTAC750_A1_FW_v101b03.bin.extracted/squashfs-root/etc/init0.d/S80telnetd.sh'
```

![image](https://github.com/FaLLenSKiLL1/CVE-2024-22853/assets/43922662/833c80e3-d42e-472e-98de-554d470d19d0)

![image](https://github.com/FaLLenSKiLL1/CVE-2024-22853/assets/43922662/e3736618-37ec-4615-bc67-45ee4fe6ebd3)

![image](https://github.com/FaLLenSKiLL1/CVE-2024-22853/assets/43922662/e548c887-01de-4395-a6bb-7f849c6e9ccb)

# Hardcoded Creds:

Alphanetworks:wrgac18_dlob.hans_ac750
