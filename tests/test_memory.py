from numpy import zeros, array, array_equal

from helpers import same
from simple_algs.memory import MemoryCollection, Tape, Calculator


def test_memory_collection():
    def a():
        return 1

    def b():
        return 2

    def c():
        return 1

    calculator = Calculator()
    tape = Tape(5, (1,), zeros([1, 2]))
    collection = MemoryCollection(
        {'calculator': calculator, 'tape': tape},
        input_element=calculator,
        output_element=tape,
        additional_actions=[a],
        additional_control_structures=[b],
        additional_conditions=[c]
    )
    assert calculator.add in collection.actions
    assert tape.get in collection.actions
    assert a in collection.actions
    assert b in collection.control_structures
    assert c in collection.conditions


def test_memory_collection_input_output_1():
    tape = Tape(9, (3,))
    collection = MemoryCollection(
        {
            'input': tape,
            'working_memory': Tape(5, (2, 2)),
            'output': tape
        },
        input_element='input',
        output_element='output',
    )

    collection.input(array([1, 2]))
    assert array_equal(array([1, 2]), tape.output())
    assert array_equal(array([1, 2]), collection.output())


def test_memory_collection_input_output_2():
    collection = MemoryCollection(
        {
            'input_1': Tape(9, (3,)),
            'input_2': Tape(9, (3,)),
            'working_memory': Tape(5, (2, 2)),
            'output_1': Tape(9, (3,)),
            'output_2': Tape(9, (3,))
        },
        output_element=['output_1', 'output_2'],
    )

    collection.input({'input_1': array([1, 2]), 'input_2': array([2, 1])})
    assert array_equal(array([1, 2]), collection.elements['input_1'].output())
    assert array_equal(array([2, 1]), collection.elements['input_2'].output())

    collection.elements['output_1'].input(array([2, 3]))
    collection.elements['output_2'].input(array([3, 2]))
    expected_output = {
        'output_1': array([2, 3]),
        'output_2': array([3, 2])
    }
    assert same(expected_output, collection.output())


def test_calculator_1():
    calculator = Calculator(3)
    calculator.input(8)
    assert 8 == calculator.output()
    calculator.type(5)
    calculator.type(3)
    assert 53 == calculator.output()
    calculator.add()
    calculator.type(4)
    calculator.type(0)
    assert 93 == calculator.output()
    calculator.divide()
    calculator.type(3)
    assert 31 == calculator.output()
    calculator.multiply()
    calculator.type(2)
    assert 62 == calculator.output()


def test_calculator_2():
    calculator = Calculator(4)
    calculator.type(3)
    assert 3 == calculator.output()
    calculator.multiply()
    calculator.type(2)
    calculator.type(0)
    assert 60 == calculator.output()


def test_calculator3():
    calculator = Calculator(3)
    calculator.add()
    calculator.input(3)
    calculator.multiply()
    calculator.type(2)
    calculator.add()
    calculator.type(1)
    assert 7 == calculator.output()
