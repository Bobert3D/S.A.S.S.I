import random
import sqlite3
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

# Initialize Lexical Core
PY_LANG = Language(tspython.language())
parser = Parser(PY_LANG)

BANNED_TOKENS = {"os", "subprocess", "eval", "exec", "open", "system", "shutil"}

ROASTS = [
    "Nice try, Dr. Hackerman. Submission denied.",
    "My grandmother writes cleaner code, and she's a ceramic cat.",
    "Syntax violation detected. Please go sit in the corner and think about your life.",
    "This code looks like it was written by a caffeinated squirrel on a broken keyboard.",
    "Security breach blocked. I have logged your IP address and told your mother."
]

def init_database():
    """Creates a local database file to track developer offenses permanently."""
    conn = sqlite3.connect("sassi_scorecard.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            username TEXT PRIMARY KEY,
            roast_count INTEGER DEFAULT 0,
            last_infraction TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_roast(username, reason):
    """Tracks and increments developer offenses in the database scorecard."""
    conn = sqlite3.connect("sassi_scorecard.db")
    cursor = conn.cursor()
    
    # Insert user if they don't exist, or increment their roast counter if they do
    cursor.execute("""
        INSERT INTO leaderboard (username, roast_count, last_infraction)
        VALUES (?, 1, ?)
        ON CONFLICT(username) DO UPDATE SET 
            roast_count = roast_count + 1,
            last_infraction = excluded.last_infraction
    """, (username, reason))
    
    conn.commit()
    conn.close()

def print_leaderboard():
    """Displays the Wall of Shame in the terminal."""
    conn = sqlite3.connect("sassi_scorecard.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, roast_count, last_infraction FROM leaderboard ORDER BY roast_count DESC")
    rows = cursor.fetchall()
    conn.close()
    
    print("\n" + "█"*50)
    print("      S.A.S.S.I. WALL OF SHAME LEADERBOARD      ")
    print("█"*50)
    print(f"{'DEVELOPER':<15} | {'ROASTS':<8} | {'RECENT CRIMES'}")
    print("-" * 50)
    for row in rows:
        print(f"\033[93m{row[0]:<15}\033[0m | {row[1]:<8} | \033[91m{row[2]}\033[0m")
    print("█"*50 + "\n")

def map_and_roast_tree(node, source_bytes, depth=0):
    node_text = source_bytes[node.start_byte:node.end_byte].decode("utf8").strip()
    if node.type in ("identifier", "string") and node_text in BANNED_TOKENS:
        raise PermissionError(f"Banned entity '{node_text}' detected.")
        
    for child in node.children:
        map_and_roast_tree(child, source_bytes, depth + 1)

def sassi_gatekeeper(username, raw_user_code):
    """Main verification gateway mapped to a unique user handle."""
    print("\n" + "═"*70)
    print(f"S.A.S.S.I. INTERROGATING USER: @{username}...")
    print("═"*70)
    
    source_bytes = bytes(raw_user_code, "utf8")
    syntax_tree = parser.parse(source_bytes)
    root = syntax_tree.root_node
    
    if root.has_error:
        print(f"\033[91m[REJECTED]\033[0m Structure corrupted. {random.choice(ROASTS)}")
        log_roast(username, "Corrupted Syntax Layout")
        return False
        
    try:
        map_and_roast_tree(root, source_bytes)
        print(f"\033[92m[PASSED]\033[0m Logic cleared. Secure step verified.")
        return True
    except PermissionError as secure_error:
        print(f"\033[91m[SECURITY BLOCK]\033[0m {secure_error}")
        print(f"\033[93mS.A.S.S.I. Says:\033[0m \"{random.choice(ROASTS)}\"")
        log_roast(username, str(secure_error))
        return False

# --- RUNTIME OPERATIONS TRACKER ---
if __name__ == "__main__":
    init_database()
    
    # Simulation: Different users trying to break rules
    sassi_gatekeeper("AliceCoder", "def add(a, b): return a + b") # Safe
    sassi_gatekeeper("Bobert3D", "def break_code(x) return x")    # Bad syntax
    sassi_gatekeeper("HackerMan99", "import os\nos.system('clear')") # Malicious
    sassi_gatekeeper("Bobert3D", "import subprocess")             # Another exploit attempt!
    
    # Display the score chart!
    print_leaderboard()
