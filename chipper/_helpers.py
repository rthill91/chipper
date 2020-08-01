from dataclasses import dataclass, field
from typing import List


@dataclass
class argument:
    mask: int
    shift: int


@dataclass
class opcode:
    id: str
    name: str
    pattern: int
    mask: int
    arguments: List[argument] = field(default_factory=lambda: [])
