from functools import partial

from numpy import empty


class Condition:
    def __init__(self, tape, value):
        self.tape = tape
        self.value = value


class MemoryAbstract:
    def __init__(self, actions=None, control_structures=None, conditions=None):
        self.actions = actions or self.default_actions()
        self.control_structures = (
                control_structures or self.default_control_structures()
        )
        self.conditions = conditions or self.default_conditions()

    def input(self, data):
        raise NotImplementedError("Call to an abstract method")

    def output(self):
        raise NotImplementedError("Call to an abstract method")

    def reset(self):
        raise NotImplementedError("Call to an abstract method")

    def default_actions(self):
        return []

    def default_control_structures(self):
        return []

    def default_conditions(self):
        return []


class MemoryCollection(MemoryAbstract):
    def __init__(
            self,
            elements,
            input_element=None,
            output_element=None,
            additional_actions=None,
            additional_control_structures=None,
            additional_conditions=None
    ):
        self.elements = elements

        self.input_element = input_element
        if isinstance(input_element, str):
            try:
                self.input_element = elements[input_element]
            except KeyError:
                raise ValueError('Invalid input element')

        self.output_element = output_element
        if isinstance(output_element, str):
            try:
                self.output_element = elements[output_element]
            except KeyError:
                raise ValueError('Invalid output element')

        self.additional_actions = additional_actions or []
        self.additional_control_structures = (
                additional_control_structures or []
        )
        self.additional_conditions = additional_conditions or []

        super(MemoryCollection, self).__init__()

    def input(self, data):
        if isinstance(data, dict):
            for element_name in data:
                try:
                    self.elements[element_name].input(data[element_name])
                except KeyError:
                    raise ValueError('Invalid element name')
            return
        if self.input_element is None:
            raise ValueError(
                "The memory collection doesn't have input element specified "
                "and it doesn't know where to insert input data."
            )
        self.input_element.input(data)
        return

    def output(self):
        if isinstance(self.output_element, list):
            result = {}
            for element_name in self.output_element:
                try:
                    result[element_name] = self.elements[element_name].output()
                except KeyError:
                    raise ValueError('Invalid element name')
            return result
        return self.output_element.output()

    def reset(self):
        for element_name in self.elements:
            self.elements[element_name].reset()

    def default_actions(self):
        actions = self.additional_actions
        for element_name in self.elements:
            element = self.elements[element_name]
            actions += element.actions
        return actions

    def default_control_structures(self):
        control_structures = self.additional_control_structures
        for element_name in self.elements:
            element = self.elements[element_name]
            control_structures += element.control_structures
        return control_structures

    def default_conditions(self):
        conditions = self.additional_conditions
        for element_name in self.elements:
            element = self.elements[element_name]
            conditions += element.conditions
        return conditions

    def update_instructions(self):
        super(MemoryCollection, self).__init__()


class Tape(MemoryAbstract):
    def __init__(
            self,
            max_value,
            shape,
            data=None,
            pointer=None,
            selected_value=0
    ):
        self.max_value = max_value
        self._shape = shape
        self.data = data if data is not None else empty(shape)
        self.pointer = pointer or [0 for _ in range(len(self.shape))]
        self.selected_value = selected_value
        super(Tape, self).__init__()

    def set(self, value):
        self.data[tuple(self.pointer)] = value

    def get(self):
        return self.data[tuple(self.pointer)]

    def increment_pointer(self, axis=None):
        try:
            self.pointer[axis] += 1
        except IndexError:
            raise ValueError("Invalid axis for shape " + str(self.shape))
        if self.pointer[axis] >= self.shape[axis]:
            self.pointer[axis] = 0

    def decrement_pointer(self, axis=None):
        try:
            self.pointer[axis] -= 1
        except IndexError:
            raise ValueError("Invalid axis for shape " + str(self.shape))
        if self.pointer[axis] < 0:
            self.pointer[axis] = self.shape[axis] - 1

    def select_value(self, value):
        self.selected_value = value

    def set_selected(self):
        self.set(self.selected_value)

    def indicated_value_equals(self, value):
        return self.get() == value

    def input(self, data):
        self.data = data
        self.shape = self.data.shape

    def output(self):
        return self.data

    def reset(self):
        self.data = empty(self.shape)

    def default_actions(self):
        return (
                [
                    partial(self.set, value=i)
                    for i in range(self.max_value + 1)
                ] +
                [self.get] +
                [
                    partial(self.increment_pointer, axis=i)
                    for i in range(len(self.shape))
                ] +
                [
                    partial(self.decrement_pointer, axis=i)
                    for i in range(len(self.shape))
                ]
        )

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape
        self.pointer += [0 for _ in range(len(shape) - len(self.pointer))]

    def default_conditions(self):
        return [
            partial(self.indicated_value_equals, value=i)
            for i in range(self.max_value + 1)
        ]


class Calculator(MemoryAbstract):
    def __init__(
            self,
            input_=None
    ):
        super(Calculator, self).__init__()
        self.result = input_ or 0
        self.displayed = input_ or 0
        self._reset = True
        self._operation = None

    def input(self, input_):
        self.result = input_ or 0
        self.displayed = input_ or 0
        self._reset = True
        self._operation = None

    def output(self):
        self.equal()
        return self.displayed

    def reset(self):
        self.input(0)

    def type(self, digit):
        if self._reset:
            self.displayed = digit
            self._reset = False
        else:
            self.displayed = self.displayed * 10 + digit

    def equal(self):
        if self._operation:
            self.displayed = self._operation(self.result, self.displayed)
            self._operation = None
        self.result = self.displayed
        self._reset = True

    def add(self):
        self.operate(lambda a, b: a + b)

    def deduct(self):
        self.operate(lambda a, b: a - b)

    def multiply(self):
        self.operate(lambda a, b: a * b)

    def divide(self):
        self.operate(lambda a, b: a // b if b != 0 else 0)

    def operate(self, operation):
        self.equal()
        self._operation = operation

    # def increment(self):
    #     self.displayed += 1
    #     self.result = self.displayed
    #
    # def decrement(self):
    #     self.displayed -= 1
    #     self.result = self.displayed

    def default_actions(self):
        return (
                [partial(self.type, digit=i) for i in range(0, 10)] +
                [self.add, self.deduct, self.multiply, self.divide]
        )

    def default_conditions(self):
        return []

    def default_control_structures(self):
        return []


class Ignored(MemoryAbstract):
    def __init__(self, data=None):
        self.data = data
        super(Ignored, self).__init__()

    def input(self, data):
        self.data = data

    def output(self):
        return self.data

    def reset(self):
        self.data = None

    def default_actions(self):
        return []

    def default_conditions(self):
        return []

    def default_control_structures(self):
        return []
