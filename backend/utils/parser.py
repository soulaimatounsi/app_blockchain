import re

def extract_features(sol_code):
    return {
        "lines_of_code": len(sol_code.split("\n")),
        "num_functions": len(re.findall(r"function ", sol_code)),
        "num_public": len(re.findall(r"function .*public", sol_code)),
        "num_external": len(re.findall(r"function .*external", sol_code)),
        "num_loops": len(re.findall(r"\bfor\b|\bwhile\b", sol_code)),
        "num_calls": len(re.findall(r"\.call\(", sol_code)),
        "num_delegatecall": len(re.findall(r"\.delegatecall\(", sol_code)),
        "num_transfer": len(re.findall(r"\.transfer\(", sol_code)),
        "num_selfdestruct": len(re.findall(r"selfdestruct\(", sol_code)),
        "uses_safemath": int("SafeMath" in sol_code),
    }
