from ._helpers import argument, opcode

opcodes = [
    opcode('CLS',          'CLS',  0x00e0, 0xffff),
    opcode('RET',          'RET',  0x00ee, 0xffff),
    opcode('JP_ADDR',      'JP',   0x1000, 0xf000, [argument(0x0fff, 0)]),
    opcode('CALL_ADDR',    'CALL', 0x2000, 0xf000, [argument(0x0fff, 0)]),
    opcode('SE_VX_NN',     'SE',   0x3000, 0xf000, [argument(0x0f00, 8), argument(0x00ff, 0)]),
    opcode('SNE_VX_NN',    'SNE',  0x4000, 0xf000, [argument(0x0f00, 8), argument(0x00ff, 0)]),
    opcode('SE_VX_VY',     'SE',   0x5000, 0xf00f, [argument(0x0f00, 8), argument(0x00f0, 4)]),
    opcode('LD_VX_NN',     'LD',   0x6000, 0xf000, [argument(0x0f00, 8), argument(0x00ff, 0)]),
    opcode('ADD_VX_NN',    'ADD',  0x7000, 0xf000, [argument(0x0f00, 8), argument(0x00ff, 0)]),
    opcode('LD_VX_VY',     'LD',   0x8000, 0xf00f, [argument(0x0f00, 8), argument(0x00f0, 4)]),
    opcode('OR_VX_VY',     'OR',   0x8001, 0xf00f, [argument(0x0f00, 8), argument(0x00f0, 4)]),
    opcode('AND_VX_VY',    'AND',  0x8002, 0xf00f, [argument(0x0f00, 8), argument(0x00f0, 4)]),
    opcode('XOR_VX_VY',    'XOR',  0x8003, 0xf00f, [argument(0x0f00, 8), argument(0x00f0, 4)]),
    opcode('ADD_VX_VY',    'ADD',  0x8004, 0xf00f, [argument(0x0f00, 8), argument(0x00f0, 4)]),
    opcode('SUB_VX_VY',    'SUB',  0x8005, 0xf00f, [argument(0x0f00, 8), argument(0x00f0, 4)]),
    opcode('SHR_VX_VY',    'SHR',  0x8006, 0xf00f, [argument(0x0f00, 8), argument(0x00f0, 4)]),
    opcode('SUBN_VX_VY',   'SUBN', 0x8007, 0xf00f, [argument(0x0f00, 8), argument(0x00f0, 4)]),
    opcode('SHL_VX_VY',    'SHL',  0x800e, 0xf00f, [argument(0x0f00, 8), argument(0x00f0, 4)]),
    opcode('SNE_VX_VY',    'SNE',  0x9000, 0xf00f, [argument(0x0f00, 8), argument(0x00f0, 4)]),
    opcode('LD_I_ADDR',    'LD',   0xa000, 0xf000, [argument(0x0000, 0), argument(0x0fff, 0)]),
    opcode('JP_V0_ADDR',   'JP',   0xb000, 0xf000, [argument(0x0000, 0), argument(0x0fff, 0)]),
    opcode('RND_VX_NN',    'RND',  0xc000, 0xf000, [argument(0x0f00, 8), argument(0x00ff, 0)]),
    opcode('DRW_VX_VY_N',  'DRW',  0xd000, 0xf000, [argument(0x0f00, 8), argument(0x00f0, 4), argument(0x000f, 0)]),
    opcode('SKP_VX',       'SKP',  0xe09e, 0xf0ff, [argument(0x0f00, 8)]),
    opcode('SKNP_VX',      'SKNP', 0xe0a1, 0xf0ff, [argument(0x0f00, 8)]),
    opcode('LD_VX_DT',     'LD',   0xf007, 0xf0ff, [argument(0x0f00, 8), argument(0x0000, 0)]),
    opcode('LD_VX_N',      'LD',   0xf00a, 0xf0ff, [argument(0x0f00, 8), argument(0x0000, 0)]),
    opcode('LD_DT_VX',     'LD',   0xf015, 0xf0ff, [argument(0x0000, 0), argument(0x0f00, 8)]),
    opcode('LD_ST_VX',     'LD',   0xf018, 0xf0ff, [argument(0x0000, 0), argument(0x0f00, 8)]),
    opcode('ADD_I_VX',     'ADD',  0xf01e, 0xf0ff, [argument(0x0000, 0), argument(0x0f00, 8)]),
    opcode('LD_F_VX',      'LD',   0xf029, 0xf0ff, [argument(0x0000, 0), argument(0x0f00, 8)]),
    opcode('LD_B_VX',      'LD',   0xf033, 0xf0ff, [argument(0x0000, 0), argument(0x0f00, 8)]),
    opcode('LD_I_VX',      'LD',   0xf055, 0xf0ff, [argument(0x0000, 0), argument(0x0f00, 8)]),
    opcode('LD_VX_I',      'LD',   0xf065, 0xf0ff, [argument(0x0f00, 8), argument(0x0000, 0)]),
    opcode('DW',           'DW',   0x0000, 0x0000, [argument(0xffff, 0)]),
]
