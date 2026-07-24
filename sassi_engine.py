import ctypes
import random
import os
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
    "This code looks like it was written by a caffeinated squirrel on a broken keyboard.",
    "Security breach blocked. I have logged your IP address and told your mother."
]

def map_and_roast_tree(node, source_bytes, depth=0, result_lines=None):
    node_text = source_bytes[node.start_byte:node.end_byte].decode("utf8").strip()
    indent = "  " * depth
    line = f"{indent}┠─┨ [{node.type}] -> {node_text[:40]}"
    
    if result_lines is None:
        print(line)
    else:
        result_lines.append(line)

    if node.type in ("identifier", "string") and node_text in BANNED_TOKENS:
        raise PermissionError(
            f"CRITICAL: Banned entity '{node_text}' detected!"
        )

    for child in node.children:
        map_and_roast_tree(child, source_bytes, depth + 1, result_lines)

def scan_code(raw_user_code):
    # Strict Syntax Check: Ensure it is actual, valid Python code and not random text
    try:
        compile(raw_user_code, "<string>", "exec")
    except (SyntaxError, ValueError) as syntax_err:
        return {
            "ok": False,
            "status": "rejected",
            "summary": "Invalid Python Syntax Detected.",
            "details": [f"This does not appear to be valid executable code: {syntax_err}"],
        }

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

def sassi_gatekeeper(raw_user_code, source_name="File"):
    result = scan_code(raw_user_code)
    print("\n" + "═" * 70)
    print(f"S.A.S.S.I. SCAN PROTOCOL: {source_name}")
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

def scan_single_file(file_path):
    """Reads and targets a singular Python source file."""
    try:
        with open(file_path, "r", encoding="utf-8") as target_file:
            file_content = target_file.read()
        sassi_gatekeeper(file_content, source_name=os.path.basename(file_path))
    except Exception as e:
        print(f"❌ Could not read file '{file_path}': {e}")

def scan_directory_recursively(dir_path):
    """Walks through directories to find and analyze all .py files."""
    print(f"\nScanning directory structure: {dir_path}")
    py_files_found = 0
    
    for root_dir, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".py"):
                # Avoid scanning this engine file if it lives in the target directory
                if file == os.path.basename(__file__):
                    continue
                    
                full_path = os.path.join(root_dir, file)
                py_files_found += 1
                scan_single_file(full_path)
                
    if py_files_found == 0:
        print("ℹ️ No Python (.py) files were found in this directory.")

# Execution block to handle running the script in the terminal
if __name__ == "__main__":
    print("S.A.S.S.I. Engine Online. Press Ctrl+C to exit.")
    while True:
        try:
            target_path = input("\nEnter a file path or folder path to scan: ").strip()
            
            # Remove wrapping quotes if the user dragged and dropped the target into the terminal
            target_path = target_path.strip("'\"")
            
            if not target_path:
                continue
                
            if not os.path.exists(target_path):
                print(f"❌ Error: Path '{target_path}' does not exist. Please check your spelling.")
                continue

            # Switch execution paths depending on whether the input target is a folder or file
            if os.path.isdir(target_path):
                scan_directory_recursively(target_path)
            else:
                scan_single_file(target_path)
            
        except KeyboardInterrupt:
            print("\nShutting down S.A.S.S.I. Engine.")
            break
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
