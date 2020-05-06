from functools import partial

from simple_algs.control_structures import ConditionalStatement, WhileLoop
from simple_algs.memory import Calculator
from simple_algs.strategy import Strategy
from simple_algs.strategy_generators import BruteForceGenerator
from simple_algs.instructions import Action, Condition

actions = [Action(lambda: None), Action(lambda: None), Action(lambda: None)]
control_structures = [ConditionalStatement, WhileLoop]
conditions = [
    Condition(lambda: True),
    Condition(lambda: False),
    Condition(lambda: True)
]


def test_brute_force_generator_1():
    generator = BruteForceGenerator(actions, control_structures, conditions, 5)
    generated = generator.generate()

    expected = [
        Strategy([]),
        Strategy([actions[0], actions[2], actions[1]]),
        Strategy(
            [
                ConditionalStatement(conditions[0], Strategy([actions[1]])),
                actions[2]
            ]
        ),
        Strategy(
            [
                actions[0],
                WhileLoop(conditions[0], Strategy(actions[1:3]))
            ]
        ),
        Strategy(
            [
                ConditionalStatement(conditions[0], Strategy(actions[1:3])),
                actions[2]
            ]
        )
    ]
    for strategy in expected:
        assert strategy in generated


def test_brute_force_generator_2():
    calculator_memory = Calculator()
    generator = BruteForceGenerator(
        calculator_memory.actions,
        [],
        [],
        3
    )
    generated = generator.generate()

    strategy = Strategy(
        [
            Action(calculator_memory.multiply),
            Action(partial(calculator_memory.type, digit=2)),
            Action(partial(calculator_memory.type, digit=1))
        ]
    )
    assert strategy in generated


# control_structures_normalizer_data = [
#     (
#         [
#             actions[0],
#             control_structures[0],
#             conditions[0],
#             actions[1],
#             actions[2],
#             BruteForceGenerator.END_OF_BODY
#         ],
#         [
#             actions[0],
#             partial(
#                 control_structures[0],
#                 condition=conditions[0],
#                 body=[actions[1], actions[2]]
#             )
#         ]
#     ),
#     (
#         [
#             control_structures[0],
#             conditions[0],
#             actions[1],
#             actions[2],
#             BruteForceGenerator.END_OF_BODY,
#             actions[2]
#         ],
#         [
#             partial(
#                 control_structures[0],
#                 condition=conditions[0],
#                 body=[actions[1], actions[2]]
#             ),
#             actions[2]
#         ]
#     ),
#     (
#         [
#             control_structures[0],
#             conditions[0],
#             actions[1],
#             BruteForceGenerator.END_OF_BODY,
#             actions[2]
#         ],
#         [
#             partial(
#                 control_structures[0],
#                 condition=conditions[0],
#                 body=[actions[1]]
#             ),
#             actions[2]
#         ]
#     )
# ]
#
#
# @mark.parametrize("instructions, expected", control_structures_normalizer_data)
# def test_control_structures_normalizer(instructions, expected):
#     normalized = ControlStructuresNormalizer.normalize(instructions)
#     assert Strategy(expected) == Strategy(normalized)
