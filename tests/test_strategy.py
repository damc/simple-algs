from functools import partial

from simple_algs.instructions import Action
from simple_algs.memory import Calculator
from simple_algs.strategy import Strategy, OperationsCounter


def test_strategy_execute():
    memory = Calculator(5)
    strategy = Strategy([
        Action(memory.add),
        Action(partial(memory.type, digit=3)),
        Action(memory.deduct),
        Action(partial(memory.type, digit=4)),
    ])
    strategy.execute(OperationsCounter())
    assert 4 == memory.output()


def test_strategy_eq():
    def a():
        return 1

    def b():
        return 2

    def c(x):
        if isinstance(x, list):
            x.append(1)
            return x
        return x + 2

    def d(x):
        return x + 3

    strategy1 = Strategy([a, b, partial(c, x=5)])
    strategy2 = Strategy([a, b, partial(c, x=5)])
    strategy3 = Strategy([partial(c, x=3), b, a])
    strategy4 = Strategy([a])
    strategy5 = Strategy([a, b, partial(c, x=[partial(d, x=5)])])
    strategy6 = Strategy([a, b, partial(c, x=[partial(d, x=5)])])
    strategy7 = Strategy([a, b, partial(c, x=[partial(d, x=7)])])
    strategy8 = Strategy([a, b, partial(c, x=[partial(d, y=7)])])
    assert strategy1 == strategy2
    assert strategy1 != strategy3
    assert strategy4 != strategy1
    assert strategy5 == strategy6
    assert strategy7 != strategy8
    assert strategy5 != strategy7

    calculator = Calculator(4)
    strategy9 = Strategy(
        [
            calculator.multiply,
            partial(calculator.type, digit=2),
            calculator.add,
            partial(calculator.type, digit=1)
        ]
    )
    strategy10 = Strategy(
        [
            calculator.add,
            partial(calculator.type, digit=2),
            calculator.add,
            partial(calculator.type, digit=1)
        ]
    )
    assert strategy9 != strategy10
