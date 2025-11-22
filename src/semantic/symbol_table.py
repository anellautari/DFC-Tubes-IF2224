from dataclasses import dataclass, field
from typing import List, Optional


# ============= TAB (identifier table) =============
@dataclass
class TabEntry:
    ident: str
    obj: str              # 'constant', 'variable', 'type', 'procedure', 'function'
    type: int             # type code (integer, boolean, array, ...)
    ref: int              # reference to atab / btab
    nrm: int              # 1 = normal, 0 = by-reference
    lev: int              # lexical level
    adr: int              # address offset or constant value
    link: int             # linked list pointer in same block


# ============= BTAB (block table) =============
@dataclass
class BTabEntry:
    last: int = 0  # last identifier inserted in this block
    lpar: int = 0  # last parameter index
    psze: int = 0  # total size of parameters
    vsze: int = 0  # total size of local variables


# ============= ATAB (array type table) =============
@dataclass
class ATabEntry:
    xtyp: int
    etyp: int
    eref: int
    low: int
    high: int
    elsz: int
    size: int


class SymbolTables:
    def __init__(self):
        self.tab: List[TabEntry] = []
        self.btab: List[BTabEntry] = []
        self.atab: List[ATabEntry] = []
        self.display: List[int] = []   # display[level] = index to btab
        self.level: int = 0

        self._init_reserved()

    def _init_reserved(self):
        # reserve indices 0..28 for keywords and predefined
        for i in range(29):
            self.tab.append(
                TabEntry(
                    ident=f"<reserved-{i}>",
                    obj="reserved",
                    type=0,
                    ref=0,
                    nrm=1,
                    lev=0,
                    adr=0,
                    link=0,
                )
            )

        # global block
        self.btab.append(BTabEntry())  # index = 0
        self.display.append(0)
        self.level = 0

    # ============= SCOPE MANAGEMENT =============
    def begin_block(self) -> int:
        self.level += 1
        block_index = len(self.btab)
        self.btab.append(BTabEntry())

        if len(self.display) <= self.level:
            self.display.append(block_index)
        else:
            self.display[self.level] = block_index

        return block_index

    def end_block(self):
        self.display[self.level] = 0
        self.level -= 1

    # ============= INSERT IDENTIFIER =============
    def insert(self, ident: str, obj: str, type_code: int, ref=0, nrm=1, adr=0):
        block_idx = self.display[self.level]
        block = self.btab[block_idx]

        previous = block.last

        index = len(self.tab)
        entry = TabEntry(
            ident=ident,
            obj=obj,
            type=type_code,
            ref=ref,
            nrm=nrm,
            lev=self.level,
            adr=adr,
            link=previous,
        )
        self.tab.append(entry)

        block.last = index

        if obj == "variable":
            block.vsze += 1
        elif obj == "parameter":
            block.psze += 1

        return index

    # ============= LOOKUP IDENTIFIER =============
    def lookup(self, ident: str) -> Optional[int]:
        for lvl in range(self.level, -1, -1):
            block_idx = self.display[lvl]
            ptr = self.btab[block_idx].last

            while True:
                if ptr == 0:
                    break
                entry = self.tab[ptr]
                if entry.ident == ident:
                    return ptr
                ptr = entry.link

        return None
