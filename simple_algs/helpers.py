from functools import partial
from types import FunctionType, MethodType

from numpy import array_equal, ndarray


class CustomBaseNumber:
    def __init__(self, decimal, base):
        if decimal < 0:
            raise ValueError("Initial decimal can't be lower than 0")
        if base < 1:
            raise ValueError("Base must be at least 1")

        self.base = base
        self.digits = []
        while decimal:
            self.digits.append(decimal % base)
            decimal = decimal // base

    def increment(self):
        if self.digits:
            self.digits[0] += 1
        else:
            self.digits.append(1)
        i = 0
        while self.digits[i] == self.base:
            self.digits[i] = 0
            i += 1
            if i < len(self.digits):
                self.digits[i] += 1
            else:
                self.digits.append(1)

    def __eq__(self, other):
        return (
                isinstance(other, CustomBaseNumber) and
                self.digits == other.digits
        )

    def __len__(self):
        return len(self.digits)


class EventDispatcher:
    def __init__(self, event_listeners=None):
        self.event_listeners = event_listeners or {}

    def add_event_listener(self, event, listener):
        self.event_listeners.setdefault(event, []).append(listener)

    def dispatch_event(self, event, args):
        for listener in self.event_listeners.get(event, []):
            listener(args)


def same(a, b):
    """Check if a is equal b or a is a copy of b"""
    if a.__class__ != b.__class__:
        return False

    same_method = getattr(a, 'same', None)
    if callable(same_method):
        return same_method(b)

    if isinstance(a, partial):
        same_func = same(a.func, b.func)
        same_args = same(a.args, b.args)
        same_keywords = same(a.keywords, b.keywords)
        return same_func and same_args and same_keywords

    if isinstance(a, ndarray):
        return array_equal(a, b)

    if isinstance(a, FunctionType):
        return a == b

    if isinstance(a, MethodType):
        return a.__func__ == b.__func__

    if hasattr(a, '__dict__') and hasattr(b, '__dict__'):
        a = a.__dict__
        b = b.__dict__

    if isinstance(a, dict):
        for key in a:
            if key not in b or not same(a[key], b[key]):
                return False
        return True

    if isinstance(a, set):
        a = list(a)
        b = list(b)
        b_found = [False] * len(b)
        for a_element in a:
            found_same = False
            for b_key, b_element in enumerate(b):
                if same(a_element, b_element):
                    found_same = True
                    b_found[b_key] = True
                    break
            if not found_same:
                return False
        return all(b_found)

    if isinstance(a, list) or isinstance(a, tuple):
        if len(a) != len(b):
            return False
        for key, value in enumerate(a):
            if not same(a[key], b[key]):
                return False
        return True

    return a == b
