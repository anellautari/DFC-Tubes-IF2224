import os
import json
import sys
from src.semantic.ast import ASTNode
from src.semantic.symbol_table import SymbolTables

def load_dfa_rules(filepath: str | None = None) -> dict:
    if filepath is None:
        current_dir = os.path.dirname(__file__) 
        project_root = os.path.dirname(current_dir)
        filepath = os.path.join(project_root, "lexer", "dfa_rules.json")

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' tidak ditemukan.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: File '{filepath}' bukan file JSON valid: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca file DFA '{filepath}': {e}")
        sys.exit(1)

def read_source_code(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File source code '{path}' tidak ditemukan.")
        sys.exit(1)
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca file source code '{path}': {e}")
        sys.exit(1)

def print_symbol_tables(symtab: SymbolTables):
    def clean_enum(v):
        if hasattr(v, "name"):
            return v.name
        return str(v)
    
    print("\nTAB (identifier table):")
    header = (
        f"{'idx':<3} | {'id':<12} | {'obj':<10} | {'typ':<10} | "
        f"{'ref':<3} | {'nrm':<3} | {'lev':<3} | {'adr':<6} | {'link':<4}"
    )
    print(header)
    print("-" * len(header))

    for i, e in enumerate(symtab.tab):
        ident = e.ident if e.ident else ""
        obj = clean_enum(e.obj)
        typ = clean_enum(e.typ)
        ref = e.ref
        nrm = int(e.nrm)
        lev = e.lev
        adr = e.adr if e.adr is not None else ""
        link = e.link if e.link is not None else ""

        print(
            f"{i:<3} | "
            f"{ident:<12} | "
            f"{obj:<10} | "
            f"{typ:<10} | "
            f"{ref:<3} | "
            f"{nrm:<3} | "
            f"{lev:<3} | "
            f"{str(adr):<6} | "
            f"{str(link):<4}"
        )

    print("\nBTAB (block table):")
    header = f"{'idx':<3} | {'last':<4} | {'lpar':<4} | {'psze':<4} | {'vsze':<4}"
    print(header)
    print("-" * len(header))

    for i, e in enumerate(symtab.btab):
        print(
            f"{i:<3} | {e.last:<4} | {e.lpar:<4} | {e.psze:<4} | {e.vsze:<4}"
        )

    print("\nATAB (array table):")
    header = f"{'idx':<3} | {'xtyp':<6} | {'etyp':<6} | {'eref':<4} | {'low':<4} | {'high':<4} | {'elsz':<4} | {'size':<4}"
    print(header)
    print("-" * len(header))

    for i, e in enumerate(symtab.atab):
        print(
            f"{i:<3} | {clean_enum(e.xtyp):<6} | {clean_enum(e.etyp):<6} | "
            f"{e.eref:<4} | {e.low:<4} | {e.high:<4} | {e.elsz:<4} | {e.size:<4}"
        )

def print_ast_tree(node, prefix="", is_last=True):
    """Pretty-print AST tree using unicode branches."""
    if node is None:
        return

    connector = "└── " if is_last else "├── "
    node_name = node.__class__.__name__

    # Extra annotations if available
    extras = []
    if getattr(node, "name", None):
        extras.append(f"name={node.name}")
    if getattr(node, "type", None):
        extras.append(f"type={node.type}")
    if getattr(node, "symbol", None):
        extras.append(f"symbol={node.symbol}")
    if getattr(node, "scope_level", None):
        extras.append(f"lev={node.scope_level}")

    extra_str = (" [" + ", ".join(extras) + "]") if extras else ""

    print(prefix + connector + node_name + extra_str)

    # Prepare prefix padding
    child_prefix = prefix + ("    " if is_last else "│   ")

    # Iterate through fields that contain AST children
    children = []
    for field_name, value in node.__dict__.items():
        # Skip primitive fields
        if field_name in ("token", "name", "type", "symbol", "scope_level", "value", "evaluated_value"):
            continue

        # Single child
        if isinstance(value, ASTNode):
            children.append(value)

        # List of children
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ASTNode):
                    children.append(item)

    # Print children
    for i, child in enumerate(children):
        print_ast_tree(child, child_prefix, i == len(children) - 1)
