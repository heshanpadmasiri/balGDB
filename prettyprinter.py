import gdb.printing
import gdb

HEAP_ALIGNMENT = 8
TAG_SHIFT = 56
POINTER_MASK = (1 << TAG_SHIFT) - 1
ALIGN_MASK = ~(HEAP_ALIGNMENT - 1)
IMMEDIATE_FLAG = (0x20) << TAG_SHIFT

class VarPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        return str(int(self.val))

class TaggedPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        ptr_val = int(self.val)
        ptr_body = ptr_val & POINTER_MASK
        if ptr_val & IMMEDIATE_FLAG != 0:
            return str(ptr_body)
        new_ptr = (ptr_body & ALIGN_MASK)
        new_val = gdb.Value(new_ptr).cast(self.val.type).dereference()
        return str(int(new_val))

    def bits(self):
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
