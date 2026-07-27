import ast
import random
import os

BANNED_TOKENS = {"os", "subprocess", "eval", "exec", "open", "system", "shutil"}

ROASTS = [
    "Nice try, Dr. Hackerman. Submission denied.",
    "My grandmother writes cleaner code, and she's a ceramic cat.",
    "Syntax violation detected. Please go sit in the corner and think about your life.",
    "This code looks like it was written by a caffeinated squirrel on a broken keyboard.",
    "Security breach blocked. I have logged your IP address and told your mother."
]

def map_and_roast_tree(node, depth=0, result_lines=None):
    # Dynamically find the name of the AST node class
    node_type = type(node).__name__
    
    # Extract identifier names or values natively from the AST node
    node_text = ""
    if isinstance(node, ast.Name):
        node_text = node.id
    elif isinstance(node, ast.Constant):
        node_text = str(node.value)
    elif isinstance(node, ast.alias):
        node_text = node.name
    elif isinstance(node, ast.Attribute):
        node_text = node.attr
    elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        node_text = node.name

    indent = " " * depth
    suffix = f" -> {node_text[:40]}" if node_text else ""
    line = f"{indent}┠─┨ [{node_type}]{suffix}"
    
    if result_lines is None:
        print(line)
    else:
        result_lines.append(line)
        
    # Check if the text matches any security restrictions
    if node_text in BANNED_TOKENS:
        raise PermissionError(f"CRITICAL: Banned entity '{node_text}' detected!")
        
    # Walk down through every structural child element inside the node
    for child in ast.iter_child_nodes(node):
        map_and_roast_tree(child, depth + 1, result_lines)

def scan_code(raw_user_code):
    # Strict Syntax Check via native AST compiler
    try:
        syntax_tree = ast.parse(raw_user_code)
    except (SyntaxError, ValueError) as syntax_err:
        return {
            "ok": False,
            "status": "rejected",
            "summary": "Invalid Python Syntax Detected.",
            "details": [f"This does not appear to be valid executable code: {syntax_err}"],
        }

    result_lines = []
    try:
        map_and_roast_tree(syntax_tree, result_lines=result_lines)
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
                if file == os.path.basename(__file__):
                    continue
                full_path = os.path.join(root_dir, file)
                py_files_found += 1
                scan_single_file(full_path)
    if py_files_found == 0:
        print("ℹ️ No Python (.py) files were found in this directory.")

if __name__ == "__main__":
    print("S.A.S.S.I. Engine Online. Press Ctrl+C to exit.")
    while True:
        try:
            target_path = input("\nEnter a file path or folder path to scan: ").strip()
            target_path = target_path.strip("'\"")
            if not target_path:
                continue
            if not os.path.exists(target_path):
                print(f"❌ Error: Path '{target_path}' does not exist. Please check your spelling.")
                continue
            if os.path.isdir(target_path):
                scan_directory_recursively(target_path)
            else:
                scan_single_file(target_path)
        except KeyboardInterrupt:
            print("\nShutting down S.A.S.S.I. Engine.")
            break
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
