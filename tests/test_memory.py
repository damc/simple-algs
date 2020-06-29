from functools import partial

from numpy import zeros, array, array_equal

from simple_algs.data_types import Int, Str
from simple_algs.helpers import same
from simple_algs.memory import *


# def test_memory_collection():
#     def a():
#         return 1
#
#     def b():
#         return 2
#
#     def c():
#         return 1
#
#     calculator = Calculator()
#     tape = Tape(5, (1,), zeros([1, 2]))
#     collection = MemoryCollection(
#         {'calculator': calculator, 'tape': tape},
#         input_element=calculator,
#         output_element=tape,
#         additional_actions=[a],
#         additional_control_structures=[b],
#         additional_conditions=[c]
#     )
#     assert calculator.add in collection.actions
#     assert tape.get in collection.actions
#     assert a in collection.actions
#     assert b in collection.control_structures
#     assert c in collection.conditions
#
#
# def test_memory_collection_input_output_1():
#     tape = Tape(9, (3,))
#     collection = MemoryCollection(
#         {
#             'input': tape,
#             'working_memory': Tape(5, (2, 2)),
#             'output': tape
#         },
#         input_element='input',
#         output_element='output',
#     )
#
#     collection.input(array([1, 2]))
#     assert array_equal(array([1, 2]), tape.output())
#     assert array_equal(array([1, 2]), collection.output())
#
#
# def test_memory_collection_input_output_2():
#     collection = MemoryCollection(
#         {
#             'input_1': Tape(9, (3,)),
#             'input_2': Tape(9, (3,)),
#             'working_memory': Tape(5, (2, 2)),
#             'output_1': Tape(9, (3,)),
#             'output_2': Tape(9, (3,))
#         },
#         output_element=['output_1', 'output_2'],
#     )
#
#     collection.input({'input_1': array([1, 2]), 'input_2': array([2, 1])})
#     assert array_equal(array([1, 2]), collection.elements['input_1'].output())
#     assert array_equal(array([2, 1]), collection.elements['input_2'].output())
#
#     collection.elements['output_1'].input(array([2, 3]))
#     collection.elements['output_2'].input(array([3, 2]))
#     expected_output = {
#         'output_1': array([2, 3]),
#         'output_2': array([3, 2])
#     }
#     assert same(expected_output, collection.output())
#
#
# def test_calculator_1():
#     calculator = Calculator(3)
#     calculator.input(8)
#     assert 8 == calculator.output()
#     calculator.type(5)
#     calculator.type(3)
#     assert 53 == calculator.output()
#     calculator.add()
#     calculator.type(4)
#     calculator.type(0)
#     assert 93 == calculator.output()
#     calculator.divide()
#     calculator.type(3)
#     assert 31 == calculator.output()
#     calculator.multiply()
#     calculator.type(2)
#     assert 62 == calculator.output()
#
#
# def test_calculator_2():
#     calculator = Calculator(4)
#     calculator.type(3)
#     assert 3 == calculator.output()
#     calculator.multiply()
#     calculator.type(2)
#     calculator.type(0)
#     assert 60 == calculator.output()
#
#
# def test_calculator3():
#     calculator = Calculator(3)
#     calculator.add()
#     calculator.input(3)
#     calculator.multiply()
#     calculator.type(2)
#     calculator.add()
#     calculator.type(1)
#     assert 7 == calculator.output()


def test_variables():
    def concatenation(a: Str, b: Int) -> Str:
        return a.data.join(str(b.data))

    def int_type_1(a: Int):
        a.type(1)

    def str_type_a(a: Str):
        a.type('a')

    def list_len(l: list) -> Int:
        return Int(len(l))

    variables = Variables(
        Int,
        Int,
        [Int, Str, list],
        [
            int_type_1,
            str_type_a,
            list_len,
            concatenation
        ],
    )
    variables_list = variables.variables
    expected_actions = {
        FunctionCall(
            int_type_1,
            [FunctionParameter(Int, 'a', variables_list[0])],
            None
        ),
        partial(variables.create, type_=Int),
        partial(variables.create, type_=Str),
        partial(variables.create, type_=list)
    }
    assert same(expected_actions, variables.actions)

    variables.create(list)
    expected_actions |= {
        partial(variables.remove, id_=1),
        FunctionCall(
            list_len,
            [FunctionParameter(list, 'l', variables_list[1])],
            FunctionParameter(Int, None, variables_list[0])
        )
    }
    assert same(expected_actions, variables.actions)

    variables.create(Str)
    expected_actions |= {
        partial(variables.remove, id_=2),
        FunctionCall(
            concatenation,
            [
                FunctionParameter(Str, 'a', variables_list[2]),
                FunctionParameter(Int, 'b', variables_list[0])  # fails because there is no argument here, this is because of the bug where I typed 'wrong'
            ],
            FunctionParameter(Str, None, variables_list[2])
        ),
    }
    assert same(expected_actions, variables.actions)

    variables.remove(2)
    expected_actions -= {
        partial(variables.remove, id_=2),
        FunctionCall(
            concatenation,
            [
                FunctionParameter(Str, 'a', variables_list[2]),
                FunctionParameter(Int, 'b', variables_list[0])
            ],
            FunctionParameter(Str, None, variables_list[2])
        ),
    }
    assert same(expected_actions, variables.actions)
