import gdb.printing

class VarPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        return str(int(self.val))

class TaggedPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        bits = self.__bits__()
        if bits[63] == '1':
            # immediate
            bin_val = bits[8:]
            return str(int(bin_val, 2))
        return "pointer not implemented"

    def __bits__(self):
        return format(int(self.val), '064b');

def build_pretty_printer():
    pp = gdb.printing.RegexpCollectionPrettyPrinter(
        "bal_pp")
    pp.add_printer('TaggedPtr', '^TaggedPtr$', TaggedPrinter)
    pp.add_printer('var', '^var$', VarPrinter)
    return pp

gdb.printing.register_pretty_printer(
    gdb.current_objfile(),
    build_pretty_printer())
