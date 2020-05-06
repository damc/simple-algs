from copy import deepcopy
from functools import partial

from numpy import array

from simple_algs.helpers import CustomBaseNumber, EventDispatcher, same


def test_custom_base_number_init():
    assert [1, 0, 1] == CustomBaseNumber(5, 2).digits
    assert [0, 1] == CustomBaseNumber(2, 2).digits
    assert [2, 1] == CustomBaseNumber(6, 4).digits


def test_custom_base_number():
    number = CustomBaseNumber(6, 3)
    number.increment()
    assert CustomBaseNumber(7, 3) == number

    for _ in range(4):
        number.increment()
    assert CustomBaseNumber(11, 3) == number

    number = CustomBaseNumber(0, 12)
    number.increment()
    assert CustomBaseNumber(1, 12) == number


def test_event_dispatcher():
    class Human(EventDispatcher):
        def __init__(self):
            self.eaten_cats = []
            super(Human, self).__init__()

        def eat_cat(self, cat_name):
            self.eaten_cats.append(cat_name)
            self.dispatch_event('cat_eaten', {'name': cat_name})

    class EatenKittiesCounter:
        def __init__(self):
            self.eaten_kitties = 0

        def increment_eaten_kitties(self, args):
            if args['name'] == 'kitty':
                self.eaten_kitties += 1

    steve = Human()
    counter = EatenKittiesCounter()
    steve.add_event_listener('cat_eaten', counter.increment_eaten_kitties)
    for _ in range(0, 4):
        steve.eat_cat('kitty')
    steve.eat_cat('smokey')
    assert 4 == counter.eaten_kitties


def test_same():
    class A:
        def __init__(self, a_, b_):
            self.a = a_
            self.b = b_

        def __eq__(self, other):
            return (self.a, self.b) == (other.a, other.b)

    class B:
        def __init__(self, c_, d_):
            self.c = c_
            self.d = d_

        def __eq__(self, other):
            return self.c == other.c

    class C:
        def __init__(self, c_, d_):
            self.c = c_
            self.d = d_

        def same(self, other):
            return self.c == other.c

    a = A(1, B(2, 3))
    b = A(1, B(2, 4))
    assert not same(a, b)

    a = A(1, C(2, 3))
    b = A(1, C(2, 4))
    assert same(a, b)

    a = A(1, {1: C(1, 1)})
    b = A(1, {1: C(1, 2)})
    assert same(a, b)

    a = A(1, [C(1, 1)])
    b = A(1, [C(1, 2)])
    assert same(a, b)

    a = A(1, (C(1, 1),))
    b = A(1, (C(1, 2),))
    assert same(a, b)

    assert same([2, 3], [2, 3])

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

    list1 = [a, b, partial(c, x=5)]
    list2 = [a, b, partial(c, x=5)]
    list3 = [partial(c, x=3), b, a]
    list4 = [a]
    list5 = [a, b, partial(c, x=[partial(d, x=5)])]
    list6 = [a, b, partial(c, x=[partial(d, x=5)])]
    list7 = [a, b, partial(c, x=[partial(d, x=7)])]
    list8 = [a, b, partial(c, x=[partial(d, y=7)])]
    assert same(list1, list2)
    assert not same(list1, list3)
    assert not same(list4, list1)
    assert same(list5, list6)
    assert not same(list7, list8)
    assert not same(list5, list7)

    class A:
        def a(self):
            pass

        def b(self):
            pass

    a = A()
    assert not same(a.a, a.b)
    assert same(a.a, a.a)
    assert same(deepcopy(a.a), a.a)

    assert same(array([1, 2, 3]), array([1, 2, 3]))
    assert not same(array([3, 2, 1]), array([1, 2, 3]))
