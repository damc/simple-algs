from .instructions import ControlStructure


class ConditionalStatement(ControlStructure):
    NEEDS_CONDITION = True
    KEYWORD = 'IF'

    def execute(self, operations_counter):
        if (
                self.condition(operations_counter) and
                operations_counter.allow_execution()
        ):
            self.body(operations_counter)


class WhileLoop(ControlStructure):
    NEEDS_CONDITION = True
    KEYWORD = 'WHILE'

    def execute(self, operations_counter):
        while (
                self.condition(operations_counter) and
                operations_counter.allow_execution()
        ):
            self.body(operations_counter)
