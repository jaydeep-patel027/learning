# Task: Create an abstract base class Shape with abstract methods area() and perimeter(), 
# and implement concrete subclasses Circle and Rectangle.
from abc import ABC, abstractmethod
import math

# Define the Abstract Base Class
class Shape(ABC):
    @abstractmethod
    def area(self):
        """Abstract method to calculate area"""
        pass

    @abstractmethod
    def perimeter(self):
        """Abstract method to calculate perimeter"""
        pass

# Concrete subclass 1: Circle
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * (self.radius ** 2)

    def perimeter(self):
        return 2 * math.pi * self.radius

# Concrete subclass 2: Rectangle
class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)

# Testing the abstract classes and subclasses
circle = Circle(5)
rectangle = Rectangle(4, 6)

print(f"Circle Area: {circle.area():.2f}, Perimeter: {circle.perimeter():.2f}")
print(f"Rectangle Area: {rectangle.area()}, Perimeter: {rectangle.perimeter()}")
