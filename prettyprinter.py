import gdb
class VarPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        return str(self.val.type.name)

    @staticmethod
    def display_hint():
        return "hint"

def bal_printer(val):
    valType = str(val.type.name)
    print("called")
    if valType == "var":
        return VarPrinter(val)
    elif valType == "TaggedPtr":
        return VarPrinter(val)


gdb.pretty_printers.append(bal_printer)
