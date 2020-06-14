from copy import deepcopy
from json import load

from numpy import array
from pytest import mark

from simple_algs.helpers import same
from simple_algs.instructions import ControlStructure
from simple_algs.memory import Calculator, Tape, MemoryCollection, Ignored
from simple_algs.supervised_learning import SupervisedLearning, DataSample


def test_supervised_learning_1():
    training_data = [DataSample(2, 5), DataSample(3, 7), DataSample(5, 11)]
    testing_data = [DataSample(1, 3), DataSample(4, 9), DataSample(6, 13)]
    calculator = Calculator()
    supervised_learning = SupervisedLearning(
        calculator,
        brute_force_generator_max_length=3
    )
    supervised_learning.fit(training_data)
    for sample in testing_data:
        assert sample.output == supervised_learning.predict(sample.input)


def supervised_learning_2_data():
    test_file_names = ['tests/data/test.json']
    for file_name in test_file_names:
        with open(file_name) as file:
            data = load(file)
        data['train'] = DataSample.from_list_of_dicts(data['train'])
        data['test'] = DataSample.from_list_of_dicts(data['test'])
        for sample in data['train']:
            output_shape = (len(sample.output), len(sample.output[0]))
            sample.input = {
                'input': sample.input,
                'output_shape': output_shape
            }
        for sample in data['test']:
            output_shape = (len(sample.output), len(sample.output[0]))
            sample.input = {
                'input': sample.input,
                'output_shape': output_shape
            }
        yield (data['train'], data['test'])


@mark.parametrize("training_data, testing_data", supervised_learning_2_data())
def test_supervised_learning_2(training_data, testing_data):
    input_tape = Tape(9, (0,))
    output_tape = Tape(9, (0,))
    memory = MemoryCollection(
        {
            'input': input_tape,
            'output_shape': Ignored(),
            'output': output_tape
        },
        output_element='output'
    )

    def move_left():
        input_tape.decrement_pointer(1)
        output_tape.decrement_pointer(1)

    def move_right():
        input_tape.increment_pointer(1)
        output_tape.increment_pointer(1)

    def move_up():
        input_tape.decrement_pointer(0)
        output_tape.decrement_pointer(0)

    def move_down():
        input_tape.increment_pointer(0)
        output_tape.increment_pointer(0)

    def suck_color():
        color = input_tape.get()
        output_tape.select_value(color)

    def paint():
        output_tape.set_selected()

    class ForEachCell(ControlStructure):
        NEEDS_CONDITION = False
        KEYWORD = 'FOR_EACH_CELL'

        def execute(self, operations_counter):
            for i in range(0, input_tape.shape[0]):
                for j in range(0, input_tape.shape[1]):
                    input_tape.pointer = [i, j]
                    output_tape.pointer = [i, j]
                    self.body(operations_counter)
                    if not operations_counter.allow_execution():
                        return

    memory.actions = [
        move_left, move_right, move_up, move_down, suck_color, paint
    ]
    memory.control_structures = [ForEachCell]
    memory.conditions = []

    def preprocess_input(input_):
        input_['input'] = array(input_['input'])
        return input_

    def preprocess_output(output):
        return array(output)

    def postprocess(output):
        return output.tolist()

    supervised_learning = SupervisedLearning(
        preprocess_input=preprocess_input,
        preprocess_output=preprocess_output,
        postprocess_output=postprocess,
        memory=memory,
        brute_force_generator_max_length=5
    )

    def prepare_output_tape(args):
        memory_ = args['supervised_learning'].memory
        output = memory_.elements['output']
        output.shape = memory_.elements['output_shape'].data
        output.data = deepcopy(memory_.elements['input'].data)

    supervised_learning.add_event_listener(
        'pre_strategy_execution',
        prepare_output_tape
    )

    supervised_learning.fit(training_data)

    sample = testing_data[0]
    assert sample.output == supervised_learning.predict(sample.input)


def supervised_learning_3_data():
    return [
        (
            DataSample.from_list_of_dicts(
                [
                    {'input': 5, 'output': [1, 0, 1]},
                    {'input': 10, 'output': [0, 1, 0, 1]},
                    {'input': 8, 'output': [0, 0, 0, 1]},
                    {'input': 99, 'output': [1, 1, 0, 0, 0, 1, 1]},
                    {'input': 2, 'output': [0, 1]}
                ]
            ),
            [
                DataSample(7, [1, 1, 1]),
                DataSample(3, [1, 1]),
                DataSample(6, [0, 1, 1])
            ],
            []
        )
    ]


@mark.parametrize("training_data, testing_data", supervised_learning_3_data())
def test_supervised_learning_3(training_data, testing_data, hyperparameters):
    supervised_learning = SupervisedLearning(**hyperparameters)
    supervised_learning.fit(training_data)
    for sample in testing_data:
        prediction = supervised_learning.predict(sample.input)
        assert same(sample.output, prediction)
