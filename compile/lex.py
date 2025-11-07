import re
from typing import Any

class Token: 
    def __init__(self, type_: str, value: Any | None = None):
        self.type = type_
        self.value = value

    def __repr__(self) -> str: 
        return f"{self.type}: {self.value}"

def lex(program: str) -> list[Token]:
    tokens = []
    for line in program.split("\n"):
        tokens.extend(lex_line(line))
        tokens.append(Token('NEWLINE', '\n'))
    return tokens


def lex_line(line: str) -> list[Token]:
    tokens = []
    token_specification = [
        ('NUMBER',   r'\d+'),
        ('IF',       r'if\b'),
        ('ENDIF',    r'endif\b'),
        ('RETURN',   r'return\b'),
        ('ID',       r'[A-Za-z_]\w*'),
        # Match multi-char ops first to ensure longest match (order matters)
        ('OP',       r'\*\*|==|!=|>=|<=|and|or|not|[\+\-\*/%><]'),  # covers +, -, *, /, %, >, <, **, ==, !=, >=, <=, and, or
        ('ASSIGN',   r'='),
        ('SKIP',     r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

    for match in re.finditer(tok_regex, line):
        kind = match.lastgroup
        value = match.group()
        token = None
        match kind:
            case 'NUMBER':
                token = Token('NUMBER', int(value))
            case 'IF' | 'ENDIF':
                token = Token(kind)
            case 'RETURN':
                token = Token('RETURN', value)
            case 'ID' | 'ASSIGN':
                token = Token(kind, value)
            case 'OP':
                token = Token('OP', value)
            case 'SKIP':
                continue
            case 'MISMATCH':
                raise RuntimeError(f'Unexpected character {value!r}')
        if token is not None:
            tokens.append(token)
    return tokens

if __name__ == "__main__":
    program= """
                x=2
                y=5
                z=x+y
                return z+3
            """
    tokens = lex(program)
    print(f'Program lexed into {len(tokens)} tokens')
    print(tokens)