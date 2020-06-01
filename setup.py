import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_algs",
    version="0.0.1",
    author="Damian Czapiewski",
    author_email="damiancz@mailfence.com",
    description="Library for program synthesis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/damc/simple-algs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
