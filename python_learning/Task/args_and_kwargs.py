# Challenge 1: Define a function sum_all that takes any number of arguments and returns their sum using *args.
def sum_all(*args):
    """Calculates the sum of all provided positional arguments."""
    return sum(args)

# Testing the sum_all function
total_sum = sum_all(1, 2, 3, 4, 5)
print("Sum of all arguments using *args:", total_sum)

# Challenge 2: Define a function print_info that takes any number of keyword arguments and prints them using **kwargs.
def print_info(**kwargs):
    """Prints all provided keyword arguments in a readable format."""
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# Testing the print_info function
print("\nInformation printed using **kwargs:")
print_info(name="John Doe", age=30, occupation="Software Engineer")
