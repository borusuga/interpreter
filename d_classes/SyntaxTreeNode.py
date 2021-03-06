class SyntaxTreeNode:
    def __init__(self, node_type, value=None, children=None, lineno=None, lexpos=None):
        self.type = node_type
        self.value = value
        self.children = children
        self.lineno = lineno
        self.lexpos = lexpos

    def __repr__(self):
        return f'''type={self.type}; value={self.value}; line={self.lineno} :pos={self.lexpos}'''

    def print(self, level: int = 0):
        if self is None:
            return
        print(' ' * level, self)
        if isinstance(self.children, SyntaxTreeNode):
            self.children.print(level + 1)
        elif isinstance(self.children, list):
            for i in range(len(self.children)):
                self.children[i].print(level + 1)
        elif isinstance(self.children, dict):
            for key, value in self.children.items():
                print(' ' * (level + 1), key)
                if value:
                    value.print(level + 2)
