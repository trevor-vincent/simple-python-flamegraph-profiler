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
    
