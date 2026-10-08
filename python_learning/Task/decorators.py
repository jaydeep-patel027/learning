import time

# Challenge 1: Write a decorator time_decorator that measures the time taken by a function to execute.
def time_decorator(func):
    """A decorator that measures and prints the execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time of '{func.__name__}': {end_time - start_time:.4f} seconds")
        return result
    return wrapper

# Challenge 2: Use the decorator on a function slow_function that sleeps for 2 seconds and then prints "Function complete".
@time_decorator
def slow_function():
    """A function that simulates a slow process by sleeping for 2 seconds."""
    time.sleep(2)
    print("Function complete")

# Calling the function to test the decorator
print("Calling slow_function...")
slow_function()
