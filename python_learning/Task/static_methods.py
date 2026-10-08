# Challenge: Static Methods

class MathUtils:
    # 1. Define a class MathUtils with a static method add_numbers that takes two numbers and returns their sum.
    # Note: It doesn't take 'self' or 'cls' and uses the @staticmethod decorator.
    @staticmethod
    def add_numbers(num1, num2):
        return num1 + num2

# 2. Call the static method without creating an instance of the class.
result = MathUtils.add_numbers(15, 30)

print(f"The sum of the numbers is: {result}")
