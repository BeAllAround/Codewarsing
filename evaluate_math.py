'''
grammar:

expr
'+', '-'

term
'*', '/'

prim

'('  ')'

'''
class Ch:
    def __init__(self, s, c = 0):
        self.s = s
        self.c = c
    
    def peek(self):
        try:
            return self.s[self.c]
        except IndexError:
            return ''
    
    def is_over(self):
        return self.c >= len(self.s)
    
    def adv(self):
        c = self.c
        self.c += 1
        return self.s[c]
    
    def skip_space(self) -> None:
        while not self.is_over() and self.peek() == ' ':
            self.adv()
        

def expr(s, b = 0):
    if b:
        s.adv()
    left = term(s, 0)
    while 1:
        if s.peek() == '+':
            left = { 'a': left, 'op': '+'}
            right = term(s, 1)
            left['b'] = right
        elif s.peek() == '-':
            left = { 'a': left, 'op': '-'}
            right = term(s, 1)
            left['b'] = right
        else:
            return left

def term(s, b = 0):
    if b: s.adv()
    
    left = prim(s, 0)
    while 1:
        if s.peek() == '*':
            left = { 'a': left, 'op': '*' }
            right = prim(s, 1)
            left['b'] = right
        elif s.peek() == '/':
            left = {'a': left, 'op': '/' }
            right = prim(s, 1)
            left['b'] = right
        else:
            return left
        
def prim(s, b = 0):
    s.skip_space()
    if b: s.adv()
    s.skip_space()
    
    
    if s.peek() == '(':
        v = expr(s, 1)
        if s.peek() != ')':
            raise SyntaxError("unmatched ')'")
        s.adv() # consume ')'
        s.skip_space()
        return v
    
    elif s.peek().isdigit():
        v = ''
        while not s.is_over() and s.peek().isdigit():
            v += s.adv()
        s.skip_space()
        return {'const': int(v, 10) }
    
    elif s.peek() == '-':
        s.adv()
        if s.peek() == ' ':
            raise SyntaxError("")
        v = prim(s, 0)
        s.skip_space()
        return { 'a': v, 'op': '*', 'b': { 'const': -1 } }
        
def resolve_tree(tree):
    op = tree.get('op')
    c = tree.get('const')
    
    if op:
        left = tree.get('a')
        right = tree.get('b')
        if op == '+':
            return resolve_tree(left) + resolve_tree(right)
        elif op == '-':
            return resolve_tree(left) - resolve_tree(right)
        elif op == '*':
            return resolve_tree(left) * resolve_tree(right)
        elif op == '/':
            return resolve_tree(left) / resolve_tree(right)
        
    if c != None:
        return c
        
    
def calc(expression):
    ch = Ch(expression)
    tree = expr(ch)
    
    return resolve_tree(tree)
