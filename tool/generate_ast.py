import sys

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python generate_ast.py <output directory>")
        sys.exit(64)
    
    output_dir = sys.argv[1]
    
    expr_types = [
        {"Assign": ["name: Token", "value: Expr"]},
        {"Binary": ["left: Expr", "operator: Token", "right: Expr"]},
        {"Call": ["callee: Expr", "paren: Token", "arguments: list[Expr]"]},
        {"Grouping": ["expression: Expr"]},
        {"Literal": ["value: Any"]},
        {"Logical": ["left: Expr", "operator: Token", "right: Expr"]},
        {"Unary": ["operator: Token", "right: Expr"]},
        {"Variable": ["name: Token"]}
    ]
    
    stmt_types = [
        {"Block": ["statements: list[Stmt]"]},
        {"Expression": ["expression: Expr"]},
        {"Function": ["name: Token", "params: list[Token]", "body: list[Stmt]"]},
        {"If": ["condition: Expr", "then_branch: Stmt", "else_branch: Stmt"]},
        {"Print": ["expression: Expr"]},
        {"Return": ["keyword: Token", "value: Expr"]},
        {"Var": ["name: Token", "initializer: Expr"]},
        {"While": ["condition: Expr", "body: Stmt"]}
    ]
    base_types = list(zip(["Expr", "Stmt"], [expr_types, stmt_types]))

    define_ast(output_dir, "Expr", expr_types)
    define_ast(output_dir, "Stmt", stmt_types)
    define_visitor(output_dir, base_types)

def define_ast(output_dir: str, base_name: str, types: list[dict[str, list[str]]]):
    path = f"{output_dir}/{base_name.lower()}.py"
    with open(path, "w", encoding="UTF-8") as writer:
        lines = ["from abc import ABC, abstractmethod\n",
                 "from typing import Any\n",
                 "from token import Token\n",
                 "from visitor import Visitor\n"]
        if base_name == "Stmt":
            lines += ["from expr import Expr\n"]
        lines += ["\n",
                  f"class {base_name}(ABC):\n",
                  "\n",
                  f"\tdef __repr__(self):\n",
                  f"\t\treturn (type(self).__name__) + str(self.__dict__)\n",
                  "\n"
                  "\t@abstractmethod\n",
                  f"\tdef accept(self, visitor: Visitor):\n",
                  "\t\tpass\n\n"]

        writer.writelines(lines)

        for t in types:
            classname = list(t.keys())[0]
            fields = t[classname]
            define_type(writer, base_name, classname, fields)


def define_visitor(output_dir, base_types):
    path = f"{output_dir}/visitor.py"

    with open(path, "w") as writer:
        writer.writelines(["from abc import ABC, abstractmethod\n",
                           "\n",
                           f"class Visitor(ABC):\n",
                           "\n"
                           ])
        for base in base_types:
            base_name = base[0]
            types = base[1]
            for t in types:
                classname = list(t.keys())[0]
                writer.write("\t@abstractmethod\n")
                writer.write(f"\tdef visit_{classname.lower()}_{base_name.lower()}(self, expr):\n")
                writer.write(f"\t\tpass\n\n")

def define_type(writer, base, classname, fields):
    str_fields = ", ".join(fields)
    writer.write(f"class {classname}({base}):\n")
    writer.write(f"\tdef __init__(self, {str_fields}):\n")
    for field in fields:
        name = field.split(': ')[0]
        writer.write(f"\t\tself.{name} = {name}\n")
    writer.write(f"\n")
    writer.write(f"\tdef accept(self, visitor: Visitor):\n")
    writer.write(f"\t\treturn visitor.visit_{classname.lower()}_{base.lower()}(self)\n\n")

if __name__ == "__main__":
    main()

