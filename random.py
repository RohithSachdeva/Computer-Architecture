import sys

# Memory
# ------
# Holds bytes
#
# Big array of bytes
#
# To get or set data in memory, you need the index in the array
#
# These terms are equivalent:
# * Index into the memory array
# * Address
# * Location
# * Pointer

# "opcode" == the instruction byte
# "operands" == arguments to the instruction

PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3
PRINT_REG = 4

memory = [0] * 256

# Variables are called "registers".
# * There are a fixed number
# * They have preset names: R0, R1, R2, R3 ... R7
#
# Registers can each hold a single byte

register = [0] * 8  # [0,0,0,0,0,0,0,0]


# Read program data

address = 0

if len(sys.argv) != 2:
	print("usage: comp.py progname")
	sys.exit(1)

try:
	with open(sys.argv[1]) as f:
		for line in f:
			line = line.strip()

			if line == '' or line[0] == "#":
				continue

			try:
				str_value = line.split("#")[0]
				value = int(str_value, 10)

			except ValueError:
				print(f"Invalid number: {str_value}")
				sys.exit(1)

			memory[address] = value
			address += 1

except FileNotFoundError:
	print(f"File not found: {sys.argv[1]}")
	sys.exit(2)

# Start execution at address 0

# Keep track of the address of the currently-executing instruction
pc = 0   # Program Counter, pointer to the instruction we're executing

halted = False

while not halted:
	instruction = memory[pc]

	if instruction == PRINT_BEEJ:
		print("Beej!")
		pc += 1

	elif instruction == HALT:
		halted = True
		pc += 1

	elif instruction == SAVE_REG:
		reg_num = memory[pc + 1]
		value = memory[pc + 2]
		register[reg_num] = value
		pc += 3

	elif instruction == PRINT_REG:
		reg_num = memory[pc + 1]
		print(register[reg_num])
		pc += 2

	else:
		print(f"unknown instruction {instruction} at address {pc}")
		sys.exit(1)