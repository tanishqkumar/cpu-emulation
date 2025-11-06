from .ast_types import Program, Assignment, Return, Expression, Variable, Literal, BinOp, UnaryOp
from .parse import parse 
from .lex import lex

TMP_ADDR = 0xF0  # Use address 240 for temp storage (far from program code)
VAR_START_ADDR = 0xA0  # Variables start at address 160 (leave room for ~80 instructions)

# Make variables a global
variables = {}

def compile(file: str = "program.txt", src: str | None = None) -> list[str]:
    global variables
    variables = {}  # Reset variables for every compile call
    if src is None:
        with open(file, "r") as f:
            program_text = f.read()
    else:
        program_text = src
    
    # lex 
    tokens = lex(program_text)
    # parse 
    ast = parse(tokens)
    # compile
    return compile_ast(ast)


def isvar(name: str) -> bool:
    global variables
    return name in variables

def compile_assignment(assignment: Assignment) -> list[str]:
    global variables, VAR_START_ADDR
    out = []
    if assignment.var not in variables:
        variables[assignment.var] = hex(VAR_START_ADDR + len(variables))

    out.extend(compile_expression(assignment.expr))
    out.append(f"STA {variables[assignment.var]}")
    return out 

def compile_return(ret: Return) -> list[str]:
    out = []
    out.extend(compile_expression(ret.expr))
    out.append("HALT")
    return out 

def compile_binop(binop: BinOp, temp_depth: int = 0) -> list[str]:
    global TMP_ADDR
    out = []
    # Use different temp addresses for nested expressions
    stack_ptr = TMP_ADDR + temp_depth
    
    # For SUB, we need special handling because it's not commutative
    # TODO: adding more registers should make this easier 
    if binop.op == "-":
        # Store right in temp first
        out.extend(compile_expression(binop.right, temp_depth + 1))
        out.append(f"STA {stack_ptr}")
        # Load left into ACC
        out.extend(compile_expression(binop.left, temp_depth + 1))
        # Now: ACC = left - right
        out.append(f"SUB {stack_ptr}")
    else:
        # For commutative operators (+, and, or, ^), normal order works
        out.extend(compile_expression(binop.left, temp_depth + 1))
        out.append(f"STA {stack_ptr}")
        out.extend(compile_expression(binop.right, temp_depth + 1))
        match binop.op:
            case "+":
                out.append(f"ADD {stack_ptr}")
            case "and":
                out.append(f"AND {stack_ptr}")
            case "or":
                out.append(f"OR {stack_ptr}")
            case "^":
                out.append(f"XOR {stack_ptr}")
            case ">": # TODO, wip 
                out.extend(compile_expression(binop.left, temp_depth + 1))
                out.append(f"STA {stack_ptr}")
                out.extend(compile_expression(binop.right, temp_depth + 1))
                out.append(f"SUB {stack_ptr}")
            case _:
                raise RuntimeError(f"Unsupported binary operator: {binop.op}")
    return out 

def compile_unaryop(unaryop: UnaryOp, temp_depth: int = 0) -> list[str]:
    out = []
    out.extend(compile_expression(unaryop.expr, temp_depth))
    match unaryop.op:
        case "not":
            out.append("NOT")
        case _:
            raise RuntimeError(f"Unsupported unary operator: {unaryop.op}")
    return out 

def compile_expression(expr: Expression, temp_depth: int = 0) -> list[str]:
    global variables
    match expr:
        case Variable():
            return [f"LDA {variables[expr.name]}"]
        case Literal():
            return [f"LDI {expr.value}"]
        case BinOp():
            return compile_binop(expr, temp_depth)
        case UnaryOp():
            return compile_unaryop(expr, temp_depth)

def compile_ast(ast: Program) -> list[str]:
    global variables
    out = []
    # variables is now global, do not re-declare it here
    for stmt in ast.stmts:
        match stmt: 
            case Assignment():
                out.extend(compile_assignment(stmt))
            case Return():
                out.extend(compile_return(stmt))
            case Expression():
                out.extend(compile_expression(stmt))
            case _:
                raise RuntimeError(f"Unknown statement type: {type(stmt)}")
    return out 


if __name__ == "__main__":
    src = """
    x = 2
    y = 5
    z = x + y
    return z + 3
    """
    compiled = compile(src=src)
    for c in compiled:
        print(c)