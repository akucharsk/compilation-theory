from tokens_names import *

class Symbol:
    def __init__(self, name):
        self.name = name


class VariableSymbol(Symbol):
    def __init__(self, name, type, size = None, dtype = None, value = None):
        super().__init__(name)
        self.type = type
        self.size = size
        self.dtype = dtype
        self.value = value
        
    def __str__(self) :
        return "<{name}:{type}:{size}{string}>".format(name=self.name, type=self.type, size=self.size, string = f":{self.dtype}" if self.type == MATRIX else "")
    
    def __repr__(self) :
        return str(self)


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
