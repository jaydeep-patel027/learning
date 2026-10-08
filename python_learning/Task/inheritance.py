# Challenge: Inheritance
# Base class from previous challenge
class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def display_info(self):
        print(f"Car Details: {self.year} {self.make} {self.model}")

# 1. Define a class ElectricCar that inherits from the Car class.
class ElectricCar(Car):
    def __init__(self, make, model, year, battery_size):
        # Initialize attributes of the parent class
        super().__init__(make, model, year)
        # 2. Add an attribute battery_size to the ElectricCar class.
        self.battery_size = battery_size

    # 3. Override the display_info method to include battery size.
    def display_info(self):
        print(f"Electric Car Details: {self.year} {self.make} {self.model} with a {self.battery_size} kWh battery.")

# Testing the ElectricCar class
my_ev = ElectricCar("Tesla", "Model S", 2023, 100)
my_ev.display_info()
