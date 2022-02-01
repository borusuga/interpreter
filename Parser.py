import sys

from ply import yacc
from ply.lex import LexError

from Lexer import Lexer
from d_classes.SyntaxTreeNode import SyntaxTreeNode


class Parser(object):
    tokens = Lexer.tokens

    precedence = (
        ('left', 'ADD', 'SUB'),
        ('left', 'MUL', 'DIV'),
    )

    def __init__(self):
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self)
        self.functions = dict()
        self.ok = True

    def parse(self, s):
        try:
            res = self.parser.parse(s)
            return res, self.functions, self.ok
        except LexError:
            sys.stderr.write(f'Illegal token {s}\n')

    ''' СТРАННО ОПРЕДЕЛЯЕТСЯ НОМЕР ПОЗИЦИИ (от начала документа)'''

    ############ N E W ######################################################

    # программа состоит из функций
    # дети программы - функции
    # функции состоят из stmt_list

    def p_program(self, p):
        """program : fun_list"""  # в main(->parameters_list<-)
        p[0] = SyntaxTreeNode('program', children=p[1], lineno=0, lexpos=0)

    def p_fun_list(self, p):
        """fun_list : function fun_list
                    | function"""
        if len(p) == 2:
            p[0] = p[1]  # SyntaxTreeNode('fun_list', children=[p[1]], lineno=p.lineno(1), lexpos=p.lexpos(1))
        else:
            p[0] = SyntaxTreeNode('fun_list', children=[p[1], p[2]], lineno=p.lineno(2), lexpos=p.lexpos(2))

    def p_function(self, p):  # children - массив параметров, массив stmt_list
        """function : type VARIABLE SQ_OPEN_BR par_list SQ_CLOSING_BR BEGIN stmt_list END DOT
                    | type VARIABLE SQ_OPEN_BR SQ_CLOSING_BR BEGIN stmt_list END DOT"""
        if p[2] not in self.functions:
            if len(p) == 10:
                self.functions[p[2]] = SyntaxTreeNode('function',
                                                      value=p[1],
                                                      children={'param': p[4], 'body': p[7]},
                                                      lineno=p.lineno(2),
                                                      lexpos=p.lexpos(2))
            else:
                self.functions[p[2]] = SyntaxTreeNode('function',
                                                      value=p[1],
                                                      children={'body': p[6]},
                                                      lineno=p.lineno(2),
                                                      lexpos=p.lexpos(2))
        else:
            raise NotImplementedError("Функция с таким именем уже существует")

        if len(p) == 10:
            p[0] = SyntaxTreeNode(node_type='function',
                                  value=[p[2], p[1]],
                                  children=[p[4],
                                            # SyntaxTreeNode('par_list', children=p[4], lineno=p.lineno(2), lexpos=0),
                                            # SyntaxTreeNode('stmt_list', children=p[7], lineno=p.lineno(2) + 1, lexpos=0),
                                            p[7]],
                                  lineno=p.lineno(2),
                                  lexpos=p.lexpos(2))
        else:
            p[0] = SyntaxTreeNode(node_type='function',
                                  value=[p[2], p[1]],
                                  children=[
                                      # SyntaxTreeNode('stmt_list', children=p[6], lineno=p.lineno(5) + 1, lexpos=0),
                                      p[6]],
                                  lineno=p.lineno(2),
                                  lexpos=p.lexpos(2))

    def p_par_list(self, p):
        """par_list : parameter COMMA par_list
                    | parameter"""
        if len(p) == 2:
            p[0] = p[1]  # SyntaxTreeNode('par_list', children=[p[1]], lineno=p.lineno(1), lexpos=p.lexpos(1))
        else:
            p[0] = SyntaxTreeNode('par_list', children=[p[1], p[3]], lineno=p.lineno(3), lexpos=p.lexpos(3))

    def p_parameter(self, p):
        """parameter : type VARIABLE
                    | FIELD type type VARIABLE"""
        # FIELD VARIABLE - добавлено +
        if p[1] == 'field':
            p[0] = SyntaxTreeNode('parameter_matr',
                                  value=[p[3], p[4]],
                                  children=[
                                      SyntaxTreeNode('variable', value=p[4], lineno=p.lineno(1), lexpos=p.lexpos(1))],
                                  lineno=p.lineno(1),
                                  lexpos=p.lexpos(1))
        else:
            p[0] = SyntaxTreeNode('parameter',
                                  value=p[1],
                                  children=[
                                      SyntaxTreeNode('variable', value=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2))],
                                  lineno=p.lineno(2),
                                  lexpos=p.lexpos(2))

    #########################################################################

    # def p_program(self, p):
    #     """program : stmt_list"""  # в main(->parameters_list<-)
    #     p[0] = SyntaxTreeNode('program', children=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_stmt_list(self, p):  # сначала ставим запятые, а для последнего statement - точку
        """stmt_list : statement COMMA stmt_list
                    | statement DOT"""
        if len(p) == 3:
            p[0] = p[
                1]  # SyntaxTreeNode('statement', value='last statement', children=[p[1]], lineno=p.lineno(2), lexpos=0)
        else:
            p[0] = SyntaxTreeNode('stmt_list', value=p[2], children=[p[1], p[3]], lineno=p.lineno(2), lexpos=0)

    def p_statement(self, p):
        """statement : declaration
                    | assignment
                    | arithm_operation
                    | until
                    | check
                    | function_call
                    | robot_operation
                    | return"""
        # | until
        # | comparison
        # | check
        # | function  ??????????????/ а оно вообще надо внутри функции? - скорее всего нет
        # | function_call """
        p[0] = p[1]

    # !!!!!!!!!!!!!!!!!!!!!!!!!!         <---------- arithm_operation <=> literal
    def p_declaration(self, p):
        """declaration : type variable_list R_ASSIGNMENT literal
                        | FIELD type type variable_list R_ASSIGNMENT literal"""
        if len(p) == 5:
            # value - type
            p[0] = SyntaxTreeNode('declaration', value=p[1],
                                  children=[p[2],
                                            # SyntaxTreeNode('identification(s)', children=p[2], lineno=p.lineno(3)),
                                            p[4]],
                                  lineno=p.lineno(3))
        else:
            p[0] = SyntaxTreeNode('declaration_matrix', value=[p[2], p[3]],
                                  children=[p[4],
                                            p[6]],
                                  lineno=p.lineno(1))

    def p_type(self, p):
        """type : TINY
                | SMALL
                | NORMAL
                | BIG"""
        p[0] = p[1]  # SyntaxTreeNode('type', value=p[1], children=[], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_variable_list(self, p):
        """variable_list : VARIABLE variable_list
                        | VARIABLE"""

        if len(p) == 3:
            p[0] = SyntaxTreeNode('variable_list',
                                  children=[
                                      SyntaxTreeNode('variable', value=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1)),
                                      p[2]
                                      # SyntaxTreeNode('variable_list', children=p[2], lineno=p.lineno(1), lexpos=p.lexpos(1))
                                  ],
                                  lineno=p.lineno(1),
                                  lexpos=p.lexpos(1))
        else:
            p[0] = SyntaxTreeNode('variable', value=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_literal(self, p):
        """literal : U_NUMBER
                    | S_NUMBER"""
        p[0] = SyntaxTreeNode('literal', value=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))

    # def p_punctuation_mark(self, p):
    #     """punctuation_mark : COMMA
    #                         | DOT"""
    #
    #     p[0] = p[1]

    def p_assignment(self, p):
        # """assignment : VARIABLE R_ASSIGNMENT VARIABLE
        #                 | VARIABLE R_ASSIGNMENT literal
        #                 | VARIABLE R_ASSIGNMENT arithm_operation
        #                 | VARIABLE R_ASSIGNMENT assignment
        #                 | VARIABLE L_ASSIGNMENT VARIABLE
        #                 | literal L_ASSIGNMENT VARIABLE
        #                 | arithm_operation L_ASSIGNMENT VARIABLE
        #                 | VARIABLE L_ASSIGNMENT assignment
        #                 | arithm_operation L_ASSIGNMENT assignment"""
        """assignment : arithm_operation R_ASSIGNMENT arithm_operation
                        | arithm_operation R_ASSIGNMENT assignment
                        | arithm_operation L_ASSIGNMENT arithm_operation
                        | arithm_operation L_ASSIGNMENT assignment"""

        #  #################################################################  #
        #  #################################################################  #
        #  #                                                               #  #
        #  # добавить проверку детей для корректного добавления в children #  #
        #  #                                                               #  #
        #  #################################################################  #
        #  #################################################################  #
        if not hasattr(p[1], 'type'):
            first = SyntaxTreeNode('variable', value=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))
        else:
            first = p[1]
        if not hasattr(p[3], 'type'):
            second = SyntaxTreeNode('variable', value=p[3], lineno=p.lineno(3), lexpos=p.lexpos(3))
        else:
            second = p[3]
        p[0] = SyntaxTreeNode('assignment',
                              value=p[2],
                              children=[first, second],
                              lineno=p.lineno(2),
                              lexpos=p.lexpos(2))

    def p_arithm_operation(self, p):
        """arithm_operation : OPEN_BR arithm_operation CLOSING_BR
                            | ADD arithm_operation
                            | SUB arithm_operation
                            | arithm_operation MUL arithm_operation
                            | arithm_operation DIV arithm_operation
                            | arithm_operation ADD arithm_operation
                            | arithm_operation SUB arithm_operation"""
        if len(p) == 3:
            p[0] = SyntaxTreeNode('unary_arithm_operation',
                                  value=p[1],
                                  children=[p[2]],
                                  lineno=p.lineno(1),
                                  lexpos=p.lexpos(1))
        elif p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = SyntaxTreeNode('arithm_operation',
                                  value=p[2],
                                  children=[p[1], p[3]],
                                  lineno=p.lineno(1),
                                  lexpos=p.lexpos(1))
        # if not hasattr(p[1], 'type'):
        #     first = SyntaxTreeNode('variable', value=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))
        # else:
        #     first = p[1]
        # if not hasattr(p[3], 'type'):
        #     second = SyntaxTreeNode('variable', value=p[3], lineno=p.lineno(3), lexpos=p.lexpos(3))
        # else:
        #     second = p[3]
        #
        # p[0] = SyntaxTreeNode('arithm_operation',
        #                       value=p[2],
        #                       children=[first, second],
        #                       lineno=p.lineno(1),
        #                       lexpos=p.lexpos(1))

    def p_arithm_operation_endpoints(self, p):
        """arithm_operation : varlit
                            | function_call
                            | robot_operation"""
        p[0] = p[1]

    # def p_operator_low(self, p):
    #     """operator_low : ADD
    #                     | SUB"""
    #     p[0] = p[1]
    #
    # def p_operator_high(self, p):
    #     """operator_high : MUL
    #                     | DIV"""
    #     p[0] = p[1]

    def p_varlit(self, p):
        """varlit : VARIABLE
                    | literal
                    | matr_elem"""
        if not hasattr(p[1], 'type'):
            p[0] = SyntaxTreeNode('variable', value=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))
        else:
            p[0] = p[1]

    def p_matr_elem(self, p):
        """matr_elem : VARIABLE SQ_OPEN_BR literal literal SQ_CLOSING_BR"""
        # children - индексы элемента в матрице VARIABLE
        p[0] = SyntaxTreeNode('matr_elem', value=p[1], children=[p[3], p[4]], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_comparison(self, p):
        """comparison : arithm_operation N_EQ arithm_operation
                        | arithm_operation L_EQ arithm_operation
                        | arithm_operation GR_EQ arithm_operation"""
        # | arithm_operation N_EQ varlit
        # | arithm_operation L_EQ varlit
        # | arithm_operation GR_EQ varlit
        # | varlit N_EQ arithm_operation
        # | varlit L_EQ arithm_operation
        # | varlit GR_EQ arithm_operation
        # | varlit N_EQ varlit
        # | varlit L_EQ varlit
        # | varlit GR_EQ varlit"""
        # возможно нужны лишь первые три строчки, так как так дано в звдании
        p[0] = SyntaxTreeNode('comparison',
                              value=p[2],
                              children=[p[1], p[3]],
                              lineno=p.lineno(1),
                              lexpos=p.lexpos(1))

    def p_until(self, p):
        """until : UNTIL comparison DO stmt_list"""
        p[0] = SyntaxTreeNode('until',
                              # value=p[2],  # comparison statement
                              children=[p[2],  # comparison statement
                                        p[4]],  # until body
                              lineno=p.lineno(1),
                              lexpos=p.lexpos(1))

    def p_check(self, p):
        """check : CHECK comparison DO stmt_list"""
        p[0] = SyntaxTreeNode('check',
                              # value=p[2],  # comparison statement
                              children=[p[2],  # comparison statement
                                        p[4]],  # check body
                              lineno=p.lineno(1),
                              lexpos=p.lexpos(1))

    def p_function_call(self, p):
        """function_call : VARIABLE OPEN_BR CLOSING_BR
                        | VARIABLE OPEN_BR variable_list CLOSING_BR"""
        if len(p) == 4:
            p[0] = SyntaxTreeNode('function_call',
                                  value=p[1],  # function name
                                  # children=[],  # var_list
                                  lineno=p.lineno(1),
                                  lexpos=p.lexpos(1))
        else:
            p[0] = SyntaxTreeNode('function_call',
                                  value=p[1],  # function name
                                  children=[p[3]],  # var_list
                                  lineno=p.lineno(1),
                                  lexpos=p.lexpos(1))

    def p_robot_operation(self, p):
        """robot_operation : GO
                            | RL
                            | RR
                            | SONAR
                            | COMPASS"""
        p[0] = SyntaxTreeNode('robot_operation',
                              value=p[1],  # operation name
                              lineno=p.lineno(1),
                              lexpos=p.lexpos(1))

    def p_return(self, p):
        """return : RETURN arithm_operation"""
        # RETURN aritm_operation - добавлено +
        p[0] = SyntaxTreeNode('return',
                              value=p[1],  # == type
                              children=[p[2]],  # check body
                              lineno=p.lineno(1),
                              lexpos=p.lexpos(1))

    def p_error(self, p):
        err = ""
        try:
            err += f'Syntax error at line: {p.lineno}\n'
        except Exception:
            err += f'Syntax error\n'
        self.ok = False
        raise NotImplementedError(err)

    # def p_var_list(self, p):
    #     """var_list : VARIABLE var_list
    #                 | VARIABLE"""
    #     if len(p) == 1:
    #         p[0] = SyntaxTreeNode('variable', value=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))
    #     else:
    #         p[0] = SyntaxTreeNode('var_list',
    #                               # value=p[1],
    #                               children=[SyntaxTreeNode('variable', value=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1)),
    #                                         SyntaxTreeNode('var_list', lineno=p.lineno(1), lexpos=p.lexpos(1))],
    #                               lineno=p.lineno(1),
    #                               lexpos=p.lexpos(1))


if __name__ == '__main__':
    parser = Parser()

    f = open('robo_data/right_hand_rule.txt', 'r')
    txt = f.read()
    f.close()
    print(f'INPUT: {txt}')
    # tree, func_table, ok = parser.parse(txt)
    tree = parser.parser.parse(txt, debug=True)
    tree.print()
