import  ctypes
import random
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

# The modern, clean way to load the Python language bindings
PY_LANG = Language(tspython.language())
parser = Parser(language=PY_LANG)

BANNED_TOKENS = {"os", "subprocess", "eval", "exec", "open", "system", "shutil"}
ROASTS = [
    "Nice try, Dr. Hackerman. Submission denied.",
    "My grandmother writes cleaner code, and she's a ceramic cat.",
    "Syntax violation detected. Please go sit in the corner and think about your life.",
    "This code looks like it was written by an caffeinated squirrel on a broken keyboard.",
    "Security breach blocked. I have logged your IP address and told your mother."
]

def map_and_roast_tree(node, source_bytes, depth=0, result_lines=None):
    node_text = source_bytes[node.start_byte:node.end_byte].decode("utf8").strip()
    indent = " " * depth
    line = f"{indent}┠─┨ [{node.type}] -> {node_text[:40]}"
    
    if result_lines is None:
        print(line)
    else:
        result_lines.append(line)
        
    if node.type in ("identifier", "string") and node_text in BANNED_TOKENS:
        raise PermissionError(
            f"CRITICAL: Banned entity '{node_text}' detected at line {node.start_point[0] + 1}!"
        )
        
    for child in node.children:
        map_and_roast_tree(child, source_bytes, depth + 1, result_lines)

def scan_code(raw_user_code):
    source_bytes = raw_user_code.encode("utf8")
    syntax_tree = parser.parse(source_bytes)
    root = syntax_tree.root_node
    result_lines = []
    
    if root.has_error:
        return {
            "ok": False,
            "status": "rejected",
            "summary": "Code structure is corrupted.",
            "details": ["Syntax errors were detected in the submitted code."],
        }
        
    try:
        map_and_roast_tree(root, source_bytes, result_lines=result_lines)
        return {
            "ok": True,
            "status": "passed",
            "summary": "Code logic cleared.",
            "details": result_lines,
        }
    except PermissionError as secure_error:
        return {
            "ok": False,
            "status": "security_block",
            "summary": "Security block detected.",
            "details": [str(secure_error), random.choice(ROASTS)],
        }

def sassi_gatekeeper(raw_user_code):
    result = scan_code(raw_user_code)
    print("\n" + "═" * 70)
    print("S.A.S.S.I. INITIALIZING SCAN PROTOCOL...")
    print("═" * 70)
    
    if result["ok"]:
        print("\nGENOME STRUCTURAL COMPILATION MAP:")
        for line in result["details"]:
            print(line)
        print("\n[PASSED] Code logic cleared. Clean, secure, and profoundly boring. Proceed.")
        return True
        
    if result["status"] == "rejected":
        print(f"\n[REJECTED] {result['summary']}")
        print(result["details"][0])
    else:
        print(f"\n[SECURITY BLOCK] {result['summary']}")
        print(result["details"][0])
        print(result["details"][1])
    return False
