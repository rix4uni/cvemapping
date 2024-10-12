# CVE-2023-48034

I have discovered weak encryption used in the wireless protocol of the Acer Wireless Keyboard SK-9662 (FCC ID: H4IKB9662). This weak encryption allows an attacker to easily monitor and log keystrokes and also inject arbitrary keystrokes.
## Intro
The keyboard uses a Texas Instruments CC2545 chip, transmitting data using the Enhanced Shockburst protocol developed by Nordic Semiconductors. The payload consists of 12 bytes, the first byte appears to be a constant value (0x48 in my testing). The second byte is the modifier byte (ctrl, shift etc.), the third and fourth bytes are consumer and power control keys. The fifth thru tenth bytes are the key codes. The eleventh bytes acts as a checksum and the twelfth byte is the random number used for encryption.
## Encryption Scheme
Payload encryption starts with the generation of a random byte from radio noise. A different byte stored in the firmware (keyvalue) is used as a key for AES. Both the key and random byte are zero padded to 128 bits and sent to the AES coprocessor on the CC2545. The AES coprocessor is configured for CBC mode with a null IV. The output of the AES coprocessor will be referred to as the xorkey. The first eleven bytes of the payload are xor'ed with the corresponding bytes in the xorkey. The random byte is the last byte of the payload in order for the receiver to decrypt the payload.

Decryption of the payload is similar to encryption. The twelfth byte of the payload (the random value) along with the keyvalue (known by the receiver ahead of time) is used to generate the xorkey and xor'ed with the encrypted payload.
## Exploit
This encryption scheme is easily circumvented due to the use of only a one byte AES key. Since the key is limited to only 256 possible values, the key can be easily brute-forced within seconds. The python script in this repository shows brute force decryption of a captured encrypted packet.

In order for this vulnerability to exploited, an attacker must have means to capture the 2.4 GHz radio traffic. This requires close physical proximity to the target keyboard. However, once a single packet is captured, the AES key can be brute-forced within seconds and real-time keylogging and keystroke injection is possible, allowing access to the victim's computer. A popular wireless hacking tool, jackit (https://github.com/insecurityofthings/jackit), can be extended to support sniffing and injecting keystrokes into nearby SK-9662 keyboards all on a cheap 2.4 GHz USB dongle.
## Mitigation
The SK-9662 keyboard is an obsolete product. An update mechanism for the keyboard does not exist and users should discontinue usage of the vulnerable keyboard. Acer recommends switching to a newer keyboard product.