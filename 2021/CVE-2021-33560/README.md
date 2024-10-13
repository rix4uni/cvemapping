# PGP client checker – CVE-2021-33560

This is a tool to check whether your OpenPGP client is affected by
[CVE-2021-33560](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-33560).

This vulnerability exposes to plaintext recovery the messages you
encrypt to some ElGamal subkeys.  The technical details of the
vulnerability are described in [this blog
post](https://ibm.github.io/system-security-research-updates/2021/07/20/insecurity-elgamal-pt1)
and [this research article](https://eprint.iacr.org/2021/923).

This tool tests whether your OpenPGP client is affected **when acting
as a sender**.  It **does not tell** whether your ElGamal subkeys
**are affected when acting as the recipient**, this is unfortunately a
computationally heavy check that can only be performed by an expert.
If you use ElGamal subkeys and are concerned about their security,
read [our
FAQ](https://ibm.github.io/system-security-research-updates/2021/07/20/insecurity-elgamal-pt1#faq).

## Requirements

You need Python version 3.8 or higher.

## How to use

This tool works by encrypting a message to a specially crafted ElGamal
subkey, then analyzing the produced ciphertext to look for the
vulnerability.

The way you import the public key and encrypt to it depends on your
OpenPGP client.  In the example below, we use GPG (whose libgcrypt is
affected until versions 1.8.8 and 1.9.3), but you will have to adapt
the steps to your own client.

1. Clone this repo and enter it
   
   ```
   git clone https://github.com/IBM/PGP-client-checker-CVE-2021-33560.git
   cd PGP-client-checker-CVE-2021-33560
   ```

2. Import the public key (this step depends on your client)
   
   ```
   gpg --import key.asc
   ```
   
3. Encrypt a message (e.g., "Hi") to the imported key (this step
   depends on your client)
   
   ```
   echo "Hi" | gpg -e --always-trust --armor -r joe@foo.bar --output ciphertext.asc
   ```

4. Run the tool on the obtained ciphertext
   
   ```
   ./sec-check.py ciphertext.asc
   ```
   
   and inspect the output. If your client is affected, you may have a
   message similar to this:
   
   ```
   Inspecting ./ciphertext.asc
   Ephemeral secret bit length: 342
   
   **Your client is affected by CVE-2021-33560!**
   
   Your client seems to be based on an old version of libgcrypt.  If a
   security patch for your client is available, install it!
   ```

## Learn more

To learn more about the vulnerability, read [our technical blog
post](https://ibm.github.io/system-security-research-updates/2021/07/20/insecurity-elgamal-pt1).
