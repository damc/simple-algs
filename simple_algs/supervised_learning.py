from copy import deepcopy

from .helpers import EventDispatcher, same
from .strategy import OperationsCounter
from .strategy_generators import BruteForceGenerator


class SupervisedLearning(EventDispatcher):
    def __init__(
            self,
            memory,
            preprocess_input=(lambda x: x),
            preprocess_output=(lambda x: x),
            postprocess_output=(lambda x: x),
            strategy_generator=None,
            brute_force_generator_max_length=5,
            accepted_score=1,
            operations_counter=None,
            max_operations=100
    ):
        self.memory = memory
        self.preprocess_input = preprocess_input
        self.preprocess_output = preprocess_output
        self.postprocess_output = postprocess_output
        self.strategy_generator = strategy_generator or BruteForceGenerator(
            memory.actions,
            memory.control_structures,
            memory.conditions,
            brute_force_generator_max_length
        )
        self.accepted_score = accepted_score
        self.best_strategy = None
        self.best_score = 0
        self.operations_counter = operations_counter or OperationsCounter(
            max_operations
        )
        super(SupervisedLearning, self).__init__()

    def fit(self, data):
        preprocessed_data = self._preprocess(data)
        strategies = self.strategy_generator.generate()
        for strategy in strategies:
            correct = 0
            for sample in preprocessed_data:
                input_ = deepcopy(sample.input)
                prediction = self.predict(input_, strategy, False)
                correct += int(same(prediction, sample.output))
            score = correct / len(data)
            if score > self.best_score:
                self.best_strategy = strategy
                self.best_score = score
                if self.best_score >= self.accepted_score:
                    return

    def predict(self, input_, strategy=None, process=True):
        if strategy is None:
            strategy = self.best_strategy
        if not strategy:
            return None

        preprocessed_input = (
            self.preprocess_input(input_) if process
            else deepcopy(input_)
        )
        self.operations_counter.reset()
        self.memory.reset()
        self.memory.input(preprocessed_input)

        event_args = {
            'supervised_learning': self,
            'strategy': strategy,
            'input': input_,
            'preprocessed_input': preprocessed_input
        }
        self.dispatch_event('pre_strategy_execution', event_args)
        strategy(self.operations_counter)

        postprocessed_output = (
            self.postprocess_output(self.memory.output()) if process
            else self.memory.output()
        )
        return postprocessed_output

    def _preprocess(self, data):
        preprocessed_data = []
        for sample in data:
            input_ = self.preprocess_input(sample.input)
            output = self.preprocess_output(sample.output)
            preprocessed_sample = DataSample(input_, output)
            preprocessed_data.append(preprocessed_sample)
        return preprocessed_data


class DataSample:
    def __init__(self, input_, output):
        self.input = input_
        self.output = output

    @staticmethod
    def from_dict(dict_):
        try:
            return DataSample(dict_['input'], dict_['output'])
        except KeyError:
            raise ValueError(
                "A dictionary must contain 'input' and 'output' keys in order "
                "to convert it to DataSample."
            )

    @staticmethod
    def from_list_of_dicts(list_):
        return [DataSample.from_dict(sample) for sample in list_]
