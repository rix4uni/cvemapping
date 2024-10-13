# CVE-2019-1653
A vulnerability in the web-based management interface of Cisco Small Business RV320 and RV325 Dual Gigabit WAN VPN Routers could allow an unauthenticated, remote attacker to retrieve sensitive information.


Script python sederhana ini merupakan automation exploit pada CVE-2019-1653 yang meng-infeksi perangkat Cisco Small Business RV320 dan RV325. Kerentanan pertama yang dieksploitasi yaitu SIE(Sensitive information exposures) dimana attacker dengan level unauthenticated bisa melakukan stealing credential untuk memasuki router dashboard dan melakukan command injection pada halaman generate certificate dengan membuka telnet port sehingga attacker dapat melakukan compromised lebih pada perangkat yang vulnerable.    
