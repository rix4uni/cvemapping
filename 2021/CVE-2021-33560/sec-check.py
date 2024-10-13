#!/usr/bin/env python3
import sys, base64, re

def parse(input):
    '''
    Parse OpenPGP message (armored or not)
    '''
    # read OpenPGP ciphertext stream in one shot
    buffer = input.read()

    # de-armor if necessary
    if buffer.startswith(b'-----BEGIN PGP MESSAGE-----'):
        m = re.match(r'-----BEGIN PGP MESSAGE-----.*\r?\n\r?\n(.+)\n=([a-zA-Z0-9/+]{4})\r?\n-----END PGP MESSAGE-----', buffer.decode(), re.DOTALL)
        if m is None:
            print('Error decoding the ascii-armored message')
            sys.exit(1)
        else:
            buffer = base64.b64decode(m[1])

    # find all ElGamal ciphertexts and output their components
    while buffer:
       b, buffer = buffer[0], buffer[1:]
       if not (b & 0x80 == 0x80):
           print("Error decoding the message")
           sys.exit(1)
       new_format = b & 0x40 == 0x40

       if new_format:
          packet_type = (b & 0x3f) >> 0
          packet = b''
          while True:
             b, buffer = buffer[0], buffer[1:]
             if 0 <= b <= 191: # one-octet length
                read_len = b
                final = True
             elif 192 <= b <= 223: # two-octet length
                bb, buffer = buffer[0], buffer[1:]
                read_len = ((b - 192) << 8) + bb + 192
                final = True
             elif b == 255: # five-octet length
                b1, b2, b3, b4, buffer = buffer[0], buffer[1], buffer[2], buffer[3], buffer[4:]
                read_len = (b1 << 24) | (b2 << 16) | (b3 << 8) | b4
                final = True
             else: # partial packet
                read_len = 1 << (b & 0x1f)
                final = False
             partial_packet, buffer = buffer[:read_len], buffer[read_len:]
             packet += partial_packet
             if final: break

       else: # old format
          packet_type = (b & 0x3c) >> 2
          length_type = (b & 0x03) >> 0

          if length_type == 0: # one-octet header
             b, buffer = buffer[0], buffer[1:]
             read_len = b
          elif length_type == 1: # two-octet header
             b1, b2, buffer = buffer[0], buffer[1], buffer[2:]
             read_len = (b1 << 8) | b2
          elif length_type == 2: # four-octet header
             b1, b2, b3, b4, buffer = buffer[0], buffer[1], buffer[2], buffer[3], buffer[4:]
             read_len = (b1 << 24) | (b2 << 16) | (b3 << 8) | b4
          else: # length_type == 3
             assert False, "not implemented"
          packet, buffer = buffer[:read_len], buffer[read_len:]

       if packet_type != 1: continue # process exclusively "Public-Key Encrypted Session Key Packets (Tag 1)" packets

       version = packet[0]
       assert version == 3, "invalid input format"

       keyID = packet[1:9]

       algo = packet[9]
       if algo != 16: continue # process exclusively "ElGamal (Encrypt Only)" keys

       packet, elgA = packet[10:], 0
       lenA1, lenA2 = packet[0], packet[1]
       leninbitsA = (lenA1 << 8) | lenA2
       assert leninbitsA > 0, "invalid input format"
       leninbytesA = (leninbitsA + 7) // 8
       for c in packet[2:2 + leninbytesA]:
          elgA = (elgA << 8) + c
       assert (1 << (leninbitsA - 1)) <= elgA < (1 << leninbitsA), "invalid input format"

       packet, elgB = packet[2 + leninbytesA:], 0
       lenB1, lenB2 = packet[0], packet[1]
       leninbitsB = (lenB1 << 8) | lenB2
       assert leninbitsB > 0, "invalid input format"
       leninbytesB = (leninbitsB + 7) // 8
       for c in packet[2:2 + leninbytesB]:
          elgB = (elgB << 8) + c
       assert (1 << (leninbitsB - 1)) <= elgB < (1 << leninbitsB), "invalid input format"

       packet = packet[2 + leninbytesB:]
       assert not packet, "invalid input format"

       return elgA, elgB


# PK Paramters
p = 2**2037 * 3 * 7 * 61 + 1
g = 5

# Dlog in the 2**2037 part
def dlog2(g, h, n):
    if n == 1:
        return 1 if g == h else 0
    else:
        a = n // 2
        b = n - a
        x = dlog2(pow(g, 2**a, p), pow(h, 2**a, p), b)
        y = dlog2(pow(g, 2**b, p), h * pow(g, -x, p) % p, a)
        return (y << b) + x

# Full dlog
def dlog(g, h):
    f = 3 * 7 * 61
    x = dlog2(pow(g, f, p), pow(h, f, p), 2037)
    g = pow(g, 2**2037, p)
    h = pow(h, 2**2037, p)
    y = next(i for i in range(f) if pow(g, i, p) == h)
    # Hand computed CRT
    return (x - x*2**(60*34) +  y*8*2**2037) % (p-1)


###################
if __name__ == '__main__':
    v = sys.version_info
    if v[0] < 3 or v[1] < 8:
        print('Need Python 3.8 or higher.')
        sys.exit(1)

    if len(sys.argv) > 1:
        b = open(sys.argv[1], 'rb')
        print('Inspecting %s...' % sys.argv[1])
    else:
        b = sys.stdin.buffer
        print('Inspecting stdin...')
    c0, c1 = parse(b)
    y = dlog(g, c0)
    l = y.bit_length()
    print('Ephemeral secret bit length: %d\n' % l)

    if l > 2018:
        print('**Your client is not affected.**')
    elif 334 <= l <= 344:
        print('''**Your client is affected by CVE-2021-33560!**

Your client seems to be based on an old version of libgcrypt.  If a
security patch for your client is available, install it!''')
    else:
        print('**Your client is affected by CVE-2021-33560!**')
