class Variable:
    def __init__(self, var_type, var_value):
        if not isinstance(var_value, int):
            # TINY
            if var_type == 'tiny':
                self.type = var_type
                if var_value in ['0', '1']:
                    self.value = int(var_value)
                else:
                    raise NotImplementedError("Type mismatch! tiny: 0..1")
            # SMALL
            elif var_type == 'small':
                self.value = to_decimal(var_value)
                # SMALL SIGNED
                if var_value[0] in ['-', '+']:
                    self.type = "s_{}".format(var_type)
                    if self.value not in range(-16, 16):
                        raise NotImplementedError(
                            "Type mismatch! Signed small: -16..+15 [-G..+F]. You got: {}".format(var_value))
                # SMALL UNSIGNED
                else:
                    self.type = "u_{}".format(var_type)
                    if self.value not in range(0, 32):
                        raise NotImplementedError(
                            "Type mismatch! Unsigned small: 0..31 [0..V]. You got: {}".format(var_value))

            # NORMAL
            elif var_type == 'normal':
                self.value = to_decimal(var_value)
                # NORMAL SIGNED
                if var_value[0] in ['-', '+']:
                    self.type = "s_{}".format(var_type)
                    if self.value not in range(-512, 512):
                        raise NotImplementedError(
                            "Type mismatch! Signed normal: -512..+511 [-G0..+FV]. You got: {}".format(var_value))
                # NORMAL UNSIGNED
                else:
                    self.type = "u_{}".format(var_type)
                    if self.value not in range(0, 1024):
                        raise NotImplementedError(
                            "Type mismatch! Unsigned normal: 0..1023 [0..VV]. You got: {}".format(var_value))

            # BIG
            elif var_type == 'big':
                self.value = to_decimal(var_value)
                # BIG SIGNED
                if var_value[0] in ['-', '+']:
                    self.type = "s_{}".format(var_type)
                    if self.value not in range(-16384, 16384):
                        raise NotImplementedError(
                            "Type mismatch! Signed big: -16384..+16383 [-G00..+FVV]. You got: {}".format(var_value))
                # BIG UNSIGNED
                else:
                    self.type = "u_{}".format(var_type)
                    if self.value not in range(0, 32768):
                        raise NotImplementedError(
                            "Type mismatch! Unsigned big: 0..32768 [0..VVV]. You got: {}".format(var_value))

        else:
            self.type = var_type
            self.value = var_value

    def __repr__(self):
        return f'{self.type} {self.value}'

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.value == other.value
        return NotImplemented


class MatrixVar:
    def __init__(self, var_type, size_type, var_value):
        self.type = var_type
        if size_type == 'tiny':
            self.size = 1
        elif size_type == 'small':
            self.size = 31
        elif size_type == 'normal':
            self.size = 1023
        elif size_type == 'big':
            self.size = 32767
        var = Variable(var_type, var_value)
        self.matr = [[var.value] * self.size for _ in range(self.size)]

    def __repr__(self):
        s_matr = ""
        for line in self.matr:
            s_matr += f'{line}\n'
        return f'{self.type}:\n{s_matr}'


def to_decimal(n):
    try:
        return int(n, 32)
    except ValueError:
        raise NotImplementedError("Wrong value: invalid value for number with base 32: {}".format(n))


def converse(typeVar, value):  # приведение типов
    # TINY
    if typeVar == 'tiny':
        if abs(0 - value) < abs(1 - value):
            return Variable(typeVar, 0)
        else:
            return Variable(typeVar, 1)
    # SMALL
    elif typeVar == 'u_small':
        if value in range(0, 32):
            return Variable(typeVar, value)
        else:
            if abs(0 - value) < abs(31 - value):
                return Variable(typeVar, 0)
            else:
                return Variable(typeVar, 31)

    elif typeVar == 's_small':
        if value in range(-16, 16):
            return Variable(typeVar, value)
        else:
            if abs(-16 - value) < abs(15 - value):
                return Variable(typeVar, -16)
            else:
                return Variable(typeVar, 15)
    # NORMAL
    elif typeVar == 'u_normal':
        if value in range(0, 1024):
            return Variable(typeVar, value)
        else:
            if abs(0 - value) < abs(1023 - value):
                return Variable(typeVar, 0)
            else:
                return Variable(typeVar, 1023)

    elif typeVar == 's_normal':
        if value in range(-512, 512):
            return Variable(typeVar, value)
        else:
            if abs(-512 - value) < abs(511 - value):
                return Variable(typeVar, -512)
            else:
                return Variable(typeVar, 511)
    # BIG
    elif typeVar == 'u_big':
        if value in range(0, 32768):
            return Variable(typeVar, value)
        else:
            if abs(0 - value) < abs(32767 - value):
                return Variable(typeVar, 0)
            else:
                return Variable(typeVar, 32767)

    elif typeVar == 's_big':
        if value in range(-16384, 16384):
            return Variable(typeVar, value)
        else:
            if abs(-16384 - value) < abs(16383 - value):
                return Variable(typeVar, -16384)
            else:
                return Variable(typeVar, 16383)



if __name__ == '__main__':
    m = MatrixVar('normal', 'small', '0')
    print(m)
