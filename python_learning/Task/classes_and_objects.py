# Challenge: Classes and Objects
# 1. Define a class Car with attributes make, model, and year.
class Car:
    def __init__(self, make, model, year):
        # Initialize attributes
        self.make = make
        self.model = model
        self.year = year

    # 3. Add a method display_info that prints out the details of the car.
    def display_info(self):
        print(f"Car Details: {self.year} {self.make} {self.model}")

# 2. Create an instance of the Car class.
my_car = Car("Toyota", "Corolla", 2020)

# Testing the method
my_car.display_info()
