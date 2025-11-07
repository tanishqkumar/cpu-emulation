from .lex import lex, Token
from .ast_types import Expression, Variable, Literal, Assignment, Return, Program, ASTNode, UnaryOp, BinOp, If, Statement, Block

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
    else: 
        # Find RIGHTMOST operator at each precedence level for left-associativity, order of loops defines precedence
        for i in range(len(tokens) - 1, -1, -1):
            tok = tokens[i]
            if tok.type == 'OP' and tok.value in ['==', '!=', 'and', 'or']: # '>', '<', '>=', '<=', not supported yet
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

def parse_if(block: list[list[Token]]) -> If:
    assert block[0][0].type == 'IF', "Expected if keyword, got something else"
    print(f'INSIDE PARSE_IF')
    print(f'block: {block}')
    print(f'giving parse_expr the tokens: {block[1][1:]}')
    condition = parse_expr(block[0][1:])
    
    print(f'condition: {condition}')
    print(f'giving parse_block the tokens: {block[2:-1]}')
    then_block = parse_block(block[2:-1]) # Block, last element is endif
    
    return If(condition, Block(then_block))

def parse_return(tokens: list[Token]) -> Return:
    assert tokens[0].type == 'RETURN', "Expected return keyword, got something else"
    return Return(parse_expr(tokens[1:]))


def parse_one_liner(tokens: list[Token]) -> ASTNode:
    if len(tokens) <= 1:
        raise RuntimeError(f"Expected statement, got {tokens[0].type}")
    # route to (parse_assignment, parse_return, parse_expr)
    if tokens[0].type == 'RETURN':
        return parse_return(tokens)
    elif tokens[1].type == 'ASSIGN':
        return parse_assignment(tokens)
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


def parse_chunk(i: int, stmts: list[list[Token]]) -> list[ASTNode]: 

    parsed = []
    while i < len(stmts): 
        curr_line = stmts[i]
        
        # casework on [IF, ENDIF, ONE LINERS]
        if curr_line[0].type == 'IF': 
            condn = parse_expr(curr_line[1:]) 
            i, then_block = parse_chunk(i + 1, stmts)
            parsed.append(If(condn, Block(then_block)))
            
        elif curr_line[0].type == 'ENDIF':
            return i + 1, parsed 
        else:
            parsed.append(parse_one_liner(curr_line))
            i += 1

    return i, parsed


def parse(tokens: list[Token]) -> ASTNode:
    stmts = split_at_newlines(tokens) 
    _, parsed_stmts = parse_chunk(0, stmts)
    
    return Program(parsed_stmts)


if __name__ == "__main__":
    program= """
                x = 4
                y = 2
                if x == 5
                    if y == 2
                        x = x + 420 
                    endif
                    x = x + 69
                endif
                z = 4
                return x
            """
    tokens = lex(program)
    ast = parse(tokens)
    print(ast)