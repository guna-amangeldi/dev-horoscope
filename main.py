import ast
import sys
from pathlib import Path


def analyze_code(path: Path) -> dict:
    """
    Analyze a Python file and return simple metrics about structure.
    """
    source = path.read_text(encoding="utf-8")

    # Basic line-level metrics
    lines = source.splitlines()
    total_lines = len(lines)
    comment_lines = sum(1 for line in lines if line.strip().startswith("#"))
    todo_lines = sum(1 for line in lines if "TODO" in line.upper())

    # Use AST (Abstract Syntax Tree) to inspect structure
    tree = ast.parse(source)

    func_defs = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    num_functions = len(func_defs)

    # Approximate function length (by line numbers)
    func_lengths = []
    for func in func_defs:
        if hasattr(func, "lineno") and hasattr(func, "end_lineno"):
            func_lengths.append(func.end_lineno - func.lineno + 1)
    avg_func_length = sum(func_lengths) / len(func_lengths) if func_lengths else 0

    return {
        "total_lines": total_lines,
        "comment_lines": comment_lines,
        "todo_lines": todo_lines,
        "num_functions": num_functions,
        "avg_func_length": avg_func_length,
    }


def generate_horoscope(metrics: dict) -> str:
    """
    Turn code metrics into a playful 'developer horoscope'.
    """
    lines = metrics["total_lines"]
    comments = metrics["comment_lines"]
    todos = metrics["todo_lines"]
    funcs = metrics["num_functions"]
    avg_len = metrics["avg_func_length"]

    messages = []

    # Comment ratio
    if lines > 0:
        comment_ratio = comments / lines
    else:
        comment_ratio = 0.0

    if comment_ratio < 0.05:
        messages.append("The stars whisper: your future holds… documentation. Consider leaving clues for your teammates.")
    elif comment_ratio < 0.20:
        messages.append("You comment when it matters. A balanced mind in a chaotic codebase.")
    else:
        messages.append("Your comments shine brighter than your code. Future you will be very grateful.")

    # Functions / structure
    if funcs == 0:
        messages.append("The cosmos sees one giant script. Perhaps it is time to split logic into functions.")
    elif funcs < 5:
        messages.append("Few but focused functions. You seek clarity over fragmentation.")
    else:
        messages.append("Many small functions: you embrace modularity. The gods of refactoring approve.")

    # Average function length
    if avg_len > 50:
        messages.append("Some functions carry heavy destiny. Consider granting them smaller responsibilities.")
    elif 0 < avg_len <= 15:
        messages.append("Short functions, sharp focus. Your future PRs will be easy to review.")
    elif avg_len == 0:
        pass  # no functions, already handled above
    else:
        messages.append("Your functions have a healthy length. The balance of Zen and practicality is strong in you.")

    # TODOs
    if todos == 0:
        messages.append("No TODOs in sight. Either your work is complete, or you fear the truth.")
    elif todos < 5:
        messages.append("A few TODOs mark the path ahead. Future sprints already know their purpose.")
    else:
        messages.append("Many TODOs gather like clouds. This is a sign to schedule a refactoring ritual.")

    # Total lines
    if lines < 50:
        messages.append("A small file with big potential. Every line matters.")
    elif lines > 500:
        messages.append("The constellations warn of a mighty file. Perhaps some pieces long to be modules.")
    else:
        messages.append("Your file walks the middle path: not too small, not too sprawling.")

    horoscope = "\n".join(f"• {msg}" for msg in messages)
    return horoscope


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path-to-python-file>")
        sys.exit(1)

    path = Path(sys.argv[1])

    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)

    try:
        metrics = analyze_code(path)
    except SyntaxError as e:
        print(f"Could not parse file due to syntax error: {e}")
        sys.exit(1)

    print(f"Analyzing: {path}")
    print()
    print("Your developer horoscope:")
    print("--------------------------")
    print(generate_horoscope(metrics))


if __name__ == "__main__":
    main()
