from copy import copy

from .helpers import CustomBaseNumber
from .instructions import Action, Condition, ControlStructureAbstract
from .strategy import Strategy


class StrategyGeneratorAbstract:
    def __init__(self, actions, control_structures, conditions):
        self.actions = self._convert_instructions(actions, Action)
        self.control_structures = control_structures
        self.conditions = self._convert_instructions(conditions, Condition)

    def _convert_instructions(self, instructions, instruction_class):
        return [
            instruction if isinstance(instruction, instruction_class)
            else instruction_class(instruction)
            for instruction in instructions
        ]

    def generate(self):
        raise NotImplementedError("Call to abstract method")


class BruteForceGenerator(StrategyGeneratorAbstract):
    END_OF_BODY = 0

    def __init__(self, actions, control_structures, conditions, max_length):
        self._max_length = max_length
        self._instructions = []
        super(BruteForceGenerator, self).__init__(
            actions,
            control_structures,
            conditions
        )

    def generate(self):
        if len(self.actions) < 1 and len(self.control_structures) < 1:
            return []

        self._prepare_instructions()
        number = CustomBaseNumber(0, len(self._instructions))
        while len(number) <= self._max_length:
            strategy = self._convert_to_strategy(number)
            if isinstance(strategy, Strategy):
                yield strategy
            number.increment()

    def _prepare_instructions(self):
        self._instructions = [BruteForceGenerator.END_OF_BODY]
        self._instructions += self.actions
        for control_structure in self.control_structures:
            if control_structure.NEEDS_CONDITION:
                for condition in self.conditions:
                    self._instructions.append(control_structure(condition))
            else:
                self._instructions.append(control_structure())

    def _convert_to_strategy(self, number):
        strategy = Strategy()
        body_stack = [strategy]
        for digit in number.digits:
            instruction = copy(self._instructions[digit])
            if instruction != self.END_OF_BODY:
                body_stack[-1].append(instruction)
            else:
                body_stack.pop()
                if not body_stack:
                    return False
            if isinstance(instruction, ControlStructureAbstract):
                instruction.body = Strategy()
                body_stack.append(instruction.body)
        return strategy
