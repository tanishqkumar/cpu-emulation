from .lex import lex, Token
from .ast_types import Expression, Variable, Literal, Assignment, Return, Program, ASTNode, UnaryOp, BinOp

# (not a) == (b + 3)
    # BinOp(UnaryOp(Variable("a")), "==", BinOp(Variable("b"), "+", Literal(3)))
# x + 5 - y + 2
    # 
# w and not (x == y)
# not a
# eg. [ID, OP, NUMBER] -> BinOp(Variable(ID.name), OP, Literal(NUMBER.value))
def parse_expr(tokens: list[Token]) -> Expression: # need to solve precedence and unary ops 
    if len(tokens) == 0:
        raise RuntimeError("Expected expression, got nothing")
    elif len(tokens) == 1:
        if tokens[0].type == 'ID':
            return Variable(tokens[0].value)
        elif tokens[0].type == 'NUMBER':
            return Literal(tokens[0].value)
        else:
            raise RuntimeError(f"Expected variable or literal, got {tokens[0].type}")
    elif len(tokens) == 2:
        if tokens[0].type == 'OP' and tokens[1].type in ['ID', 'NUMBER']:
            val = Variable(tokens[1].value) if tokens[1].type == 'ID' else Literal(tokens[1].value)
            match tokens[0].value:
                case 'not':
                    return UnaryOp(tokens[0].value, val)
                case _:
                    raise RuntimeError(f"Expected unary operator, got {tokens[0].value}")
        else:
            raise RuntimeError(f"Expected unary operator and variable, got {tokens[0].type} and {tokens[1].type}")
    else: # binops, need order of if stmts to reflect precedence
        # Find RIGHTMOST operator at each precedence level for left-associativity
        # Lower precedence first (evaluated last)
        for i in range(len(tokens) - 1, -1, -1):
            tok = tokens[i]
            if tok.type == 'OP' and tok.value in ['==', '!=', '>', '<', '>=', '<=', 'and', 'or']: 
                return BinOp(parse_expr(tokens[:i]), tok.value, parse_expr(tokens[i+1:]))
        
        for i in range(len(tokens) - 1, -1, -1):
            tok = tokens[i]
            if tok.type == 'OP' and tok.value in ['+', '-']: 
                return BinOp(parse_expr(tokens[:i]), tok.value, parse_expr(tokens[i+1:]))

        raise RuntimeError(f"Expected binary operator, got {tokens[0].type}")


def parse_assignment(tokens: list[Token]) -> Assignment:
    assert len(tokens) > 2, "Expected assignment statement, got something else"
    assert tokens[1].type == 'ASSIGN', "Expected assignment operator, got something else"
    return Assignment(tokens[0].value, parse_expr(tokens[2:]))

def parse_if(tokens: list[Token]) -> If:
    assert tokens[0].type == 'IF', "Expected if keyword, got something else"
    # condition = parse_expr(tokens[1:])
    # then_block = parse_stmt(tokens[2:])
    # TODo 
        # need to add more flags to support >, <, >=, <=, ==, !=, first. (eg. not just Z flag but N)
    return If(condition, then_block, else_block)

def parse_return(tokens: list[Token]) -> Return:
    assert tokens[0].type == 'RETURN', "Expected return keyword, got something else"
    return Return(parse_expr(tokens[1:]))

def parse_stmt(tokens: list[Token]) -> ASTNode:
    if len(tokens) <= 1:
        raise RuntimeError(f"Expected statement, got {tokens[0].type}")
    # route to (parse_assignment, parse_return, parse_expr)
    if tokens[0].type == 'RETURN':
        return parse_return(tokens)
    elif tokens[1].type == 'ASSIGN':
        return parse_assignment(tokens)
    # should handle if/for/while here as well 
    else:
        raise RuntimeError(f"Expected assignment, return, or expression, got {tokens[0].type}")
    
def split_at_newlines(tokens: list[Token]) -> list[list[Token]]:
    stmts = []
    curr = []
    for tok in tokens:
        if tok.type == 'NEWLINE':
            if curr: 
                stmts.append(curr)
                curr = []
        else: 
            curr.append(tok)
    return stmts

def parse(tokens: list[Token]) -> ASTNode:
    stmts = split_at_newlines(tokens)
    parsed_stmts = []
    for stmt in stmts:
        parsed = parse_stmt(stmt)
        parsed_stmts.append(parsed)
    return Program(parsed_stmts)


if __name__ == "__main__":
    program= """
                x=2
                y=5
                z=x+y
                return z+3
            """
    tokens = lex(program)
    ast = parse(tokens)
    