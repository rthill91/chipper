class CPU:
    def __init__(self):
        self.memory = []
        self.program_counter = 0x200
        self.registers = []
        self.index_register = 0
        self.stack = []
        self.stack_pointer = -1
        self.sound_timer = 0
        self.delay_timer = 0
