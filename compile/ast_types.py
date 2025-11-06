from abc import ABC, abstractmethod

class ASTNode(ABC): 
    pass 

class Statement(ASTNode): 
    pass 

class Expression(ASTNode): # x + y + 3
    pass 

class Return(Statement): 
    def __init__(self, expr: Expression): 
        self.expr = expr

    def __repr__(self) -> str: 
        return f"Return({self.expr!r})"

class Variable(Expression): 
    def __init__(self, name: str): 
        self.name = name

    def __repr__(self) -> str: 
        return f"Variable({self.name!r})"

class Literal(Expression): 
    def __init__(self, value: int): 
        self.value = value

    def __repr__(self) -> str: 
        return f"Literal({self.value!r})"

class Assignment(Statement): 
    def __init__(self, var: str, expr: Expression): 
        self.var = var
        self.expr = expr

    def __repr__(self) -> str: 
        return f"Assignment({self.var!r}, {self.expr!r})"

class BinOp(Expression): # [+, -, *, /, %, **, ==, !=, >, <, >=, <=, and, or]
    def __init__(self, left: Expression, op: str, right: Expression): 
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str: 
        return f"BinOp({self.left!r}, {self.op!r}, {self.right!r})"

class UnaryOp(Expression): # [not, -]
    def __init__(self, op: str, expr: Expression): 
        self.op = op
        self.expr = expr

    def __repr__(self) -> str: 
        return f"UnaryOp({self.op!r}, {self.expr!r})"

class Block: 
    def __init__(self, stmts: list[Statement]):
        self.stmts = stmts

    def __repr__(self) -> str: 
        return f"Block({self.stmts!r})"

class If(Statement):
    def __init__(self, cond: Expression, then: Block):
        self.cond = cond
        self.then = then

    def __repr__(self) -> str: 
        return f"If({self.cond!r}, {self.then!r})"

class Program: 
    def __init__(self, stmts: list[Statement]):
        self.stmts = stmts

    def __repr__(self) -> str: 
        return f"Program({self.stmts!r})"
