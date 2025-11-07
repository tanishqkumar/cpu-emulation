from .ast_types import Program, Assignment, Return, Expression, Variable, Literal, BinOp, UnaryOp, If, Block
from .parse import parse 
from .lex import lex

TMP_ADDR = 0xF0  # Use address 240 for temp storage (far from program code)
VAR_START_ADDR = 0xA0  # Variables start at address 160 (leave room for ~80 instructions)
 
# Make variables a global
variables = {}

def isvar(name: str) -> bool:
    global variables
    return name in variables

def compile_assignment(assignment: Assignment) -> list[tuple]:
    global variables, VAR_START_ADDR
    out = []
    if assignment.var not in variables:
        variables[assignment.var] = hex(VAR_START_ADDR + len(variables))

    out.extend(compile_expression(assignment.expr))
    out.append(("STA", variables[assignment.var]))
    return out 

def compile_return(ret: Return) -> list[tuple]:
    out = []
    out.extend(compile_expression(ret.expr))
    out.append(("HALT",))
    return out 

def compile_binop(binop: BinOp, temp_depth: int = 0) -> list[tuple]:
    global TMP_ADDR
    out = []
    stack_ptr = TMP_ADDR + temp_depth
    
    if binop.op == "-":
        out.extend(compile_expression(binop.right, temp_depth + 1))
        out.append(("STA", hex(stack_ptr)))
        out.extend(compile_expression(binop.left, temp_depth + 1))
        out.append(("SUB", hex(stack_ptr)))
    else:
        out.extend(compile_expression(binop.left, temp_depth + 1))
        out.append(("STA", hex(stack_ptr)))
        out.extend(compile_expression(binop.right, temp_depth + 1))
        match binop.op:
            case "+":
                out.append(("ADD", hex(stack_ptr)))
            case "and":
                out.append(("AND", hex(stack_ptr)))
            case "or":
                out.append(("OR", hex(stack_ptr)))
            case "^":
                out.append(("XOR", hex(stack_ptr)))
            case "==": 
                out.extend(compile_expression(binop.left, temp_depth + 1))
                out.append(("STA", hex(stack_ptr)))
                out.extend(compile_expression(binop.right, temp_depth + 1))
                out.append(("SUB", hex(stack_ptr)))
            case "!=": 
                out.extend(compile_expression(binop.left, temp_depth + 1))
                out.append(("STA", hex(stack_ptr)))
                out.extend(compile_expression(binop.right, temp_depth + 1))
                out.append(("SUB", hex(stack_ptr)))
                out.append(("NOT",))
            case _:
                raise RuntimeError(f"Unsupported binary operator: {binop.op}")
    return out 

def len_tuple_list(lst: list[tuple]) -> int:
    return sum(len(t) for t in lst)

def compile_chunk(block: Block, curr_addr: int) -> list[tuple]: 
    out = []
    for stmt in block.stmts:
        match stmt: 
            case Assignment():
                out.extend(compile_assignment(stmt))
            case Return():
                out.extend(compile_return(stmt))
            case Expression():
                out.extend(compile_expression(stmt))
            case If(): 
                compiled_condition = compile_expression(stmt.cond)
                out.extend(compiled_condition)
                compiled_then = compile_chunk(stmt.then, curr_addr + len_tuple_list(out) + 2)
                out.append(("JNZ", curr_addr + len_tuple_list(out) + len_tuple_list(compiled_then) + 2))
                out.extend(compiled_then)
            case _:
                raise RuntimeError(f"Unknown statement type: {type(stmt)}")
    return out


def compile_unaryop(unaryop: UnaryOp, temp_depth: int = 0) -> list[tuple]:
    out = []
    out.extend(compile_expression(unaryop.expr, temp_depth))
    match unaryop.op:
        case "not":
            out.append(("NOT",))
        case _:
            raise RuntimeError(f"Unsupported unary operator: {unaryop.op}")
    return out 

def compile_expression(expr: Expression, temp_depth: int = 0) -> list[tuple]:
    global variables
    match expr:
        case Variable():
            return [("LDA", variables[expr.name])]
        case Literal():
            return [("LDI", expr.value)]
        case BinOp():
            return compile_binop(expr, temp_depth)
        case UnaryOp():
            return compile_unaryop(expr, temp_depth)

def compile_ast(program: Program) -> list[tuple]:
    global variables
    out = compile_chunk(Block(program.stmts), 0)
    return out 

def compile(file: str = "program.txt", src: str | None = None) -> list[tuple]:
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

if __name__ == "__main__":
    src = """
            x = 4
            y = 2
            if x == 5
                if y == 2
                    x = x + 420 
                endif
                z = 4
            endif
            return x
    """
    compiled = compile(src=src)
    counter = 0
    for c in compiled:
        print(f"line {counter}: {c}")
        counter += len(c)