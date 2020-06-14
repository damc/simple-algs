from inspect import signature

from .strategy import Strategy


class InstructionAbstract:
    def __init__(self, execution):
        self.execution = execution

    def execute(self, operations_counter):
        if 'operations_counter' in signature(self.execution).parameters:
            return self.execution(operations_counter)
        operations_counter.increment()
        return self.execution()

    def __call__(self, *args, **kwargs):
        self.execute(*args, **kwargs)

    def __str__(self):
        return getattr(self.execution, '__name__', str(self.execution))

    def __repr__(self):
        return str(self)


class Action(InstructionAbstract):
    pass


class ControlStructureAbstract(InstructionAbstract):
    NEEDS_CONDITION = False
    KEYWORD = 'UNNAMED_CONTROL_STRUCTURE'

    def __init__(self, condition=None, body=None):
        self.condition = condition
        self.body = body or Strategy()
        super(ControlStructure, self).__init__(None)

    def execute(self, operations_counter):
        raise NotImplementedError("Call to an abstract method")

    def __str__(self):
        return (
                self.KEYWORD + " " +
                (
                    "(" + str(self.condition) + ") " if self.NEEDS_CONDITION
                    else ""
                ) +
                "{\n" +
                self._add_indentation(str(self.body)) +
                "\n}"
        )

    def _add_indentation(self, text):
        return "\t" + text.replace("\n", "\n\t")

    def __repr__(self):
        str(self)


class Condition(InstructionAbstract):
    pass
