# CVE-2024-42861
The DOS attack against IEEE 802.1AS standard(gPTP protocol)<br><br>
[CVE ID]<br>
CVE-2024-42861<br><br>
[PRODUCT]<br>
IEEE 802.1AS standard<br><br>
[VERSION]<br>
IEEE 802.1AS-2020, IEEE 802.1AS-2010<br><br>
[PROBLEM]<br>
DOS attack<br><br>
[DESCRIPTION]<br>
When a port of a device with IEEE 802.1AS enabled receives two Pdelay_Req messages with different clockID, the time synchronization function of that port becomes disabled, leading to a denial of service attack.Attacker and the target are on the same Ethernet network. The attacker sends two Pdelay_Req messages with different ClockID to the target. Upon receiving these messages, the target's port will automatically terminate clock synchronization communication with the peer port, rendering the clock synchronization function of that port unavailable for a certain period of time. This DOS attack was successfully reproduced on linuxPTP(a software that implemnets the ptp and gptp protocols).
