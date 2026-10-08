# Challenge: Encapsulation

# 1. Modify the Car class to make the make, model, and year attributes private.
class Car:
    def __init__(self, make, model, year):
        # Private attributes are denoted by a double underscore prefix
        self.__make = make
        self.__model = model
        self.__year = year

    # 2. Add getter and setter methods to access and modify these private attributes.
    
    # Getters
    def get_make(self):
        return self.__make

    def get_model(self):
        return self.__model

    def get_year(self):
        return self.__year

    # Setters
    def set_make(self, make):
        self.__make = make

    def set_model(self, model):
        self.__model = model

    def set_year(self, year):
        # Adding some basic validation for the year
        if year > 1885: 
            self.__year = year
        else:
            print("Invalid year for a car.")

    def display_info(self):
        print(f"Car Details: {self.__year} {self.__make} {self.__model}")

# Testing Encapsulation
my_encapsulated_car = Car("Ford", "Mustang", 2021)

# Accessing via getter
print(f"Make accessed via getter: {my_encapsulated_car.get_make()}")

# Modifying via setter
my_encapsulated_car.set_year(2025)
print("Details after modification:")
my_encapsulated_car.display_info()
