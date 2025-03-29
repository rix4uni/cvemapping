# CVE-2023-0748
BTCPayServer 1.7.5 and lower version is vulnerable for Open Redirection attack.

<strong>Step to Reproduce</strong>

1. Login your account on 

https://mainnet.demo.btcpayserver.org/login

2. Then Click the link below

https://mainnet.demo.btcpayserver.org/recovery-seed-backup?cryptoCode=BTC&mnemonic=above&passphrase=&isStored=false&requireConfirm=true&returnUrl=//evil.com

3. Check the `I have written down my recovery phrase and stored it in a secure location`

4. Then click `Done`

You will be redirected to evil.com



<br><br>

<h1>Credits</h1>

• Jefferson Gonzales (Gonz)<br>
• Link: https://twitter.com/gonzxph
