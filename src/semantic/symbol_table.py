 
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from src.common.errors import SemanticError


class ObjectKind(str, Enum):
    CONSTANT = "constant"
    VARIABLE = "variable"
    TYPE = "type"
    PROCEDURE = "procedure"
    FUNCTION = "function"
    RESERVED = "reserved"  # internal use


class TypeKind(str, Enum):
    NOTYP = "notyp"
    INTS = "ints"
    REALS = "reals"
    BOOLS = "bools"
    CHARS = "chars"
    ARRAYS = "arrays"
    RECORDS = "records"
    STRINGS = "strings"


# ============= TAB (identifier table) =============
@dataclass
class TabEntry:
    ident: str
    link: int
    obj: ObjectKind
    typ: TypeKind
    ref: int
    nrm: bool
    lev: int
    adr: int


# ============= BTAB (block table) =============
@dataclass
class BTabEntry:
    last: int = 0  # last identifier in this block
    lpar: int = 0  # last parameter index (future use)
    psze: int = 0  # size of parameters
    vsze: int = 0  # size of local variables


# ============= ATAB (array type table) =============
@dataclass
class ATabEntry:
    xtyp: TypeKind
    etyp: TypeKind
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
        self.display: List[int] = []  # static chain: display[level] -> btab index
        self.level: int = 0

        self._init_standard_identifiers()

    # ============= Initialization (Sentinel + Standard Identifiers) =============
    def _init_standard_identifiers(self):
        # Global block index 0
        self.btab.append(BTabEntry())
        self.display.append(0)
        self.level = 0

        # Sentinel at index 0
        self.tab.append(
            TabEntry(
                ident="", link=0, obj=ObjectKind.VARIABLE, typ=TypeKind.NOTYP, ref=0,
                nrm=True, lev=0, adr=0
            )
        )

        # Standard constants
        self._enter_standard("false", ObjectKind.CONSTANT, TypeKind.BOOLS, 0)
        self._enter_standard("true", ObjectKind.CONSTANT, TypeKind.BOOLS, 1)

        # Standard types
        self._enter_standard("real", ObjectKind.TYPE, TypeKind.REALS, 1)
        self._enter_standard("char", ObjectKind.TYPE, TypeKind.CHARS, 1)
        self._enter_standard("boolean", ObjectKind.TYPE, TypeKind.BOOLS, 1)
        self._enter_standard("integer", ObjectKind.TYPE, TypeKind.INTS, 1)

        # Standard functions
        std_funcs = [
            ("abs", TypeKind.REALS, 0),
            ("sqr", TypeKind.REALS, 2),
            ("odd", TypeKind.BOOLS, 4),
            ("chr", TypeKind.CHARS, 5),
            ("ord", TypeKind.INTS, 6),
            ("succ", TypeKind.CHARS, 7),
            ("pred", TypeKind.CHARS, 8),
            ("round", TypeKind.INTS, 9),
            ("trunc", TypeKind.INTS, 10),
            ("sin", TypeKind.REALS, 11),
            ("cos", TypeKind.REALS, 12),
            ("exp", TypeKind.REALS, 13),
            ("ln", TypeKind.REALS, 14),
            ("sqrt", TypeKind.REALS, 15),
            ("arctan", TypeKind.REALS, 16),
            ("eof", TypeKind.BOOLS, 17),
            ("eoln", TypeKind.BOOLS, 18),
        ]
        for name, typ, adr in std_funcs:
            self._enter_standard(name, ObjectKind.FUNCTION, typ, adr)

        # Standard procedures
        std_procs = [
            ("read", 1),
            ("readln", 2),
            ("write", 3),
            ("writeln", 4),
            ("", 0),  # blank procedure as per original listing
        ]
        for name, adr in std_procs:
            self._enter_standard(name, ObjectKind.PROCEDURE, TypeKind.NOTYP, adr)

    def _enter_standard(self, name: str, obj: ObjectKind, typ: TypeKind, adr: int):
        idx = len(self.tab)
        # Link to previous entry 
        link = idx - 1
        self.tab.append(
            TabEntry(
                ident=name,
                link=link,
                obj=obj,
                typ=typ,
                ref=0,
                nrm=True,
                lev=0,
                adr=adr,
            )
        )
        # Update global block last pointer
        self.btab[0].last = idx

    # ============= Scope Management =============
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

    # ============= User Identifier Insertion (enter) =============
    def enter(self, ident: str, kind: ObjectKind) -> int:
        """Insert a user-defined identifier following Pascal-S duplicate rules.

        Raises SemanticError if identifier already defined in current scope.
        The newly inserted entry has typ=NOTYP, adr=0, ref=0 initially.
        """
        block_idx = self.display[self.level]
        last = self.btab[block_idx].last

        # Duplicate check: traverse current scope chain
        j = last
        while j != 0:
            if self.tab[j].ident == ident:
                raise SemanticError(f"Identifier '{ident}' already defined in this scope")
            j = self.tab[j].link

        idx = len(self.tab)
        self.tab.append(
            TabEntry(
                ident=ident,
                link=last,
                obj=kind,
                typ=TypeKind.NOTYP,
                ref=0,
                nrm=True,
                lev=self.level,
                adr=0,
            )
        )
        self.btab[block_idx].last = idx
        return idx

     # ============= INSERT IDENTIFIER =============
    def insert(self, ident: str, obj: str, type_code: int, ref=0, nrm=1, adr=0):
        """Legacy insertion used earlier; now delegates to enter and then patches fields.
        type_code is ignored for now (will be assigned later)."""
        kind = ObjectKind(obj) if obj in ObjectKind._value2member_map_ else ObjectKind.VARIABLE
        idx = self.enter(ident, kind)
        # Optionally patch adr/ref if provided
        entry = self.tab[idx]
        entry.adr = adr
        entry.ref = ref
        entry.nrm = bool(nrm)
        return idx

    # ============= Lookup (loc) =============
    def loc(self, ident: str) -> int:
        """Locate identifier index across static levels; raise error if undefined."""
        lvl = self.level
        while lvl >= 0:
            block_idx = self.display[lvl]
            ptr = self.btab[block_idx].last
            while ptr != 0:
                if self.tab[ptr].ident == ident:
                    return ptr
                ptr = self.tab[ptr].link
            lvl -= 1
        raise SemanticError(f"Undefined identifier '{ident}'")

    def lookup(self, ident: str) -> Optional[int]:  # interface
        try:
            return self.loc(ident)
        except SemanticError:
            return None
