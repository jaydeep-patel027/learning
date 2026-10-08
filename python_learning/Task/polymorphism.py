# Challenge: Polymorphism

# Base class with the start_engine method added
class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    # 2. Add a method start_engine to the Car class that prints "Car engine started".
    def start_engine(self):
        print("Car engine started")

# 1. Define a class Bike with a method start_engine that prints "Bike engine started".
class Bike:
    def __init__(self, type):
        self.type = type

    def start_engine(self):
        print("Bike engine started")

# 3. Write a function start_vehicle that takes a vehicle object and calls its start_engine method.
def start_vehicle(vehicle):
    # This demonstrates polymorphism; it calls start_engine regardless of the object's specific class
    vehicle.start_engine()

# Testing polymorphism
my_car = Car("Honda", "Civic", 2022)
my_bike = Bike("Mountain Bike")

print("Starting vehicles:")
start_vehicle(my_car)
start_vehicle(my_bike)
