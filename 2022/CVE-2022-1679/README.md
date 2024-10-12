# Detection-and-Mitigation-for-CVE-2022-1679

The ath9k is a Linux kernel driver supporting Atheros chips. A use-after-free flaw was found in the Linux kernel’s Atheros wireless adapter driver in the way a user forces the ath9k_htc_wait_for_target function to fail with some input messages. This flaw allows a local user to crash or potentially escalate their privileges on the system. t is recommended to blacklist the module if not being used for the affected version of the CVE-2022-1679 vulnerability.

Installation

wget https://github.com/EkamSinghWalia/Detection-and-Mitigation-for-CVE-2022-1679.git

Usage

./CVE2022-1679.sh 
