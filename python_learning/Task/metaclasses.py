# Task: Create a metaclass SingletonMeta that ensures only one instance of a class can be created.

class SingletonMeta(type):
    """
    A metaclass that implements the Singleton pattern.
    It keeps track of instances and returns the existing one if it's already created.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # If the class doesn't have an instance yet, create one
        if cls not in cls._instances:
            # Call the superclass to create the instance and store it
            cls._instances[cls] = super().__call__(*args, **kwargs)
        # Return the stored instance
        return cls._instances[cls]

# Testing the SingletonMeta
class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self):
        self.connection_string = "Connected to DB"
        print("Initializing DatabaseConnection...")

# Attempting to create multiple instances
db1 = DatabaseConnection()
db2 = DatabaseConnection()
db3 = DatabaseConnection()

print(f"db1 is db2: {db1 is db2}") # Should be True
print(f"db2 is db3: {db2 is db3}") # Should be True
