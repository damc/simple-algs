from math import inf

from .helpers import same


class Strategy:
    def __init__(self, instructions=None):
        self.instructions = instructions or []

    def execute(self, operations_counter):
        for instruction in self.instructions:
            instruction(operations_counter)

    def append(self, instruction):
        self.instructions.append(instruction)

    def __add__(self, other):
        return Strategy(self.instructions + other.instructions)

    def __iadd__(self, other):
        self.instructions += other.instructions

    def __call__(self, max_operations=None):
        self.execute(max_operations)

    def __str__(self):
        instructions_str = [
            str(instruction)
            for instruction in self.instructions
        ]
        return "\n".join(instructions_str)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return same(self, other)


class OperationsCounter:
    def __init__(self, limit=inf):
        self.executed_operations = 0
        self.limit = limit

    def allow_execution(self):
        return self.executed_operations < self.limit

    def increment(self):
        self.executed_operations += 1

    def reset(self):
        self.executed_operations = 0

    def __iadd__(self, other):
        self.executed_operations += other
