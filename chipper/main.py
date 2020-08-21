import sys
from time import sleep
from .cpu import CPU


def run():
    argv = sys.argv
    if len(argv) < 2:
        raise Exception("No ROM provided")
    elif len(argv) > 2:
        raise Exception("Unexpected arguments provided")
    file_path = argv[1]
    with open(file_path, 'rb') as f:
        rom = bytearray(f.read())

    cpu = CPU()
    cpu.load(rom)

    timer = 0
    while True:
        timer = cycle(cpu, timer)
        # sleep(0.1)


def cycle(cpu, timer):
    timer += 1
    if timer % 5 == 0:
        cpu.tick()
        timer = 0

    cpu.step()
    return timer
