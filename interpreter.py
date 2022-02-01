from Parser import Parser
from Robot import Robot
from d_classes.VarClass import *
from json_convert import convert


class Interpreter:
    def __init__(self, parser=Parser()):
        self.parser = parser
        self.map = None
        self.program = None
        self.symbol_table = [dict()]  # переменные зон видимости
        self.scope = 0
        self.tree = None
        self.functions = None
        self.robot = None
        self.exit_found = False
        self.ret = False
        self.return_table = dict()  # возвращаемые значения зоны видимости {self.scope : return_value}

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

        elif node.type == 'stmt_list' and not self.ret:
            for ch in node.children:
                if not self.ret:
                    self.interpreter_node(ch)

        # statements
        elif node.type == 'declaration' and not self.ret:
            declaration_type = node.value
            declaration_children = node.children
            self.declare_variables(declaration_type, declaration_children)

        elif node.type == 'declaration_matrix' and not self.ret:
            declaration_type = node.value[0]
            size_type = node.value[1]
            declaration_children = node.children
            self.declare_matrixes(declaration_type, size_type, declaration_children)

        elif node.type == 'assignment' and not self.ret:
            # k << b << c >> p << k,
            # k = c
            # b = c
            # скорее всего это так не должно работать, но добавлено (для правого присваивания) +
            self.assign_r(node)
            self.assign_l(node)

        elif node.type == 'arithm_operation' and not self.ret:
            return self.calc(node)

        elif node.type == 'unary_arithm_operation' and not self.ret:
            return self.calc_un(node)

        elif node.type == 'variable' and not self.ret:
            try:
                return self.symbol_table[self.scope][node.value].value
            except:
                raise NotImplementedError(f"Error: no such variable in this scope: '{node.value}' : line={node.line}")

        elif node.type == 'matr_elem' and not self.ret:
            try:
                i = to_decimal(node.children[0].value)
                j = to_decimal(node.children[1].value)
                if (i > self.symbol_table[self.scope][node.value].size or
                        j > self.symbol_table[self.scope][node.value].size):
                    raise NotImplementedError('Error: index out of range')
                return self.symbol_table[self.scope][node.value].matr[i][j]
            except:
                raise NotImplementedError(f"Error: no such variable in this scope: '{node.value}' : line={node.line}")

        elif node.type == 'literal' and not self.ret:
            return to_decimal(node.value)

        elif node.type == 'comparison' and not self.ret:
            if node.value == "<=":
                return self.interpreter_node(node.children[0]) <= self.interpreter_node(node.children[1])
            elif node.value == "<>":
                return self.interpreter_node(node.children[0]) != self.interpreter_node(node.children[1])
            elif node.value == "=>":
                return self.interpreter_node(node.children[0]) >= self.interpreter_node(node.children[1])
            else:
                print("SOMETHING WRONG...")

        elif node.type == 'until' and not self.ret:
            while self.interpreter_node(node.children[0]):
                self.interpreter_node(node.children[1])

        elif node.type == 'check' and not self.ret:
            if self.interpreter_node(node.children[0]):
                self.interpreter_node(node.children[1])

        ##########################################################################
        elif node.type == 'return' and not self.ret:
            n = self.interpreter_node(node.children[0])
            ret_val = converse(self.type, self.interpreter_node(node.children[0])).value
            self.ret = True
            self.return_table[self.scope] = ret_val
            print(f'{self.scope}\t{ret_val}\n')

        #########################################################################
        elif node.type == 'function_call' and not self.ret:
            self.scope += 1
            pr_type = self.type
            self.type = self.functions[node.value].value
            self.symbol_table.append(dict())
            if node.children is not None:
                var_list = self.get_var(node.children[0])
            else:
                var_list = []
            if hasattr(self.functions[node.value].children, 'param'):
                par_list = self.get_var(self.functions[node.value].children['param'])
            else:
                par_list = []
            if len(var_list) != len(par_list):
                raise NotImplementedError('Error: Different numbers of arguments')
            # добавление параметров в зону видимости
            for i in range(0, len(var_list)):
                if par_list[i].value in self.symbol_table[self.scope - 1][var_list[i].value].type:
                    self.symbol_table[self.scope][par_list[i].children[0].value] = self.symbol_table[self.scope - 1][
                        var_list[i].value]
            # выполнение тела функции
            self.interpreter_node(self.functions[node.value].children['body'])
            result = self.return_table[self.scope]
            del self.return_table[self.scope]
            del self.symbol_table[self.scope]
            # откат зоны видимости scope[i]
            self.scope -= 1
            self.type = pr_type
            self.ret = False
            return result
        #########################################################################
        elif node.type == 'robot_operation' and not self.ret:
            if node.value == 'go':
                return self.robot.go()
            elif node.value == 'rr':
                return self.robot.rr()
            elif node.value == 'rl':
                return self.robot.rl()
            elif node.value == 'sonar':
                return self.robot.sonar()
            elif node.value == 'compass':
                return self.robot.compass()

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

    # def assign_r(self, node):
    #     # сеачала делаем правое присвоение (более приоритетное)
    #     if node.value == '<<':
    #         if node.children[0].type == 'variable':  # если узел, которому присваиваем - переменная
    #             if node.children[1].type != 'assignment':  # если слева не очередной узел присвоения, то:
    #                 # левому ребёнку присваиваем знчение правого
    #                 # при этом соблюдается приведение типов с помощью класса Variable
    #                 self.symbol_table[self.scope][node.children[0].value] = converse(self.symbol_table[self.scope][node.children[0].value].type,
    #                                                                                  self.interpreter_node(node.children[1]))
    #             else:  # если слева очередной узел присвоения
    #                 # текущему левому ребёнку присваиваем значение левого потомка правого ребёнка
    #                 self.symbol_table[self.scope][node.children[0].value] = converse(self.symbol_table[self.scope][node.children[0].value].type,
    #                                                                                  self.interpreter_node(node.children[1].children[0]))
    #         else:
    #             # иначе - не можем сделать присвоение
    #             raise NotImplementedError(f'Impossible to perform assignment Error: line={node.line}')
    #     # запускаем рекурсивно для всех узлов
    #     if node.children[1].type == 'assignment':
    #         self.assign_r(node.children[1])

    def assign_r(self, node):
        # сеачала делаем правое присвоение (более приоритетное)
        if node.value == '<<':
            tmp_node = node
            while tmp_node.children[1].type == 'assignment' and tmp_node.children[1].value == '<<':
                tmp_node = tmp_node.children[1]

            if node.children[0].type == 'variable':  # если узел, которому присваиваем - переменная
                if tmp_node.children[1].type != 'assignment':  # если слева не очередной узел присвоения, то:
                    # левому ребёнку присваиваем знчение правого ребёнка
                    # при этом соблюдается приведение типов с помощью класса Variable
                    self.symbol_table[self.scope][node.children[0].value] = converse(
                        self.symbol_table[self.scope][tmp_node.children[0].value].type,
                        self.interpreter_node(tmp_node.children[1]))
                else:  # если слева очередной узел присвоения
                    # текущему левому ребёнку присваиваем значение левого потомка правого ребёнка
                    self.symbol_table[self.scope][node.children[0].value] = converse(
                        self.symbol_table[self.scope][tmp_node.children[0].value].type,
                        self.interpreter_node(tmp_node.children[1].children[0]))
            elif node.children[0].type == 'matr_elem':
                i = to_decimal(node.children[0].children[0].value)
                j = to_decimal(node.children[0].children[1].value)
                if (i > self.symbol_table[self.scope][node.children[0].value].size or
                        j > self.symbol_table[self.scope][node.children[0].value].size):
                    raise NotImplementedError('Error: index out of range')
                if tmp_node.children[1].type != 'assignment':  # если справа не очередной узел присвоения, то:
                    # левому ребёнку присваиваем знчение правого ребёнка
                    # при этом соблюдается приведение типов с помощью класса Variable
                    self.symbol_table[self.scope][node.children[0].value].matr[i][j] = converse(
                        self.symbol_table[self.scope][tmp_node.children[0].value].type,
                        self.interpreter_node(tmp_node.children[1])).value
                else:  # если слева очередной узел присвоения
                    # текущему левому ребёнку присваиваем значение левого потомка правого ребёнка
                    self.symbol_table[self.scope][node.children[0].value].matr[i][j] = converse(
                        self.symbol_table[self.scope][tmp_node.children[0].value].type,
                        self.interpreter_node(tmp_node.children[1].children[0])).value

            else:
                # иначе - не можем сделать присвоение
                raise NotImplementedError(f'Impossible to perform assignment Error: line={node.line}')
        # запускаем рекурсивно для всех узлов
        if node.children[1].type == 'assignment':
            self.assign_r(node.children[1])

    def assign_l(self, node):
        # потом делаем левое присвоение (менее приоритетное)
        if node.value == '>>':
            # если достигли дна дерева:
            if node.children[1].type != 'assignment':
                if node.children[1].type == 'variable':
                    # правому ребёнку присваиваем знчение левого
                    self.symbol_table[self.scope][node.children[1].value] = converse(
                        self.symbol_table[self.scope][node.children[1].value].type,
                        self.interpreter_node(node.children[0]))
                elif node.children[1].type == 'matr_elem':
                    i = to_decimal(node.children[1].children[0].value)
                    j = to_decimal(node.children[1].children[1].value)
                    if (i > self.symbol_table[self.scope][node.children[1].value].size or
                            j > self.symbol_table[self.scope][node.children[1].value].size):
                        raise NotImplementedError('Error: index out of range')
                    self.symbol_table[self.scope][node.children[1].value].matr[i][j] = converse(
                        self.symbol_table[self.scope][node.children[1].value].type,
                        self.interpreter_node(node.children[0])).value
                else:
                    # иначе - не можем сделать присвоение
                    raise NotImplementedError(f'Impossible to perform assignment Error: line={node.line}')
            else:
                if node.children[1].children[0].type == 'variable':
                    # значение текущего левого ребёнка присваиваем левому потомку правого ребёнка
                    self.symbol_table[self.scope][node.children[1].children[0].value] = converse(
                        self.symbol_table[self.scope][node.children[1].children[0].value].type,
                        self.interpreter_node(node.children[0]))
                elif node.children[1].children[0].type == 'matr_elem':
                    i = to_decimal(node.children[1].children[0].children[0].value)
                    j = to_decimal(node.children[1].children[0].children[1].value)
                    if (i > self.symbol_table[self.scope][node.children[1].children[0].value].size or
                            j > self.symbol_table[self.scope][node.children[1].children[0].value].size):
                        raise NotImplementedError('Error: index out of range')
                    self.symbol_table[self.scope][node.children[1].children[0].value].matr[i][j] = converse(
                        self.symbol_table[self.scope][node.children[1].children[0].value].type,
                        self.interpreter_node(node.children[0])).value
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
                return first / abs(first) * 32767
            else:
                return first / second
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
            if node.children[0].value in self.symbol_table[self.scope - 1].keys():
                if self.symbol_table[self.scope - 1][node.children[0].value] == node.value:
                    self.symbol_table[self.scope][node.children[0].value] = self.symbol_table[self.scope - 1][
                        node.children[0].value]

    def get_var(self, node):
        this_node = node
        mass = []
        if this_node.type == 'variable' or this_node.type == 'parameter':
            mass.append(this_node)
            return mass
        while this_node.children[1].type == 'variable_list' or this_node.children[1].type == 'par_list':
            mass.append(this_node.children[0])
            this_node = this_node.children[1]
        mass.append(this_node.children[0])
        mass.append(this_node.children[1])
        return mass


if __name__ == '__main__':
    # robo_data/example1.json
    # robo_data/example2.json
    # robo_data/example3.json
    map_, walls, finish, r = convert('robo_data/example1.json')
    robot = Robot(r['x'], r['y'], r['rotation'], map_, walls, finish)
    int = Interpreter()
    #
    # data/test_prog.txt
    # data/test_assignment.txt
    # data/fibonacci.txt
    # robo_data/test_comands.txt
    # robo_data/right_hand_rule.txt
    prog = open('data/test_prog.txt', 'r').read()
    res = int.interpreter(robot, prog)
    print(int.robot.log)
