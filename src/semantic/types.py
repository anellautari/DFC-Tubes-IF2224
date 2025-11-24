
TYPE_UNKNOWN = 0
TYPE_INTEGER = 1
TYPE_REAL = 2
TYPE_CHAR = 3
TYPE_STRING = 4
TYPE_BOOLEAN = 5
TYPE_ARRAY = 6
TYPE_CUSTOM = 7
TYPE_VOID = 8  # Untuk procedure (no return value)
TYPE_ERROR = 9

TYPE_NAMES = {
    0: "unknown",
    1: "integer",
    2: "real",
    3: "char",
    4: "string",
    5: "boolean",
    6: "array",
    7: "custom",
    8: "void",
    9: "error"
}


# ==================== HELPER FUNCTIONS ====================
def get_type_name(type_code: int) -> str:
    """Get human-readable type name dari type code"""
    return TYPE_NAMES.get(type_code, "unknown")

def get_type_code(type_name: str) -> int:
    """Get type code dari human-readable type name"""
    for code, name in TYPE_NAMES.items():
        if name == type_name:
            return code
    return TYPE_UNKNOWN


def types_compatible(type1: int, type2: int) -> bool:
    """Check apakah dua tipe compatible untuk assignment/comparison"""
    if type1 == type2:
        return True
    
    if type1 == TYPE_INTEGER and type2 == TYPE_REAL:
        return True
    
    if type1 == TYPE_REAL and type2 == TYPE_INTEGER:
        return True
    
    return False


def result_type(op: str, left_type: int, right_type: int) -> int:
    """Determine result type dari binary operation"""
    
    if op in ('+', '-', '*', '/'):
        if left_type == TYPE_REAL or right_type == TYPE_REAL:
            return TYPE_REAL
        if op == '/':
            return TYPE_REAL
        if left_type == TYPE_INTEGER and right_type == TYPE_INTEGER:
            return TYPE_INTEGER
        return TYPE_UNKNOWN
    
    if op in ('bagi', 'mod'):
        if left_type == TYPE_INTEGER and right_type == TYPE_INTEGER:
            return TYPE_INTEGER
        return TYPE_UNKNOWN
    
    if op in ('=', '<>', '<', '<=', '>', '>='):
        return TYPE_BOOLEAN
    
    if op in ('dan', 'atau'):
        if left_type == TYPE_BOOLEAN and right_type == TYPE_BOOLEAN:
            return TYPE_BOOLEAN
        return TYPE_UNKNOWN
    
    return TYPE_UNKNOWN