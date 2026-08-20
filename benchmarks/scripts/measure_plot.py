"""Measure code economy metrics from a benchmark plot.py file.

Usage:
    python measure_plot.py <path_to_plot.py>
    python measure_plot.py <path_to_plot.py> --json

Outputs:
    plot_loc              — non-empty, non-comment lines
    number_of_axes        — Matplotlib axes created (from subplots, add_subplot, etc.)
    helper_function_count — user-defined functions (def statements)

Counting rules:
    plot_loc: strip each line; skip empty; skip lines starting with '#'.
              Docstring lines are NOT excluded.
    number_of_axes: count from code patterns (plt.subplots, fig.add_subplot,
                    fig.add_axes, plt.subplot, ax.inset_axes, twinx, twiny).
                    Manual verification recommended.
    helper_function_count: count top-level and nested 'def' statements.
                           Excludes 'if __name__' boilerplate main().
"""

import ast
import re
import sys
import json
from pathlib import Path


def count_plot_loc(source: str) -> int:
    """Count non-empty, non-comment Python lines."""
    count = 0
    for line in source.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        count += 1
    return count


def count_axes(source: str) -> int:
    """Estimate number of Matplotlib axes from code patterns.

    Detected patterns:
      plt.subplots(r, c, ...) -> r * c axes
      plt.subplots()          -> 1 axis
      fig.add_subplot(...)    -> +1
      fig.add_axes(...)       -> +1
      plt.subplot(...)        -> +1
      .inset_axes(...)        -> +1
      .twinx()                -> +1
      .twiny()                -> +1
    """
    axes = 0

    # plt.subplots with explicit nrows/ncols or positional args
    for m in re.finditer(
        r"plt\.subplots\s*\(([^)]*)\)", source
    ):
        args_str = m.group(1).strip()
        if not args_str:
            axes += 1
            continue

        # Try to extract row and col counts
        nrows, ncols = 1, 1

        # Check for keyword arguments
        kr = re.search(r"nrows\s*=\s*(\d+)", args_str)
        kc = re.search(r"ncols\s*=\s*(\d+)", args_str)
        if kr:
            nrows = int(kr.group(1))
        if kc:
            ncols = int(kc.group(1))

        if not kr and not kc:
            # Try positional: first two integer args
            positional = re.findall(r"^(\d+)\s*,\s*(\d+)", args_str)
            if positional:
                nrows, ncols = int(positional[0][0]), int(positional[0][1])

        axes += nrows * ncols

    # fig.add_subplot, fig.add_axes, plt.subplot
    axes += len(re.findall(r"\.add_subplot\s*\(", source))
    axes += len(re.findall(r"\.add_axes\s*\(", source))
    axes += len(re.findall(r"plt\.subplot\s*\(", source))

    # Inset axes
    axes += len(re.findall(r"\.inset_axes\s*\(", source))

    # Twin axes
    axes += len(re.findall(r"\.twinx\s*\(", source))
    axes += len(re.findall(r"\.twiny\s*\(", source))

    return axes


def count_helper_functions(source: str) -> int:
    """Count user-defined functions using AST parsing.

    Excludes a bare main() that only serves as if __name__ == '__main__' entry.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        # Fallback to regex
        return len(re.findall(r"^\s*def\s+", source, re.MULTILINE))

    func_count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Skip bare main() entry point
            if node.name == "main" and _is_entry_main(tree, node):
                continue
            func_count += 1
    return func_count


def _is_entry_main(tree: ast.Module, func_node: ast.FunctionDef) -> bool:
    """Check if a main() function is just an if __name__ entry point."""
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.If):
            # Check for if __name__ == "__main__"
            try:
                test = node.test
                if (isinstance(test, ast.Compare) and
                    isinstance(test.left, ast.Name) and
                    test.left.id == "__name__"):
                    # Check if body calls main()
                    for stmt in node.body:
                        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                            if (isinstance(stmt.value.func, ast.Name) and
                                stmt.value.func.id == "main"):
                                return True
            except AttributeError:
                pass
    return False


def measure(plot_path: Path) -> dict:
    """Return economy metrics for a single plot.py file."""
    source = plot_path.read_text(encoding="utf-8")
    return {
        "plot_loc": count_plot_loc(source),
        "number_of_axes": count_axes(source),
        "helper_function_count": count_helper_functions(source),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <path_to_plot.py> [--json]")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: {path} not found")
        sys.exit(1)

    result = measure(path)

    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        print(f"plot_loc:              {result['plot_loc']}")
        print(f"number_of_axes:        {result['number_of_axes']}")
        print(f"helper_function_count: {result['helper_function_count']}")
