"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

#Flag bits 00000LGE

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.sp = 7
        self.register[self.sp] = 0xF4
        self.flag_register = [0] * 8


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
        elif op == "CMP":
            if self.register[reg_a] == self.register[reg_b]:
                self.flag_register = 0b00000001
            if self.register[reg_a] < self.register[reg_b]:
                self.flag_register = 0b00000100
            if self.register[reg_a] > self.register[reg_b]:
                self.flag_register = 0b00000010
 

        #Flag bits 00000LGE
        #less than  -> L = 1
        #g than -> g = 1
        #e then -> E = 1
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
    
    def push_val(self, value):
        self.register[self.sp] -= 1
        top_Of_Stack = self.register[self.sp]
        self.ram[top_Of_Stack] = value
    
    def pop_val(self):
        top_Of_Stack = self.register[self.sp]
        value = self.ram[top_Of_Stack]
        self.register[self.sp] += 1
        return value


    def run(self):
        """Run the CPU."""
        running = True
        

        while running:
            instruction = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            

            if instruction == LDI:
                self.register[operand_a] = operand_b
                self.pc += 3
                # LDI function

            elif instruction == PRN:
                print(self.register[operand_a])
                self.pc += 2
                # PRN function

            elif instruction == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            
            elif instruction == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            
            elif instruction == PUSH:
                self.register[self.sp] -= 1
                value = self.register[operand_a]
                top_Of_Stack = self.register[self.sp]
                self.ram[top_Of_Stack] = value
                self.pc += 2
            
            elif instruction == POP:
                top_Of_Stack = self.register[self.sp]
                value = self.ram[top_Of_Stack]
                self.register[operand_a] = value
                self.register[self.sp] += 1
                self.pc += 2
            
            elif instruction == CALL:
                return_address = (self.pc + 2)
                self.push_val(return_address)
                subroutine_address = self.register[operand_a]
                self.pc = subroutine_address
            
            elif instruction == RET:
                return_address = self.pop_val()
                self.pc = return_address
            
            elif instruction == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3
            
            elif instruction == JMP:
                self.pc = self.register[operand_a]
            
            elif instruction == JEQ:
                if self.flag_register == 0b00000001:
                    self.pc = self.register[operand_a]
                else:
                    self.pc += 2

            elif instruction == JNE:
                if self.flag_register != 0b00000001:
                    self.pc = self.register[operand_a]
                else:
                    self.pc += 2


            elif instruction == HLT:
                self.pc += 1
                running = False
                # Halt function
            else: 
                print(f"unknown instruction {instruction:08b} at address {self.pc}")
                sys.exit(1)