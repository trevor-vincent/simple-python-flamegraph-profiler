
# Simple Python Sampling Profiler with FlameGraph Output

This repository contains a simple sampling-based profiler for Python programs. It periodically collects stack traces to analyze the performance of the code. The output can be directly converted to a FlameGraph using Brendan Greggs Flamegraph perl script. Don't be fooled by the simplicity, it is still very accurate and useful.

## Installation

1. Nothing to install. Python 3 is required. 

## Usage

### Example

```python
from profiler import Sampler

def some_function():
    b = 0    
    for i in range(100000000):
        b += 1

def another_function():
    c = 0
    for i in range(100000000):
        c += 1

def main():
    # Initialize the sampler
    sampler = Sampler()

    # Start the sampler
    sampler.start()

    # Code to profile
    some_function()
    another_function()

    # Output the collected statistics to a file
    sampler.output_stats("example.stacks")
    
    # Stop the sampler
    sampler.stop()

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
