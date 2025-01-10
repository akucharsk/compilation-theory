from queue import LifoQueue


class NoSuchVariableException(Exception):
    pass


class Memory:

    def __init__(self, name): # memory name
        self.name = name
        self.values = {}

    def has_key(self, name):  # variable name
        return name in self.values

    def get(self, name):         # gets from memory current value of variable <name>
        return self.values.get(name, None)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.values[name] = value


class MemoryStack:
                                                                             
    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.stack = [] if memory is None else [memory]

    def get(self, name):             # gets from memory stack current value of variable <name>
        for memory in self.stack[::-1]:
            if memory.has_key(name):
                return memory.get(name)
        raise NoSuchVariableException(f"No variable named {name}")

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        for memory in self.stack[::-1]:
            if memory.has_key(name):
                memory.put(name, value)

    def push(self, memory): # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.stack.pop()


