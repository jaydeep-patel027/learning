# Challenge: Property Methods

# 1. Define a class Person with a private attribute _age.
class Person:
    def __init__(self, name):
        self.name = name
        self._age = 0  # Private attribute

    # 2. Create a property method age with a getter and setter to access and modify the _age attribute.
    
    # Getter method using @property
    @property
    def age(self):
        return self._age

    # Setter method using @<property_name>.setter
    @age.setter
    def age(self, value):
        # Adding some validation logic in the setter
        if value >= 0:
            self._age = value
        else:
            print("Age cannot be negative.")

# 3. Instantiate the Person class, set the age, and print it.
person = Person("Alice")

# Setting the age using the property setter (looks like standard attribute assignment)
person.age = 28

# Getting the age using the property getter (looks like standard attribute access)
print(f"{person.name} is {person.age} years old.")

# Trying to set an invalid age
person.age = -5
