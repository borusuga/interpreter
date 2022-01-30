from Parser import Parser
from SyntaxTreeNode import SyntaxTreeNode
from d_classes.VarClass import *


class Interpreter:
    def __init__(self, parser=Parser()):
        self.parser = parser
        self.map = None
        self.program = None
        self.symbol_table = [dict()]
        self.scope = 0
        self.tree = None
        self.functions = None
        self.robot = None
        self.exit_found = False
        self.ret = None
        self.return_table = dict()

    def interpreter(self, robot=None, program=None):
        self.robot = robot
        self.program = program
        self.symbol_table = [dict()]
        self.tree, self.functions, _correct = self.parser.parse(self.program)
        if _correct:
            if 'main' not in self.functions.keys():
                raise NotImplementedError("NoStartPoint: 'main' function is absent")
            self.interpreter_tree(self.tree)  # prints tree
            try:
                self.type = self.functions['main'].value
                self.ret = False
                self.interpreter_node(self.functions['main'].children['body'])
                return True
            except RecursionError:
                print(f'RecursionError: function calls itself too many times\n')
                print("========= Program has finished with fatal error =========\n")
                return False
        else:
            print(f'Can\'t interpretate incorrect input file\n')

    def interpreter_tree(self, tree):
        print("Program tree:\n")
        tree.print()
        print("\n")

    def interpreter_node(self, node):
        if node is None:
            return ''

        elif node.type == 'stmt_list':
            for ch in node.children:
                if not self.ret:
                    self.interpreter_node(ch)

        # statements
        elif node.type == 'declaration':
            declaration_type = node.value
            declaration_children = node.children
            self.declare_variables(declaration_type, declaration_children)

        elif node.type == 'declaration_matrix':
            declaration_type = node.value[0]
            size_type = node.value[1]
            declaration_children = node.children
            self.declare_matrixes(declaration_type, size_type, declaration_children)

        elif node.type == 'assignment':
            self.assign_r(node)
            self.assign_l(node)

        elif node.type == 'arithm_operation':
            return self.calc(node)

        elif node.type == 'unary_arithm_operation':
            return self.calc_un(node)

        elif node.type == 'variable':
            try:
                return self.symbol_table[self.scope][node.value].value
            except:
                raise NotImplementedError(f"Error: no such variable in this scope: '{node.value}' : line={node.line}")

        elif node.type == 'literal':
            return to_decimal(node.value)

        elif node.type == 'comparison':
            if node.value == "<=":
                return self.interpreter_node(node.children[0]) <= self.interpreter_node(node.children[1])
            elif node.value == "<>":
                return self.interpreter_node(node.children[0]) != self.interpreter_node(node.children[1])
            elif node.value == "=>":
                return self.interpreter_node(node.children[0]) >= self.interpreter_node(node.children[1])
            else:
                print("SOMETHING WRONG...")

        elif node.type == 'until':
            while self.interpreter_node(node.children[0]):
                self.interpreter_node(node.children[1])

        elif node.type == 'check':
            if self.interpreter_node(node.children[0]):
                self.interpreter_node(node.children[1])

        ##########################################################################
        elif node.type == 'return':
            ret_val = self.interpreter_node(node.children[0])
            self.ret = True
            self.return_table[self.scope] = ret_val

        #########################################################################
        elif node.type == 'function_call':
            self.scope += 1
            self.symbol_table.append(dict())
            var_list = self.get_var(node.children[0])
            par_list = self.get_var(self.functions[node.value].children['param'])
            if len(var_list) != len(par_list):
                raise NotImplementedError('Error: Different numbers of arguments')
            # добавление параметров в зону видимости
            for i in range(0, len(var_list)):
                if par_list[i].value in self.symbol_table[self.scope-1][var_list[i].value].type:
                    self.symbol_table[self.scope][par_list[i].children[0].value] = self.symbol_table[self.scope-1][var_list[i].value]
            # выполнение тела функции
            self.interpreter_node(self.functions[node.value].children['body'])
            # возврат значений параметров
            for var, par in var_list, par_list:
                if self.functions[self.scope][var.value].type == par.value:
                    self.functions[self.scope-1][var.value] = self.functions[self.scope][var.value]
            # откат зоны видимости scope[i]
            self.scope -= 1
            self.ret = False
        #########################################################################

    def declare_variables(self, type, children):
        literal = children[1].value
        if children[0].type == 'variable':
            var_name = children[0].value
            self.declare_var(type, var_name, literal)
        elif children[0].type == 'variable_list':
            for child in children[0].children:
                if child.type == 'variable':
                    self.declare_var(type, child.value, literal)
                elif child.type == 'variable_list':
                    self.declare_variables(type, [child, children[1]])

    def declare_var(self, type, var, literal):
        if var in self.symbol_table[self.scope].keys():
            raise NotImplementedError('Redeclaration variable Error')
        else:
            self.symbol_table[self.scope][var] = Variable(type, literal)

    def declare_matrixes(self, var_type, size_type, children):
        literal = children[1].value
        if children[0].type == 'variable':
            var_name = children[0].value
            self.declare_matrix(var_type, size_type, var_name, literal)
        elif children[0].type == 'variable_list':
            for child in children[0].children:
                if child.type == 'variable':
                    self.declare_matrix(var_type, size_type, child.value, literal)
                elif child.type == 'variable_list':
                    self.declare_matrixes(var_type, size_type, [child, children[1]])

    def declare_matrix(self, var_type, size_type, var, literal):
        if var in self.symbol_table[self.scope].keys():
            raise NotImplementedError('Redeclaration variable Error')
        else:
            self.symbol_table[self.scope][var] = MatrixVar(var_type, size_type, literal)

    def assign_r(self, node):
        # сеачала делаем правое присвоение (более приоритетное)
        if node.value == '<<':
            if node.children[0].type == 'variable':  # если узел, которому присваиваем - переменная
                if node.children[1].type != 'assignment':  # если слева не очередной узел присвоения, то:
                    # левому ребёнку присваиваем знчение правого
                    # при этом соблюдается приведение типов с помощью класса Variable
                    self.symbol_table[self.scope][node.children[0].value] = converse(self.symbol_table[self.scope][node.children[0].value].type,
                                                                                     self.interpreter_node(node.children[1]))
                else:  # если слева очередной узел присвоения
                    # текущему левому ребёнку присваиваем значение левого потомка правого ребёнка
                    self.symbol_table[self.scope][node.children[0].value] = converse(self.symbol_table[self.scope][node.children[0].value].type,
                                                                                     self.interpreter_node(node.children[1].children[0]))
            else:
                # иначе - не можем сделать присвоение
                raise NotImplementedError(f'Impossible to perform assignment Error: line={node.line}')
        # запускаем рекурсивно для всех узлов
        if node.children[1].type == 'assignment':
            self.assign_r(node.children[1])

    def assign_l(self, node):
        # потом делаем левое присвоение (менее приоритетное)
        if node.value == '>>':
            if node.children[1].children[0].type == 'variable':
                # если достигли дна дерева:
                if node.children[1].type != 'assignment':
                    # правому ребёнку присваиваем знчение левого
                    self.symbol_table[self.scope][node.children[1].value] = converse(self.symbol_table[self.scope][node.children[1].value].type,
                                                                                     self.interpreter_node(node.children[0]))
                else:
                    # значение текущего левого ребёнка присваиваем левому потомка правого ребёнка
                    self.symbol_table[self.scope][node.children[1].children[0].value] = converse(self.symbol_table[self.scope][node.children[1].children[0].value].type,
                                                                                                 self.interpreter_node(node.children[0]))
            else:
                # иначе - не можем сделать присвоение
                raise NotImplementedError(f'Impossible to perform assignment Error: line={node.line}')
        # запускаем рекурсивно для всех узлов
        if node.children[1].type == 'assignment':
            self.assign_l(node.children[1])

    def calc(self, node):
        # if node.children[0].type == 'arithm_operation':
        first = self.interpreter_node(node.children[0])
        # elif node.children[0].type == 'variable':
        #     first = self.symbol_table[self.scope][node.children[0].value]
        # elif node.children[0].type == 'literal':
        #     first = to_decimal(node.children[0].value)
        # else:
        #     print("SOMETHING WRONG...")

        # if node.children[1].type == 'arithm_operation':
        second = self.interpreter_node(node.children[1])
        # elif node.children[1].type == 'variable':
        #     second = self.symbol_table[self.scope][node.children[1].value]
        # elif node.children[1].type == 'literal':
        #     second = to_decimal(node.children[1].value)
        # else:
        #     print("SOMETHING WRONG...")
        if node.value == '+':
            return first + second
        elif node.value == '-':
            return first - second
        elif node.value == '*':
            return first * second
        elif node.value == '/':
            if second == 0:
                return first/abs(first)*32767
            else:
                return first/second
        else:
            print("SOMETHING WRONG...")

    def calc_un(self, node):
        if node.value == '+':
            return self.interpreter_node(node.children[0])
        else:
            return -self.interpreter_node(node.children[0])

    def process_parlist_to_scope_var(self, node):
        if node.type == 'par_list':
            self.process_parlist_to_scope_var(node.children[0])
            self.process_parlist_to_scope_var(node.children[1])
        else:
            if node.children[0].value in self.symbol_table[self.scope-1].keys():
                if self.symbol_table[self.scope-1][node.children[0].value] == node.value:
                    self.symbol_table[self.scope][node.children[0].value] = self.symbol_table[self.scope-1][node.children[0].value]

    def get_var(self, node):
        this_node = node
        mass = []
        while this_node.children[1].type == 'variable_list' or this_node.children[1].type == 'par_list':
            mass.append(this_node.children[0])
            this_node = this_node.children[1]
        mass.append(this_node.children[0])
        mass.append(this_node.children[1])
        return mass


int = Interpreter()
prog = open('data/test_prog.txt', 'r').read()
res = int.interpreter(program=prog)
