class VariableSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name)
        self.type = type


class SymbolTable:
    def __init__(self, parent=None, name=""):
        self.parent = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol):
        self.symbols[name] = symbol

    def get(self, name):
        symbol = self.symbols.get(name)
        if symbol is None and self.parent:
            return self.parent.get(name)
        return symbol

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        return SymbolTable(parent=self, name=name)

    def popScope(self):
        return self.parent
