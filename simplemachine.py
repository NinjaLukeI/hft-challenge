class SimpleMachine:
    def __init__(self):
        self.registers = [0] * 16

    def execute_program(self, program):
        for instruction in program:
            op, *operands = instruction.split()
            if op == 'ADD':
                value = int(operands[0])
                src_register = int(operands[1][1:])
                dest_register = int(operands[2][1:])
                self.registers[dest_register] = self.registers[src_register] + value
            elif op == 'STORE':
                value = int(operands[0])
                dest_register = int(operands[1][1:])
                self.registers[dest_register] = value
            elif op == 'MOV':
                src_register = int(operands[0][1:])
                dest_register = int(operands[1][1:])
                self.registers[dest_register] = self.registers[src_register]
            else:
                print(f"Invalid instruction: {instruction}")

    def sum_registers(self):
        return str(sum(self.registers))