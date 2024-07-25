import collections 
import signal
import time
import atexit
import os

class Sampler: 
    """
    A simple sampling-based profiler for Python programs. It periodically
    collects stack traces to analyze the performance of the code.
    
    Attributes:
        interval (float): Time interval between samples in seconds.
        _started (float): Timestamp when sampling was started.
        _stack_counts (dict): A dictionary to count the occurrences of each stack trace.
        nextId (int): Identifier for the next sample.
    """
    def __init__(self, interval=0.005):
        """
        Initializes the Sampler with the given sampling interval.
        
        Args:
            interval (float): Time interval between samples in seconds.
        """
        self.interval = interval
        self._started = None
        self._stack_counts = collections.defaultdict(int)
        self.nextId = 1
        
    def start(self):
        """
        Starts the sampling process. Sets up the signal handler and
        initializes the timer.
        
        Raises:
            ValueError: If the method is not called from the main thread.
        """
        self._started = time.time()
        try:
            signal.signal(signal.SIGVTALRM, self._sample)
        except ValueError:
            raise ValueError('Can only sample on the main thread')

        signal.setitimer(signal.ITIMER_VIRTUAL, self.interval)
        atexit.register(self.stop)

    def _sample(self, signum, frame):
        """
        Signal handler that collects the current stack trace and stores it.
        
        Args:
            signum (int): The signal number.
            frame (frame): The current stack frame.
        """
        stack = []
        while frame is not None:
            stack.append(self._format_frame(frame))
            frame = frame.f_back
        stack = ';'.join(reversed(stack))
        self._stack_counts[stack] += 1
        signal.setitimer(signal.ITIMER_VIRTUAL, self.interval)
        
    def _format_frame(self, frame):
        """
        Formats a single stack frame into a string.
        
        Args:
            frame (frame): The stack frame to format.
        
        Returns:
            str: The formatted stack frame.
        """
        return '{}:{}:{}:{}'.format(frame.f_globals.get('__name__'),
                                    os.path.basename(frame.f_code.co_filename),
                                    frame.f_lineno,
                                    os.path.basename(frame.f_code.co_name)
                                    )

    def output_stats(self, filename=""):
        """
        Outputs the collected sampling statistics.
        
        Args:
            filename (str): If provided, the statistics will be written to this file.
        
        Returns:
            str: The formatted sampling statistics.
        """
        if self._started is None:
            return ''
        elapsed = time.time() - self._started
        lines = []
        ordered_stacks = sorted(self._stack_counts.items(),
                                key=lambda kv: kv[1], reverse=True)
        lines.extend(['{} {}'.format(frame, count)
                      for frame, count in ordered_stacks])
        if filename != "":
            with open(filename, 'w') as f:
                f.write('\n'.join(lines))
        return '\n'.join(lines)

    def reset(self):
        """
        Resets the sampler's internal state, clearing all collected stack traces
        and resetting the start time.
        """
        self._started = time.time()
        self._stack_counts = collections.defaultdict(int)

    def stop(self):
        """
        Stops the sampling process and resets the sampler's internal state.
        """
        self.reset()
        signal.setitimer(signal.ITIMER_VIRTUAL, 0)

    def __del__(self):
        """
        Ensures that the sampler is stopped and cleaned up when the object
        is destroyed.
        """
        self.stop()
