from random import randint
from sys import exception


class chip8:
    def __init__(self) -> None:
        self.ram = [int(0) for x in range(4096)]  # 4096 bytes
        self.registers = [int(0) for x in range(16)]  # 8-bit registers (V0–VF)
        self.I_register = int(0)
        self.program_counter = int(0x200)
        self.instruction_history = []
        self.stack = []
        self.stack_pointer = 0
        self.timer_delay = int(0)  # 2 timers (delay + sound)
        self.timer_sound = int(0)  # 2 timers (delay + sound)
        self.screen = [[0 for i in range(64)] for j in range(32)]
        self.keys = [False for i in range(16)]
        self.interruption = False

    def info(self):
        print("\n>>>>\nSYSTEM")
        print("Registers: ", self.registers)
        print("I register: ", hex(self.I_register))
        print("Program Counter: ", hex(self.program_counter))
        print("Instruction: ", self.instruction_history)
        print("Stack: ", self.stack)
        print("Interrupition: ", self.interruption)
        print("DT: ", self.timer_delay)
        print("ST: ", self.timer_sound)
        # print("RAM: ", self.ram)

    def display(self):
        for i in self.screen:
            for j in i:
                print(j, end="")
            print()

    def warmup(self):
        self.timer_sound = 3
        self.instructions = {
            0: self.handle_0group,
            1: self.c1nnn,
            2: self.c2nnn,
            3: self.c3xkk,
            4: self.c4xkk,
            5: self.c5xy0,
            6: self.c6xkk,
            7: self.c7xkk,
            8: self.handle_8group,
            9: self.c9xy0,
            10: self.cannn,
            11: self.cbnnn,
            12: self.ccxkk,
            13: self.cdxyn,
            14: self.handle_egroup,
            15: self.handle_fgroup,
        }

    def load_rom(self, file_name):
        with open(file_name, "rb") as rom:
            for i in rom.read():
                self.ram[self.program_counter] = i
                self.program_counter += 1
        self.program_counter = 0x200

    def decode(self, code):
        # print(hex(code), hex(code >> 12)[2])
        ld = code >> 12
        if ld in self.instructions.keys():
            self.instructions[ld](code)
        else:
            print("Unknown opcode:", hex(code))
            # self.info()

    # First nibble (instruction group):
    # opcode >> 12

    # Second nibble:
    # (opcode >> 8) & 0xF

    # Third nibble:
    # (opcode >> 4) & 0xF

    # Last nibble:
    # opcode & 0xF

    # Last two hex digits (NN):
    # opcode & 0xFF

    # Last three hex digits (NNN):
    # opcode & 0x0FFF

    def handle_0group(self, code):
        if code == 0x00EE:
            self.c00ee()
        elif code == 0x00E0:
            self.screen = [[0 for i in range(64)] for j in range(32)]
        else:
            pass

    def c00ee(self):
        old_pointer = self.stack_pop()
        self.program_counter = old_pointer

    def c1nnn(self, code):
        self.program_counter = code & 0x0FFF

    def c2nnn(self, code):
        new_pointer = code & 0x0FFF
        self.stack_push(self.program_counter)
        self.program_counter = new_pointer

    def c3xkk(self, code):
        vx = (code >> 8) & 0xF
        kk = code & 0xFF
        if self.registers[vx] == kk:
            self.program_counter += 2

    def c4xkk(self, code):
        vx = (code >> 8) & 0xF
        kk = code & 0xFF
        if self.registers[vx] != kk:
            self.program_counter += 2

    def c5xy0(self, code):
        if (code & 0xF00F) != 0x5000:
            print("Invalid opcode: ", code)
        vx = (code >> 8) & 0xF
        vy = (code >> 4) & 0xF
        if self.registers[vx] == self.registers[vy]:
            self.program_counter += 2

    def c6xkk(self, code):
        register = (code >> 8) & 0xF
        value = code & 0xFF
        self.registers[register] = value

    def c7xkk(self, code):
        register = (code >> 8) & 0xF
        value = code & 0xFF
        self.registers[register] = (self.registers[register] + value) & 0xFF

    def handle_8group(self, code):
        self._8_group = {
            0: self.c8xy0,
            1: self.c8xy1,
            2: self.c8xy2,
            3: self.c8xy3,
            4: self.c8xy4,
            5: self.c8xy5,
            6: self.c8xy6,
            7: self.c8xy7,
            14: self.c8xye,
        }
        second_nibble = (code >> 8) & 0xF
        third_nibble = (code >> 4) & 0xF
        if (code & 0xF) in self._8_group:
            self._8_group[code & 0xF](second_nibble, third_nibble)
        else:
            print("Invalid 8 code: ", code)

    def c8xy0(self, second_nibble, third_nibble):
        self.registers[second_nibble] = self.registers[third_nibble]

    def c8xy1(self, second_nibble, third_nibble):
        #  OR
        self.registers[second_nibble] = (
            self.registers[second_nibble] | self.registers[third_nibble]
        )

    def c8xy2(self, second_nibble, third_nibble):
        # AND
        self.registers[second_nibble] = (
            self.registers[second_nibble] & self.registers[third_nibble]
        )

    def c8xy3(self, second_nibble, third_nibble):
        # XOR
        self.registers[second_nibble] = (
            self.registers[second_nibble] ^ self.registers[third_nibble]
        )

    def c8xy4(self, second_nibble, third_nibble):
        sum_result = self.registers[second_nibble] + self.registers[third_nibble]
        carry = 1 if sum_result > 255 else 0
        self.registers[second_nibble] = sum_result & 0xFF
        self.registers[15] = carry

    def c8xy5(self, second_nibble, third_nibble):
        subtract_result = (
            self.registers[second_nibble] - self.registers[third_nibble]
        ) & 0xFF
        not_borrow = (
            1 if self.registers[second_nibble] >= self.registers[third_nibble] else 0
        )
        self.registers[second_nibble] = subtract_result
        self.registers[15] = not_borrow

    def c8xy6(self, second_nibble, third_nibble):
        shift_result = self.registers[second_nibble] >> 1
        carry = self.registers[second_nibble] & 1
        self.registers[second_nibble] = shift_result
        self.registers[15] = carry

    def c8xy7(self, second_nibble, third_nibble):
        subtract_result = (
            self.registers[third_nibble] - self.registers[second_nibble]
        ) & 0xFF
        not_borrow = (
            1 if self.registers[third_nibble] >= self.registers[second_nibble] else 0
        )
        self.registers[second_nibble] = subtract_result
        self.registers[15] = not_borrow

    def c8xye(self, second_nibble, third_nibble):
        shift_result = (self.registers[second_nibble] << 1) & 0xFF
        carry = self.registers[second_nibble] >> 7
        self.registers[second_nibble] = shift_result
        self.registers[15] = carry

    def c9xy0(self, code):
        if (code & 0xF00F) != 0x9000:
            print("Invalid opcode: ", code)
        vx = (code >> 8) & 0xF
        vy = (code >> 4) & 0xF
        if self.registers[vx] != self.registers[vy]:
            self.program_counter += 2

    def cannn(self, code):
        nnn = code & 0x0FFF
        self.I_register = nnn

    def cbnnn(self, code):
        nnn = code & 0x0FFF
        self.program_counter = nnn + self.registers[0]

    def ccxkk(self, code):
        vx = (code >> 8) & 0xF
        kk = code & 0xFF
        rand = randint(0, 255)
        self.registers[vx] = rand & kk

    def cdxyn(self, code):
        vx = (code >> 8) & 0xF
        vy = (code >> 4) & 0xF
        n = code & 0xF
        sprite = self.ram[self.I_register : self.I_register + n]
        # print(sprite)
        self.draw(sprite, self.registers[vx], self.registers[vy])

    def draw(self, sprite, x, y):
        collision = False
        for row in range(len(sprite)):
            for column in range(8):
                bit = (sprite[row] >> (7 - column)) & 1
                new_x = (x + column) % 64
                new_y = (y + row) % 32
                if bit == 1:
                    if self.screen[new_y][new_x] == 1:
                        self.screen[new_y][new_x] = 0
                        collision = True
                    elif self.screen[new_y][new_x] == 0:
                        self.screen[new_y][new_x] = 1
        if collision:
            self.registers[15] = 1
        else:
            self.registers[15] = 0

    def handle_egroup(self, code):
        self.e_group = {158: self.cex9e, 161: self.cexa1}
        second_nibble = (code >> 8) & 0xF
        self.e_group[code & 0xFF](second_nibble)

    def cex9e(self, second_nibble):
        key_index = self.registers[second_nibble]
        if self.keys[key_index]:
            self.program_counter += 2

    def cexa1(self, second_nibble):
        key_index = self.registers[second_nibble]
        if not self.keys[key_index]:
            self.program_counter += 2

    def handle_fgroup(self, code):
        self.f_group = {
            7: self.cfx07,
            10: self.cfx0a,
            21: self.cfx15,
            24: self.cfx18,
            30: self.cfx1e,
            41: self.cfx29,
            51: self.cfx33,
            85: self.cfx55,
            101: self.cfx65,
        }
        second_nibble = (code >> 8) & 0xF
        self.f_group[code & 0xFF](second_nibble)

    def cfx07(self, second_nibble):
        self.registers[second_nibble] = self.timer_delay

    def cfx0a(self, second_nibble):
        # wait for key press and store in Vx
        # simulate any key is pressed
        self.interruption = True
        for key in range(15):
            if self.keys[key]:
                self.registers[second_nibble] = key
                self.interruption = False

    def cfx15(self, second_nibble):
        self.timer_delay = self.registers[second_nibble]

    def cfx18(self, second_nibble):
        self.timer_sound = self.registers[second_nibble]

    def cfx1e(self, second_nibble):
        self.I_register = (self.I_register + self.registers[second_nibble]) & 0xFFFF

    def cfx29(self, second_nibble):
        # TODO: add the letters to the memory
        # make I point to the digit x
        print("Command Fx29 not implemented")
        pass
        # self.I_register += self.registers[second_nibble]

    def cfx33(self, second_nibble):
        print("Command Fx33 not implemented")
        pass
        # self.I_register += self.registers[second_nibble]

    def cfx55(self, second_nibble):
        for iterate in range(second_nibble + 1):
            self.ram[self.I_register + iterate] = self.registers[iterate]
            if self.I_register + iterate >= len(self.ram):
                print("Memory write overflow")

    def cfx65(self, second_nibble):
        for iterate in range(second_nibble + 1):
            self.registers[iterate] = self.ram[self.I_register + iterate]

    def loop(self):
        if self.timer_delay > 0:
            self.timer_delay -= 1

        if self.timer_sound > 0:
            self.timer_sound -= 1

        if not self.interruption:
            self.instruction = self.read_ram()
            self.instruction_history.append(hex(self.instruction))
            self.program_counter += 2

        self.decode(self.instruction)


    def stack_push(self, value):
        # If len(self.stack) >= 16 → error
        # If len(self.stack) == 0 → error
        self.stack.append(value)

    def stack_pop(self):
        # If len(self.stack) >= 16 → error
        # If len(self.stack) == 0 → error
        return self.stack.pop()

    def read_ram(self):
        reading1 = self.ram[self.program_counter]
        reading2 = self.ram[self.program_counter + 1]
        return (reading1 << 8) | reading2
