from dataclasses import dataclass, field
from enum import Enum
from typing import List


def hello():
    print("hi")


@dataclass
class _argument:
    mask: int
    shift: int


@dataclass
class _opcode:
    name: str
    pattern: int
    mask: int
    arguments: List[_argument] = field(default_factory=lambda: [])


class Opcode(Enum):
    CLS         = _opcode('CLS',  0x00e0, 0xffff)
    RET         = _opcode('RET',  0x00ee, 0xffff)
    JP_ADDR     = _opcode('JP',   0x1000, 0xf000)
    CALL_ADDR   = _opcode('CALL', 0x2000, 0xf000)
    SE_VX_NN    = _opcode('SE',   0x3000, 0xf000)
    SNE_VX_NN   = _opcode('SNE',  0x4000, 0xf000)
    SE_VX_VY    = _opcode('SE',   0x5000, 0xf00f)
    LD_VX_NN    = _opcode('LD',   0x6000, 0xf000)
    ADD_VX_NN   = _opcode('ADD',  0x7000, 0xf000)
    LD_VX_VY    = _opcode('LD',   0x8000, 0xf00f)
    OR_VX_VY    = _opcode('OR',   0x8001, 0xf00f)
    AND_VX_VY   = _opcode('AND',  0x8002, 0xf00f)
    XOR_VX_VY   = _opcode('XOR',  0x8003, 0xf00f)
    ADD_VX_VY   = _opcode('ADD',  0x8004, 0xf00f)
    SUB_VX_VY   = _opcode('SUB',  0x8005, 0xf00f)
    SHR_VX_VY   = _opcode('SHR',  0x8006, 0xf00f)
    SUBN_VX_VY  = _opcode('SUBN', 0x8007, 0xf00f)
    SHL_VX_VY   = _opcode('SHL',  0x800e, 0xf00f)
    SNE_VX_VY   = _opcode('SNE',  0x9000, 0xf00f)
    LD_I_ADDR   = _opcode('LD',   0xa000, 0xf000)
    JP_V0_ADDR  = _opcode('JP',   0xb000, 0xf000)
    RND_VX_NN   = _opcode('RND',  0xc000, 0xf000)
    DRW_VX_VY_N = _opcode('DRW',  0xd000, 0xf000)
    SKP_VX      = _opcode('SKP',  0xe09e, 0xf0ff)
    SKNP_VX     = _opcode('SKNP', 0xe0a1, 0xf0ff)
    LD_VX_DT    = _opcode('LD',   0xf007, 0xf0ff)
    LD_VX_N     = _opcode('LD',   0xf00a, 0xf0ff)
    LD_DT_VX    = _opcode('LD',   0xf015, 0xf0ff)
    LD_ST_VX    = _opcode('LD',   0xf018, 0xf0ff)
    ADD_I_VX    = _opcode('ADD',  0xf01e, 0xf0ff)
    LD_F_VX     = _opcode('LD',   0xf029, 0xf0ff)
    LD_B_VX     = _opcode('LD',   0xf033, 0xf0ff)
    LD_I_VX     = _opcode('LD',   0xf055, 0xf0ff)
    LD_VX_I     = _opcode('LD',   0xf065, 0xf0ff)
