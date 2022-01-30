import os
import sys
import ply.lex as lex
import re

reserved = {
    # types
    'tiny': 'TINY', 'small': 'SMALL', 'normal': 'NORMAL', 'big': 'BIG',

    # data structure
    'field': 'FIELD',

    # assignment operator
    '>>': 'R_ASSIGNMENT', '<<': 'L_ASSIGNMENT',

    #  arithmetic operators / unary operators
    '+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV',

    # comparison operators
    '<>': 'N_EQ', '<=': 'L_EQ', '=>': 'GR_EQ',

    # cycle
    'until': 'UNTIL', 'do': 'DO',

    # conditional statement
    'check': 'CHECK',  # 'do': 'DO',

    # function descriptor
    # 'main': 'MAIN_FUN',
    'begin': 'BEGIN', 'end': 'END',
    'return': 'RETURN',

    # robot control operators
    'go': 'GO', 'rl': 'RL', 'rr': 'RR',
    'sonar': 'SONAR',
    'compass': 'COMPASS'

}


class Lexer:
    def __init__(self):
        self.lexer = lex.lex(module=self)

    tokens_list = []

    tokens = [
                 # variable/function name
                 'VARIABLE',  # -#

                 # literal
                 'U_NUMBER', 'S_NUMBER',  # -#

                 # operator brackets
                 'OPEN_BR', 'CLOSING_BR', 'SQ_OPEN_BR', 'SQ_CLOSING_BR',  # -#

                 # other operators
                 'COMMA', 'DOT', #'SPACE'  # -#
             ] + list(reserved.values())

    t_COMMA = r'\,'
    t_DOT = r'\.'
    # t_SPACE = r'\s'
    t_OPEN_BR = r'\('
    t_CLOSING_BR = r'\)'
    t_SQ_OPEN_BR = r'\['
    t_SQ_CLOSING_BR = r'\]'
    t_L_ASSIGNMENT = r'\>\>'
    t_R_ASSIGNMENT = r'\<\<'
    t_N_EQ = r'<>'
    t_L_EQ = r'<='
    t_GR_EQ = r'=>'
    t_ADD = r'\+'
    t_SUB = r'\-'
    t_MUL = r'\*'
    t_DIV = r'\/'

    def t_error(self, t):
        r'\n'
        t.lexer.lineno += 1
        t.lexer.skip(1)

    t_ignore = ' \t'


    def t_VARIABLE(self, t):
        r'[a-z][a-z_0-9]*'
        t.type = reserved.get(t.value, 'VARIABLE')
        return t

    def t_U_NUMBER(self, t):
        r'[0-9A-V]{1,3}'
        return t

    def t_S_NUMBER(self, t):
        r'(\-|\+)[0-9A-V]{1,3}'
        return t

    def input(self, smth):
        return self.lexer.input(smth)

    def token(self):
        return self.lexer.token()

    def genTokens(self, inp):
        self.lexer.input(inp)
        while True:
            try:
                tok = self.lexer.token()
            except lex.LexError:
                self.clear()
                return False
            if not tok:
                break
            self.tokens_list.append(tok)
            # print(tok)  # проверка
        return self.tokens_list

    def parse(self, inp: str):
        self.clear()
        self.genTokens(inp)
        # return self.check()

    def clear(self):
        self.tokens_list.clear()


# pars = Lexer()
# f = open('test_prog.txt', 'r')
# data = f.read()
# f.close()
# pars.parse(data)
# print('omegalol')
