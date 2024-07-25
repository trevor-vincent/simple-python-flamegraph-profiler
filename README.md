
# Simple Python Sampling Profiler with FlameGraph Output

This repository contains a simple sampling-based profiler for Python programs. It periodically collects stack traces to analyze the performance of the code. The output can be directly converted to a FlameGraph using Brendan Greggs Flamegraph perl script. 

## Installation

1. Nothing to install. Python 3 is required. 

## Usage

### Example

```python
from profiler import Sampler

def some_function():
    for i in range(1000000):
        pass

def another_function():
    for i in range(500000):
        pass

def main():
    # Initialize the sampler
    sampler = Sampler()

    # Start the sampler
    sampler.start()

    # Code to profile
    some_function()
    another_function()

    # Stop the sampler
    sampler.stop()

    # Output the collected statistics to a file
    sampler.output_stats("example.stacks")

if __name__ == "__main__":
    main()
```
### Output

The profiler will generate a `.stacks` file containing the profiling results. This file will be named based on your script name with a `.stacks` suffix.

For example, if your script is named `example.py`, the output file will be `example.stacks`.

### Converting the stacks file to a FlameGraph

To convert the profiling output to a FlameGraph, follow these steps:

1. Ensure you have `FlameGraph` tools installed. If not, clone the repository:
    ```bash
    git clone https://github.com/brendangregg/FlameGraph.git
    ```

2. Use the `flamegraph.pl` script to generate the FlameGraph from the `.stacks` file:
    ```bash
    ./FlameGraph/flamegraph.pl example.stacks > example.svg
    ```

3. Open the generated [example.svg](example.svg) file in a web browser to visualize the FlameGraph.

## License

This project is licensed under the MIT License.
