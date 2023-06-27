# Simple ALGS

**Note: SimpleALGS is a different thing than ALGS, they simply have a similar name (although there might be some other similarities, but ALGS is a more complex idea)**

SimpleALGS is a library for programmatically creating (possibly "finding" would be a better word) a function/program that meets given specification. Specification is a set of examples of inputs and corresponding outputs of that function/program.

This works for only simple functions/programs (for more complex, it requires too much computational power and too many examples).

I don't develop the project at the moment.

# Examples of usage

The idea of the project is to make possible something like that:

``` python
from simple_algs.automation import function_from_examples

examples = [
    {'input': 5, 'output': [1, 0, 1]},
    {'input': 10, 'output': [0, 1, 0, 1]},
    {'input': 8, 'output': [0, 0, 0, 1]},
    {'input': 99, 'output': [1, 1, 0, 0, 0, 1, 1]},
    {'input': 2, 'output': [0, 1]}
]
dec_to_bin = function_from_examples(examples)

print(dec_to_bin(7))  # prints [1, 1, 1]
print(dec_to_bin(3))  # prints [1, 1]
print(dec_to_bin(6))  # prints [0, 1, 1]
```

In the above example the library is used to make a function that converts an integer to a binary number (as a list of its digits). You give it a list of examples of inputs and corresponding outputs and it returns a function that fits your examples.

In the below example, the library programmatically creates a function that reverses a string and adds "123" at the end of it.

``` python
from simple_algs.automation import function_from_examples

examples = [
    {'input': "Damian", 'output': "naimaD123"},
    {'input': "Rodman", 'output': "namdoR123"},
    {'input': "iran", 'output': "nari123"},
]
modify = function_from_examples(examples)

print(modify("Pakistan"))  # prints "natsikaP123"
print(modify("narrow"))  # prints "worran123"
print(modify("deep"))  # prints "peed123"
```

Creating complex functions with that library takes a lot of time (or computational power). More specifically, the execution of "function_from_examples" method takes a lot of time. With a normal computer, it is possible to automate only simple functions (like the functions from these examples).

You can give a file path as a second argument and then that function will be saved to a file. Thanks to that, if you run the program for the second time, then you won't have to wait until the function is created again. It will simply read that function from the file. This is illustrated in the below example.

``` python
from simple_algs.automation import function_from_examples

examples = [
    {'input': "abcde", 'output': False},
    {'input': "abccba", 'output': True},
    {'input': "bdf", 'output': False},
    {'input': "dbd", 'output': True},
    {'input': "Poland", 'output': False}
    {'input': "polop", 'output': True}
]
is_palindrom = function_from_examples(examples, "is_palindrom.pkl")

print(is_palindrom("gaba"))  # prints False
print(is_palindrom("abba"))  # prints True
print(is_palindrom("kajak"))  # prints True
```

In the above example, the program will take a lot of time only when you run it for the first time.

Sometimes the library can create some function that fits the examples but not the one that you had in mind. Then you simply need to add more examples. If for some input the created function returns a value which is different from the one you want, then simply add that input and the correct output to the examples.

Later, more documentation will be added on how to use the library.

# Current progress

For now, it's possbile to do above examples using SupervisedLearning class. However, it's not possible to do that out of the box, without specyfying any additional parameters. If you want to find arithmetic functions, you need to pass an instance of CalculatorMemory as Memory argument of SuperivsedLearning constructor. For any other function, you would need to pass appropiate Memory and actions arguments as well, but it's more complex.

# Contributing

If you want to contribute to this open-source project, then read [contributing.md](https://github.com/damc/simple-algs/blob/master/contributing.md) file.

