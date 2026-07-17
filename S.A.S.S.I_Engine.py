import random
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

# Initialize the Lexical Parser using the updated tree-sitter 2026 API syntax
PY_LANG = Language(tspython.language())
parser = Parser(PY_LANG)


# The Ban Matrix (Your Database)
BANNED_TOKENS = {"os", "subprocess", "eval", "exec", "open", "system", "shutil"}

# Snarky rejection messages for bad code
ROASTS = [
    "Nice try, Dr. Hackerman. Submission denied.",
    "My grandmother writes cleaner code, and she's a ceramic cat.",
    "Syntax violation detected. Please go sit in the corner and think about your life.",
    "This code looks like it was written by an caffeinated squirrel on a broken keyboard.",
    "Security breach blocked. I have logged your IP address and told your mother."
]

def map_and_roast_tree(node, source_bytes, depth=0):
    """Recursively crawls code blocks and builds a visually complex syntax chart."""
    node_text = source_bytes[node.start_byte:node.end_byte].decode("utf8").strip()
    
    # Visual Polish: Generates a sci-fi nested bracket map in the terminal
    indent = "    " * depth
    print(f"{indent}┠─┨ \033[96m[{node.type}]\033[0m -> \033[90m{node_text[:40]}\033[0m")
    
    # Catch illegal system injection points
    if node.type in ("identifier", "string") and node_text in BANNED_TOKENS:
        raise PermissionError(f"CRITICAL: Banned entity '{node_text}' detected at line {node.start_point[0] + 1}!")
        
    for child in node.children:
        map_and_roast_tree(child, source_bytes, depth + 1)

def sassi_gatekeeper(raw_user_code):
    """Main interrogation pipeline."""
    print("\n" + "═"*70)
    print("S.A.S.S.I. INITIALIZING SCAN PROTOCOL...")
    print("═"*70)
    
    source_bytes = bytes(raw_user_code, "utf8")
    syntax_tree = parser.parse(source_bytes)
    root = syntax_tree.root_node
    
    # Stop physically broken code execution
    if root.has_error:
        print(f"\n\033[91m[REJECTED]\033[0m Code structure is fundamentally corrupted. {random.choice(ROASTS)}")
        return False
        
    print("\nGENOME STRUCTURAL COMPILATION MAP:")
    try:
        map_and_roast_tree(root, source_bytes)
        print(f"\n\033[92m[PASSED]\033[0m Code logic cleared. Clean, secure, and profoundly boring. Proceed.")
        return True
    except PermissionError as secure_error:
        print(f"\n\033[91m[SECURITY BLOCK] {secure_error}\033[0m")
        print(f"\033[93mS.A.S.S.I. Says:\033[0m \"{random.choice(ROASTS)}\"")
        return False


# --- RUNTIME TESTING SUITE ---
if __name__ == "__main__":
    # Test Case 1: Perfectly clean code that should pass
    clean_code = """
def calculate_total(price, tax):
    return price * (1 + tax)
"""

    # Test Case 2: Broken code missing a colon that triggers a syntax error
    broken_code = """
def bad_function(x)
    return x + 5
"""

    # Test Case 3: Malicious code trying to inject a banned command
    malicious_code = """
import os
def hack_system():
    os.system("rm -rf /")
"""

    # Run the tests through the engine gatekeeper
    sassi_gatekeeper(clean_code)
    sassi_gatekeeper(broken_code)
    sassi_gatekeeper(malicious_code)
