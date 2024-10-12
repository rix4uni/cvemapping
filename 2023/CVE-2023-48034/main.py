# Copyright (C) 2023 Alex Parker

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # pip install cryptography

iv = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) # iv is null
packet = bytearray([0xB8,0xA0,0x1D,0x2B,0x32,0xEA,0x62,0x5E,0xEA,0x6E,0x12,0xFB]) # encrypted packet, last byte is random value used to generate xorkey
keyvalue = 0
decryptedpacket = bytearray(11)

for x in range(256): # aes key is limited to one byte, despite having 16 bytes available
    key = bytearray([x,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    xorkey = encryptor.update(bytearray([packet[11],0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])) + encryptor.finalize() # generate xorkey using random value and current aes key
    checksum = 0
    for y in range(10):
        decryptedpacket[y] = packet[y] ^ xorkey[y] # before transmission, packet is xor'ed with aes generated xorkey
        checksum = (checksum + decryptedpacket[y]) & 0xFF # update checksum
    decryptedpacket[10] = packet[10] ^ xorkey[10] # decrypted packet checksum
    checksum = checksum ^ 0xFF # final step of checksum is inverting all bits
    if (checksum == decryptedpacket[10]): # if calculated checksum and decrypted packet checksum match, aes key was found
        keyvalue = x
        break
print("AES Key is " + hex(keyvalue))
print("Decrypted packet is 0x" + decryptedpacket.hex())
