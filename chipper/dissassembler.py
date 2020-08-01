from .opcode import Opcode


def disassemble(opcode):
    try:
        instruction = next(inst for inst in Opcode if (inst.value.mask & opcode) == inst.value.pattern)
    except StopIteration:
        raise StopIteration(f"No opcode found matching {hex(opcode)}")

    print(instruction)


def test_runner():
    disassemble(0xeb0c)
