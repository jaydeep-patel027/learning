# Task: Create a decorator log_methods that logs the entry and exit of every method call within a class.
import functools

def log_methods(cls):
    """
    A class decorator that wraps every callable method in the class 
    to log its entry and exit.
    """
    # Iterate over all attributes of the class
    for attr_name, attr_value in vars(cls).items():
        # Check if the attribute is a callable (a method)
        if callable(attr_value):
            # Define the wrapper function to log the calls
            @functools.wraps(attr_value)
            def wrapper(*args, **kwargs):
                print(f"--> Entering {cls.__name__}.{attr_name}()")
                result = attr_value(*args, **kwargs)
                print(f"<-- Exiting {cls.__name__}.{attr_name}()")
                return result
            
            # Replace the original method with the wrapped one
            setattr(cls, attr_name, wrapper)
    return cls

# Testing the class decorator
@log_methods
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

# Instantiating the class and calling methods to see logs
calc = Calculator()
calc.add(5, 3)
calc.subtract(10, 4)
