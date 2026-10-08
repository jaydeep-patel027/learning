# Challenge: Class Methods

# 1. Define a class Library with a class attribute total_books.
class Library:
    total_books = 0  # Class attribute

    def __init__(self, name):
        self.name = name

    # 2. Create a class method update_total_books that updates the total_books attribute.
    # Note: It takes 'cls' as the first parameter and uses the @classmethod decorator.
    @classmethod
    def update_total_books(cls, amount):
        cls.total_books += amount
        print(f"Total books updated. Current count: {cls.total_books}")

# 3. Call the class method to modify the class attribute.
# We can call it directly on the class without creating an instance.
print(f"Initial total books: {Library.total_books}")

Library.update_total_books(10)
Library.update_total_books(25)

# Checking the class attribute again
print(f"Final total books: {Library.total_books}")
