import sys

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python generate_ast.py <output directory>")
        sys.exit(64)
    
    output_dir = sys.argv[1]

    define_ast(output_dir, "Expr", [
        {"Binary": ["Expr left", "Token operator", "Expr right"]},
        {"Grouping": ["Expr expression"]},
        {"Literal": ["object value"]},
        {"Unary": ["Token operator", "Expr right"]}
    ])

def define_ast(output_dir: str, base_name: str, types: list[dict[str, list[str]]]):
    path = f"{output_dir}/{base_name}.py"
    with open(path, "w", encoding="UTF-8") as f:
        f.writelines(["from abc import ABC, abstractmethod",
                      "from token import Token",
                      "\n"
                      ])
        # f.writelines

