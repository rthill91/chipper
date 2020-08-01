from chipper.disassembler import disassemble

import pytest


def _idfn(val):
    if isinstance(val, str):
        return val
    return ''


@pytest.mark.parametrize('inst_id,opcode,arg_list', [
    ('CLS',         0x00e0, []),
    ('RET',         0x00ee, []),
    ('JP_ADDR',     0x1333, [0x333]),
    ('CALL_ADDR',   0x2062, [0x062]),
    ('SE_VX_NN',    0x3abb, [0xa,    0xbb]),
    ('SNE_VX_NN',   0x4acc, [0xa,    0xcc]),
    ('SE_VX_VY',    0x5ab0, [0xa,    0xb]),
    ('LD_VX_NN',    0x6abb, [0xa,    0xbb]),
    ('ADD_VX_NN',   0x7abb, [0xa,    0xbb]),
    ('LD_VX_VY',    0x8ab0, [0xa,    0xb]),
    ('OR_VX_VY',    0x8ab1, [0xa,    0xb]),
    ('AND_VX_VY',   0x8ab2, [0xa,    0xb]),
    ('XOR_VX_VY',   0x8ab3, [0xa,    0xb]),
    ('ADD_VX_VY',   0x8ab4, [0xa,    0xb]),
    ('SUB_VX_VY',   0x8ab5, [0xa,    0xb]),
    ('SHR_VX_VY',   0x8ab6, [0xa,    0xb]),
    ('SUBN_VX_VY',  0x8ab7, [0xa,    0xb]),
    ('SHL_VX_VY',   0x8abe, [0xa,    0xb]),
    ('SNE_VX_VY',   0x9ab0, [0xa,    0xb]),
    ('LD_I_ADDR',   0xa999, [0x0,    0x999]),
    ('JP_V0_ADDR',  0xb400, [0x0,    0x400]),
    ('RND_VX_NN',   0xcabb, [0xa,    0xbb]),
    ('DRW_VX_VY_N', 0xdab9, [0xa,    0xb,   0x9]),
    ('SKP_VX',      0xea9e, [0xa]),
    ('SKNP_VX',     0xeba1, [0xb]),
    ('LD_VX_DT',    0xfa07, [0xa,    0x0]),
    ('LD_VX_N',     0xfb0a, [0xb,    0x0]),
    ('LD_DT_VX',    0xfb15, [0x0,    0xb]),
    ('LD_ST_VX',    0xfa18, [0x0,    0xa]),
    ('ADD_I_VX',    0xfa1e, [0x0,    0xa]),
    ('LD_F_VX',     0xfa29, [0x0,    0xa]),
    ('LD_B_VX',     0xfa33, [0x0,    0xa]),
    ('LD_I_VX',     0xfa55, [0x0,    0xa]),
    ('LD_VX_I',     0xfa65, [0xa,    0x0]),
    ('DW',          0x5154, [0x5154]),
], ids=_idfn)
def test_instruction(inst_id, opcode, arg_list):
    inst = disassemble(opcode)
    assert inst[0].id == inst_id
    assert inst[1] == arg_list
