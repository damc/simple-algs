from functools import partial
from inspect import signature, Signature

from numpy import empty

from .helpers import EventDispatcher


class Condition:
    def __init__(self, tape, value):
        self.tape = tape
        self.value = value


class MemoryAbstract(EventDispatcher):
    def __init__(self, actions=None, control_structures=None, conditions=None):
        self._actions = actions or self.default_actions()
        self.control_structures = (
                control_structures or self.default_control_structures()
        )  # move control structures to supervised_learning
        self._conditions = conditions or self.default_conditions()
        super(MemoryAbstract, self).__init__()

    def input(self, data):
        pass

    def output(self):
        return None

    def reset(self):
        pass

    @property
    def actions(self):
        return self._actions

    @actions.setter
    def actions(self, actions):
        raise PermissionError("Actions property is read-only")

    def default_actions(self):
        return set()

    def default_control_structures(self):
        return set()

    def default_conditions(self):
        return set()


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
        return set(
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
        return set(
            [
                partial(self.indicated_value_equals, value=i)
                for i in range(self.max_value + 1)
            ]
        )


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
        return set(
                [partial(self.type, digit=i) for i in range(0, 10)] +
                [self.add, self.deduct, self.multiply, self.divide]
        )


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


class Variables(MemoryAbstract):
    def __init__(self, input_type, output_type, available_types, functions):
        self._available_types = available_types
        self._functions = functions
        self._variables = []
        self._variables_for_types = {}
        self._functions_for_parameter_types = {}
        self._actions_for_variables = {}
        self._input_type = input_type
        self._output_type = output_type
        self.input_key = 0
        self.output_key = 0 if input_type == output_type else 1

        super(Variables, self).__init__()

        self._prepare_functions_for_parameter_types()
        self._create_input_output_variables()

    def input(self, data):
        self._variables[self.input_key] = data

    def output(self):
        return self._variables[self.output_key]

    def reset(self):
        self._variables = []
        self._create_input_output_variables()

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, variables):
        raise PermissionError("Variables property is read-only")

    def create(self, type_, value=None):
        if value is None:
            value = type_()
        variable = Variable(type(value), value)
        self._variables.append(variable)
        self._actions_for_variables[variable] = []
        self._variables_for_types.setdefault(type_, []).append(variable)

        functions = self._functions_for_parameter_types.get(variable.type, [])
        for function_ in functions:
            call = FunctionCall(function_)
            for parameter in call.parameters:
                if parameter.type == variable.type:
                    parameter.argument = variable
                    call_copy = call.copy_including_parameters_and_return()
                    self._add_every_possible_call_as_action(call_copy)
                    parameter.argument = None

        variable_id = len(self.variables) - 1
        if variable_id > self.output_key:
            remove = partial(self.remove, id_=variable_id)
            self.actions.add(remove)

    def remove(self, id_):
        variable = self._variables[id_]
        self._variables[id_] = None
        actions = self._actions_for_variables[variable]
        for action in actions:
            self._actions.remove(action)
        self._actions_for_variables.pop(variable)

    def default_actions(self):
        return set(
            [
                partial(self.create, type_=type_)
                for type_ in self._available_types
            ]
        )

    def _prepare_functions_for_parameter_types(self):
        for type_ in self._available_types:
            functions = []
            for function_ in self._functions:
                if self._has_parameter_type(function_, type_):
                    functions.append(function_)
            self._functions_for_parameter_types[type_] = functions

    def _has_parameter_type(self, function_, type_):
        call = FunctionCall(function_)
        if call.return_ and call.return_.type == type_:
            return True
        for parameter in call.parameters:
            if parameter.type == type_:
                return True
        return False

    def _create_input_output_variables(self):
        self.create(self._input_type)
        if self._input_type != self._output_type:
            self.create(self._output_type)

    def _add_every_possible_call_as_action(self, call, start_from=0):
        i = start_from
        while (
                i < len(call.parameters) and
                call.parameters[i].argument is not None
        ):
            i += 1

        if (
                i == len(call.parameters) + 1 or
                i == len(call.parameters) and call.return_ is None
        ):
            self._actions.add(call)
            arguments = call.arguments()
            for argument in arguments:
                self._actions_for_variables.setdefault(argument, []).append(
                    call
                )
            return

        parameter = (
            call.parameters[i]
            if len(call.parameters) < i  # wrong
            else call.return_
        )
        if parameter.type is None:
            variables = self._variables
        else:
            variables = self._variables_for_types.get(parameter.type, [])
        for variable in variables:
            parameter.argument = variable
            call_copy = call.copy_including_parameters_and_return()
            self._add_every_possible_call_as_action(call_copy, i + 1)


class FunctionCall:
    def __init__(self, function_, parameters=None, return_=None):
        self.function = function_

        if parameters:
            self.parameters = parameters
        else:
            signature_parameters = signature(function_).parameters
            self.parameters = [
                FunctionParameter(
                    signature_parameters[key].annotation,
                    signature_parameters[key].name,
                    None
                )
                for key in signature_parameters
            ]

            for parameter in self.parameters:
                if parameter.type == Signature.empty:
                    parameter.type = None
            if isinstance(function_, partial):
                self.parameters = self._remove_assigned_parameters(
                    function_,
                    self.parameters
                )

        self.return_ = return_ or FunctionParameter(
            signature(function_).return_annotation,
            None,
            None
        )
        if self.return_.type == Signature.empty:
            self.return_ = None

    def copy_including_parameters_and_return(self):
        parameters = [
            FunctionParameter(
                parameter.type,
                parameter.name,
                parameter.argument
            )
            for parameter in self.parameters
        ]
        return_ = (
            FunctionParameter(
                self.return_.type,
                self.return_.name,
                self.return_.argument
            )
            if self.return_
            else None
        )
        return FunctionCall(self.function, parameters, return_)

    def arguments(self):
        return [parameter.argument for parameter in self.parameters]

    def _remove_assigned_parameters(self, partial_, parameters):
        parameters_new = []
        for parameter in parameters:
            if parameter.name not in partial_.keywords:
                parameters_new.append(parameter)
        return parameters_new

    def __call__(self):  # test
        arguments = {
            parameter.name: parameter.argument.value
            for parameter in self.parameters
        }
        if self.return_ is None:
            self.function(**arguments)
        else:
            self.return_.value = self.function(**arguments)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class_ and
            (
                    (self.function, self.parameters, self.return_) ==
                    (other.function, other.parameters, other.return_)
            )
        )

    def __hash__(self):
        return hash((self.function, tuple(self.parameters), self.return_))


class FunctionParameter:
    def __init__(self, type_, name, argument):
        self.type = type_
        self.name = name
        self.argument = argument

    def __hash__(self):
        return hash((self.type, self.name, self.argument))


class Variable:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
