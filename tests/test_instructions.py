from simple_algs.instructions import Action
from simple_algs.strategy import OperationsCounter


def test_action_execute():
    class RandomClass:
        random_attribute = 0

        @staticmethod
        def set_random_attribute_to_1():
            RandomClass.random_attribute = 1

        @staticmethod
        def set_random_attribute_to_3(operations_counter):
            RandomClass.random_attribute = 3
            operations_counter.increment()

    counter = OperationsCounter()
    action = Action(RandomClass.set_random_attribute_to_1)
    action.execute(counter)
    assert 1 == RandomClass.random_attribute
    assert 1 == counter.executed_operations

    action = Action(RandomClass.set_random_attribute_to_3)
    action.execute(counter)
    assert 3 == RandomClass.random_attribute
    assert 2 == counter.executed_operations
