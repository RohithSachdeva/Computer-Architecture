"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0

    # mar is sort of like a key value in the ram

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""
        address = 0
        if len(sys.argv) != 2:
            print("Proper usage: ls8.py progname")
            sys.exit(1)
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    
                    if line == '' or line[0] == "#":
                        continue

                    try:
                        str_value = line.split("#")[0]
                        value = int(str_value, 2)

                    except ValueError:
                        print(f"Invalid number: {str_value}")
                        sys.exit(1)

                    self.ram[address] = value
                    address += 1

        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == LDI:
                self.register[operand_a] = operand_b
                self.pc += 3
                # LDI function

            elif ir == PRN:
                print(self.register[operand_a])
                self.pc += 2
                # PRN function

            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3


            elif ir == HLT:
                self.pc += 1
                running = False
                # Halt function
            
#MUL  10100010 00000aaa 00000bbb

"""
 program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

"""


"""
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




"""
