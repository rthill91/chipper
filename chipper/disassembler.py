from .opcode import opcodes


def disassemble(opcode):
    try:
        instruction = next(inst for inst in opcodes if (inst.mask & opcode) == inst.pattern)
    except StopIteration:
        raise StopIteration(f"No opcode found matching {hex(opcode)}")

    args = [((opcode & arg.mask) >> arg.shift) for arg in instruction.arguments]


    return (instruction, args)


def test_runner():
    print(disassemble(0x9130))
