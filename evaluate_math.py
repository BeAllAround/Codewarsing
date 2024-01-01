'''
grammar:

expr
'+', '-'

term
'*', '/'

prim

'('  ')'

'''

import math
from math import *

scope = { 'two': lambda x: lambda y: x + y }
scope_globals = globals()

for method in dir(math):
    if not method.startswith('__'):
        scope[method] = scope_globals[method]

# print(scope)

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
        
    elif s.peek() >= 'a' and s.peek() <= 'z':
        v = ''
        while not s.is_over() and (s.peek().isdigit() or s.peek().isalpha() or s.peek() == '_'):
            v += s.adv()
        s.skip_space()
        
        left = {}
        while True:
            if s.peek() == '(':
                args = []
                while True:
                    args.append(expr(s, 1))
                    
                    if s.peek() == ',': 
                        continue
                    elif s.peek() == ')':
                        s.adv()
                        if left.get('args') != None:
                            left['args'].append(args)
                        else:
                            left = { 'func': v, 'args': [ args ] }
                        s.skip_space()
                        break
                    else:
                        raise SyntaxError('unmatched ' + s.peek())
            else:
                if left == {}:
                    return { 'var': v }
                return left
        
    
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
    func = tree.get('func')
    var = tree.get('var')
    
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
        
    if func != None:
        args = tree['args']
        _args = []
        try:
            value = scope[func]
            for arg in args:
                value = value(*map(resolve_tree, arg))
            return value
        except KeyError:
            raise NameError('"' + func + '" not a function')
        

     
    if var != None:
        try:
            return scope[var]
        except KeyError:
            raise NameError('"' + var + '" not defined')
    
def calc(expression, **kwargs):
    ch = Ch(expression)
    tree = expr(ch)
    
    kwargs.get('showtree') == True and print(tree)
    
    if not ch.is_over():
        raise SyntaxError('unmached ' + ch.peek())
    
    return resolve_tree(tree)

if __name__ == '__main__':
    assert calc('1+((8*10))*10') == 1+((8*10))*10
    
    assert calc('pow(1+1, 2+2)', showtree=True) == math.pow(1+1, 2+2)
    assert calc('pow(1+1, 2+2)*2', showtree=True) == math.pow(1+1, 2+2)*2
    assert calc('pow(pow(1+1, 2+2), 2+2)*2', showtree=True) == math.pow(math.pow(1+1, 2+2), 2+2)*2
    
    assert calc('two(pow(10,  10))(2+1)+1', showtree=True) == scope['two'](math.pow(10, 10))(2+1)+1
    
    assert calc('10 * (pi + 1) + 40', showtree=True) == 10 * (math.pi + 1) + 40
