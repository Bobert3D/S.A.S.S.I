import random
import streamlit as st
import tree_sitter_python as tspython
from tree_sitter import Language, Parser


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
    indent = "  " * depth
    line = f"{indent}┠─┨ [{node.type}] -> {node_text[:40]}"
    
    if result_lines is not None:
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
        map_and_roast_tree(root, source_bytes, depth=0, result_lines=result_lines)
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


def build_web_page():
    st.set_page_config(page_title="S.A.S.S.I. Gatekeeper", page_icon="🛡️", layout="centered")
    
    st.title("🛡️ S.A.S.S.I. Secure Gateway")
    st.subheader("Interactive Compilation & Scan Panel")
    st.markdown("Submit your target code block below to run parsing layout verification.")
    

    user_code = st.text_area(
        label="Target Python Code Workspace",
        height=300,
        placeholder="def entry_point():\n    print('Hello World')\n",
        help="Paste or type multi-line code here. Avoid blacklisted modules."
    )
    
    if st.button("Initialize Scan Protocol", type="primary"):
        if not user_code.strip():
            st.warning("⚠️ Execution halted: No target code was provided.")
            return

        result = scan_code(user_code)
        
        st.divider()
        st.subheader("Scan Results")
        
        if result["ok"]:
            st.success("✅ [PASSED] Code logic cleared. Clean, secure, and profoundly boring. Proceed.")
            
        
            with st.expander("View Genome Structural Compilation Map", expanded=True):
                tree_output = "\n".join(result["details"])
                st.code(tree_output, language="text")
        else:
            if result["status"] == "rejected":
                st.error(f"❌ [REJECTED] {result['summary']}")
                st.info(result["details"][0])
            else:
                st.error(f"🚨 [SECURITY BLOCK] {result['summary']}")
                st.warning(result["details"][0]) # Error line detail
                st.markdown(f"**S.A.S.S.I. Core Note:** *\"{result['details'][1]}\"*") 

if __name__ == "__main__":
    build_web_page()
