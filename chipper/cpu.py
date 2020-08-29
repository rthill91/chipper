from .disassembler import disassemble
from .display import Display
from .font_set import FONT_SET

import numpy as np

from random import randint
import warnings
import logging


warnings.filterwarnings('ignore')


# DISPLAY_HEIGHT = 64
# DISPLAY_WIDTH = 32
DISPLAY_HEIGHT = 32
DISPLAY_WIDTH = 64


class CPU:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.reset()

        self._display = Display(DISPLAY_WIDTH, DISPLAY_HEIGHT)

        self._inst_switch = {
            'CLS': self._cls,
            'RET': self._ret,
            'JP_ADDR': self._jp_addr,
            'CALL_ADDR': self._call_addr,
            'SE_VX_NN': self._se_vx_nn,
            'SNE_VX_NN': self._sne_vx_nn,
            'SE_VX_VY': self._se_vx_vy,
            'LD_VX_NN': self._ld_vx_nn,
            'ADD_VX_NN': self._add_vx_nn,
            'LD_VX_VY': self._ld_vx_vy,
            'OR_VX_VY': self._or_vx_vy,
            'AND_VX_VY': self._and_vx_vy,
            'XOR_VX_VY': self._xor_vx_vy,
            'ADD_VX_VY': self._add_vx_vy,
            'SUB_VX_VY': self._sub_vx_vy,
            'SHR_VX_VY': self._shr_vx_vy,
            'SUBN_VX_VY': self._subn_vx_vy,
            'SHL_VX_VY': self._shl_vx_vy,
            'SNE_VX_VY': self._sne_vx_vy,
            'LD_I_ADDR': self._ld_i_addr,
            'JP_V0_ADDR': self._jp_v0_addr,
            'RND_VX_NN': self._rnd_vx_nn,
            'DRW_VX_VY_N': self._drw_vx_vy_n,
            'SKP_VX': self._skp_vx,
            'SKNP_VX': self._sknp_vx,
            'LD_VX_DT': self._ld_vx_dt,
            'LD_VX_N': self._ld_vx_n,
            'LD_DT_VX': self._ld_dt_vx,
            'LD_ST_VX': self._ld_st_vx,
            'ADD_I_VX': self._add_i_vx,
            'LD_F_VX': self._ld_f_vx,
            'LD_B_VX': self._ld_b_vx,
            'LD_I_VX': self._ld_i_vx,
            'LD_VX_I': self._ld_vx_i,
        }
        self._logger.info('CPU Initialized...')

    def reset(self):
        self._logger.info('command: reset')
        self._memory = np.zeros(4096, dtype='u1')
        self._registers = np.zeros(16, dtype='u1')
        self._stack = np.zeros(16, dtype='u2')
        # Program Counter
        self._pc = 0x200
        # index register
        self._i = 0
        # stack pointer
        self._sp = -1
        # sound timer
        self._st = 0
        # delay timer
        self._dt = 0

    def load(self, rom):
        self._logger.info('command: load')
        self.reset()
        # Load default font set
        for i in range(len(FONT_SET)):
            self._memory[i] = FONT_SET[i]

        mem_start = self._pc
        for i in range(len(rom)):
            self._memory[mem_start + i] = rom[i]

    def tick(self):
        """
        Decrement Timers
        """
        if self._dt > 0:
            self._dt -= 1

        if self._st > 0:
            self._st -= 1

    def step(self):
        opcode = self._fetch()
        instruction = self._decode(opcode)
        self._execute(instruction)

    def _fetch(self):
        return (self._memory[self._pc] << 8) | (self._memory[self._pc + 1])

    def _decode(self, opcode):
        return disassemble(opcode)

    def _execute(self, instruction):
        inst_id, args = instruction

        try:
            self._inst_switch[inst_id](args)
        except KeyError:
            raise Exception(f"Illegal Instruction: {inst_id}")

    def _next_instruction(self):
        self._pc += 2

    def _skip_instruction(self):
        self._pc += 4

    def _cls(self, args):
        """
        00E0
        Clear the display
        """
        self._logger.info('opcode: CLS')
        self._logger.debug(args)
        self._display.clear()
        self._next_instruction()

    def _ret(self, args):
        """
        00EE
        Return from a subroutine
        The interpreter sets the program counter to the address at the top of the stack, then subtracts 1 from the stack pointer.
        """
        self._logger.info('opcode: RET')
        self._logger.debug(args)
        if self._sp == -1:
            raise Exception('Stack Underflow')
        self._pc = self._stack[self._sp]
        self._sp -= 1

    def _jp_addr(self, args):
        """
        1nnn
        Jump to location nnn
        The interpreter sets the program counter to nnn.
        """
        self._logger.info('opcode: JP_ADDR')
        self._logger.debug(args)
        addr = args[0]
        self._pc = addr

    def _call_addr(self, args):
        """
        2nnn
        Call subroutine at nnn
        The interpreter increments the stack pointer, then puts the current PC on the top of the stack. The PC is then set to nnn.
        """
        self._logger.info('opcode: CALL_ADDR')
        self._logger.debug(args)
        addr = args[0]
        if self._sp >= 15:
            raise Exception('Stack Overflow')
        self._sp += 1
        self._stack[self._sp] = self._pc + 2
        self._pc = addr

    def _se_vx_nn(self, args):
        """
        3xnn
        Skip next instruction if Vx = nn
        The interpreter compares register Vx to nn, and if they are equal, increments the program counter by 2.
        """
        self._logger.info('opcode: SE_VX_NN')
        self._logger.debug(args)
        vx = args[0]
        nn = args[1]
        if self._registers[vx] == nn:
            self._skip_instruction()
        else:
            self._next_instruction()

    def _sne_vx_nn(self, args):
        """
        4xnn
        Skip next instruction if Vx != nn
        The interpreter compares register Vx to nn, and if they are not equal, increments the program counter by 2.
        """
        self._logger.info('opcode: SNE_VX_NN')
        self._logger.debug(args)
        vx = args[0]
        nn = args[1]
        if self._registers[vx] != nn:
            self._skip_instruction()
        else:
            self._next_instruction()

    def _se_vx_vy(self, args):
        """
        5xy0
        Skip next instruction if Vx = Vy
        The interpreter compares register Vx to register Vy, and if they are equal, increments the program counter by 2.
        """
        self._logger.info('opcode: SE_VX_VY')
        self._logger.debug(args)
        vx = args[0]
        vy = args[1]
        if self._registers[vx] == self._registers[vy]:
            self._skip_instruction()
        else:
            self._next_instruction()

    def _ld_vx_nn(self, args):
        """
        6xnn
        Set Vx = nn
        The interpreter puts the value nn into register Vx
        """
        self._logger.info('opcode: LD_VX_NN')
        self._logger.debug(args)
        vx = args[0]
        nn = args[1]
        self._registers[vx] = nn
        self._next_instruction()

    def _add_vx_nn(self, args):
        """
        7xnn
        Set Vx = Vx + nn
        Adds the value nn to the value of register Vx, then stores the result in Vx.
        """
        self._logger.info('opcode: ADD_VX_NN')
        self._logger.debug(args)
        vx = args[0]
        nn = args[1]
        self._registers[vx] += nn
        self._next_instruction()

    def _ld_vx_vy(self, args):
        """
        8xy0
        Set Vx = Vy
        Stores the value of register Vy in register Vx.
        """
        self._logger.info('opcode: LD_VX_VY')
        self._logger.debug(args)
        vx = args[0]
        vy = args[1]
        self._registers[vx] = self._registers[vy]
        self._next_instruction()

    def _or_vx_vy(self, args):
        """
        8xy1
        Set Vx = Vx OR Vy
        Performs a bitwise OR on the values of Vx and Vy, then stores the result in Vx.
        """
        self._logger.info('opcode: OR_VX_VY')
        self._logger.debug(args)
        vx = args[0]
        vy = args[1]
        self._registers[vx] |= self._registers[vy]
        self._next_instruction()

    def _and_vx_vy(self, args):
        """
        8xy2
        Set Vx = Vx AND Vy
        Performs a bitwise AND on the values of Vx and Vy, then stores the result in Vx.
        """
        self._logger.info('opcode: AND_VX_VY')
        self._logger.debug(args)
        vx = args[0]
        vy = args[1]
        self._registers[vx] &= self._registers[vy]
        self._next_instruction()

    def _xor_vx_vy(self, args):
        """
        8xy3
        Set Vx = Vx XOR Vy
        Performs a bitwise exclusive OR on the values of Vx and Vy, then stores the result in Vx.
        """
        self._logger.info('opcode: XOR_VX_VY')
        self._logger.debug(args)
        vx = args[0]
        vy = args[1]
        self._registers[vx] ^= self._registers[vy]
        self._next_instruction()

    def _add_vx_vy(self, args):
        """
        8xy4
        Set Vx = Vx + Vy, set VF = carry
        The values of Vx and Vy are added together. If the result is greater than 8 bits (i.e., > 255,) VF is set to 1, otherwise 0. Only the lowest 8 bits of the result are kept, and stored in Vx.
        """
        self._logger.info('opcode: ADD_VX_VY')
        self._logger.debug(args)
        vx = args[0]
        vy = args[1]
        self._registers[vx] += self._registers[vy]
        self._registers[0xf] = int(self._registers[vx] + self._registers[vy] > 0xff)
        self._next_instruction()

    def _sub_vx_vy(self, args):
        """
        8xy5
        Set Vx = Vx - Vy, set VF = NOT borrow
        If Vx > Vy, then VF is set to 1, otherwise 0. Then Vy is subtracted from Vx, and the results stored in Vx.
        """
        self._logger.info('opcode: SUB_VX_VY')
        self._logger.debug(args)
        vx = args[0]
        vy = args[1]
        self._registers[0xf] = int(self._registers[vx] > self._registers[vy])
        self._registers[vx] -= self._registers[vy]
        self._next_instruction()

    def _shr_vx_vy(self, args):
        """
        8xy6
        Set Vx = Vx SHR 1
        If the least-significant bit of Vx is 1, then VF is set to 1, otherwise 0. Then Vx is divided by 2.
        """
        self._logger.info('opcode: SHR_VX_VY')
        self._logger.debug(args)
        vx = args[0]
        self._registers[0xf] =  (self._registers[vx] & 1)
        self._registers[vx] >>= 1
        self._next_instruction()

    def _subn_vx_vy(self, args):
        """
        8xy7
        Set Vx = Vy - Vx, set VF = NOT borrow
        If Vy > Vx, then VF is set to 1, otherwise 0. Then Vx is subtracted from Vy, and the results stored in Vx.
        """
        self._logger.info('opcode: SUBN_VX_VY')
        self._logger.debug(args)
        vx = args[0]
        vy = args[1]
        self._registers[0xf] = int(self._registers[vx] <= self._registers[vy])
        self._registers[vx] = self._registers[vy] - self._registers[vx]
        self._next_instruction()

    def _shl_vx_vy(self, args):
        """
        8xyE
        Set Vx = Vx SHL 1
        If the most-significant bit of Vx is 1, then VF is set to 1, otherwise to 0. Then Vx is multiplied by 2.
        """
        self._logger.info('opcode: SHL_VX_VY')
        self._logger.debug(args)
        vx = args[0]
        self._registers[0xf] = self._registers[vx] >> 7
        self._registers[vx] <<= 1
        self._next_instruction()

    def _sne_vx_vy(self, args):
        """
        9xy0
        Skip next instruction if Vx != Vy
        The values of Vx and Vy are compared, and if they are not equal, the program counter is increased by 2.
        """
        self._logger.info('opcode: SNE_VX_VY')
        self._logger.debug(args)
        vx = args[0]
        vy = args[1]
        if self._registers[vx] != self._registers[vy]:
            self._skip_instruction()
        else:
            self._next_instruction()

    def _ld_i_addr(self, args):
        """
        Annn
        Set I = nnn
        The value of register I is set to nnn.
        """
        self._logger.info('opcode: LD_I_ADDR')
        self._logger.debug(args)
        i = args[1]
        self._i = i
        self._next_instruction()

    def _jp_v0_addr(self, args):
        """
        Bnnn
        Jump to location nnn + V0
        The program counter is set to nnn plus the value of V0.
        """
        self._logger.info('opcode: JP_V0_ADDR')
        self._logger.debug(args)
        addr = args[1]
        self._pc = self._registers[0] + addr

    def _rnd_vx_nn(self, args):
        """
        Cxnn
        Set Vx = random byte AND nn
        The interpreter generates a random number from 0 to 255, which is then ANDed with the value nn. The results are stored in Vx.
        """
        self._logger.info('opcode: RND_VX_NN')
        self._logger.debug(args)
        vx = args[0]
        nn = args[1]
        self._registers[vx] = nn & randint(0, 255)
        self._next_instruction()

    def _drw_vx_vy_n(self, args):
        """
        Dxyn
        Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision
        The interpreter reads n bytes from memory, starting at the address stored in I. These bytes are then displayed as sprites on screen at coordinates (Vx, Vy). Sprites are XORed onto the existing screen. If this causes any pixels to be erased, VF is set to 1, otherwise it is set to 0. If the sprite is positioned so part of it is outside the coordinates of the display, it wraps around to the opposite side of the screen.
        """
        self._logger.info('opcode: DRW_VX_VY_N')
        self._logger.debug(args)
        vx = args[0]
        vy = args[1]
        n = args[2]
        if self._i > (4095 - n):
            raise Exception('Memory out of bounds.')

        self._registers[0xf] = 0

        for i in range(0, n):
            byte = self._memory[self._i + i]
            for position in range(0, 8):
                value = 1 if (byte & (1 << (7 - position))) else 0
                x = (self._registers[vx] + position) % DISPLAY_WIDTH
                y = (self._registers[vy] + i) % DISPLAY_HEIGHT

                if self._display.draw_pixel(x, y, value):
                    self._registers[0xf] = 1

        self._next_instruction()

    def _skp_vx(self, args):
        """
        Ex9E
        Skip next instruction if key with the value of Vx is pressed
        Checks the keyboard, and if the key corresponding to the value of Vx is currently in the down position, PC is increased by 2.
        """
        self._logger.info('opcode: SKP_VX')
        self._logger.debug(args)
        vx = args[0]
        key = self._display.get_key_down()
        if key == str(vx):
            self._skip_instruction()
        else:
            self._next_instruction()


    def _sknp_vx(self, args):
        """
        ExA1
        Skip next instruction if key with the value of Vx is not pressed
        Checks the keyboard, and if the key corresponding to the value of Vx is currently in the up position, PC is increased by 2.
        """
        self._logger.info('opcode: SKNP_VX')
        self._logger.debug(args)
        vx = args[0]
        key = self._display.get_key_down()
        if key != str(vx):
            self._skip_instruction()
        else:
            self._next_instruction()

    def _ld_vx_dt(self, args):
        """
        Fx07
        Set Vx = delay timer value
        The value of DT is placed into Vx.
        """
        self._logger.info('opcode: LD_VX_DT')
        self._logger.debug(args)
        vx = args[0]
        self._registers[vx] = self._dt
        self._next_instruction()

    def _ld_vx_n(self, args):
        """
        Fx0A
        Wait for a key press, store the value of the key in Vx
        All execution stops until a key is pressed, then the value of that key is stored in Vx.
        """
        self._logger.info('opcode: LD_VX_N')
        self._logger.debug(args)
        vx = args[0]
        key = None
        while not key:
            key = self._display.get_key_down()
        self._registers[vx] = key
        self._next_instruction()

    def _ld_dt_vx(self, args):
        """
        Fx15
        Set delay timer = Vx
        DT is set equal to the value of Vx.
        """
        self._logger.info('opcode: LD_DT_VX')
        self._logger.debug(args)
        vx = args[1]
        self._dt = self._registers[vx]
        self._next_instruction()

    def _ld_st_vx(self, args):
        """
        Fx18
        Set sound timer = Vx
        ST is set equal to the value of Vx.
        """
        self._logger.info('opcode: LD_ST_VX')
        self._logger.debug(args)
        vx = args[1]
        self._st = self._registers[vx]
        self._next_instruction()

    def _add_i_vx(self, args):
        """
        Fx1E
        Set I = I + Vx
        The values of I and Vx are added, and the results are stored in I.
        """
        self._logger.info('opcode: ADD_I_VX')
        self._logger.debug(args)
        vx = args[1]
        self._i += self._registers[vx]
        self._next_instruction()

    def _ld_f_vx(self, args):
        """
        Fx29
        Set I = location of sprite for digit Vx
        The value of I is set to the location for the hexadecimal sprite corresponding to the value of Vx.
        """
        self._logger.info('opcode: LD_F_VX')
        self._logger.debug(args)
        vx = args[1]
        if self._registers[vx] > 0xf:
            raise Exception(f"Invalid Digit {self._registers[vx]}")
        self._i = self._registers[vx * 5]
        self._next_instruction()

    def _ld_b_vx(self, args):
        """
        Fx33
        Store BCD representation of Vx in memory locations I, I+1, and I+2.
        """
        self._logger.info('opcode: LD_B_VX')
        self._logger.debug(args)
        vx = args[1]
        lst = list(map(int, str(vx)))
        while len(lst) < 3:
            lst.insert(0, 0)
        self._memory[self._i] = lst[0]
        self._memory[self._i + 1] = lst[1]
        self._memory[self._i + 2] = lst[2]
        self._next_instruction()

    def _ld_i_vx(self, args):
        """
        Fx55
        Store registers V0 through Vx in memory starting at location I
        The interpreter copies the values of registers V0 through Vx into memory, starting at the address in I.
        """
        self._logger.info('opcode: LD_I_VX')
        self._logger.debug(args)
        vx = args[1]
        if self._i > (4095 - vx):
            raise Exception("Memory out of bounds")
        for i in range(vx):
            self._memory[self._i + i] = self._registers[i]
        self._next_instruction()

    def _ld_vx_i(self, args):
        """
        Fx65
        Read registers V0 through Vx from memory starting at location I
        The interpreter reads values from memory starting at location I into registers V0 through Vx.
        """
        self._logger.info('opcode: LD_VX_I')
        self._logger.debug(args)
        vx = args[0]
        if self._i > (4095 - vx):
            raise Exception("Memory out of bounds")
        for i in range(vx):
            self._registers[i] = self._memory[self._i + i]

        self._next_instruction()

    def _dw(self, args):
        raise Exception("Illegal Instruction")

    def _log_state(self):
        self._logger.debug(f'=====\n{self._i=}\n{self._registers=}\n=====')


if __name__ == '__main__':
    chipper = CPU()
