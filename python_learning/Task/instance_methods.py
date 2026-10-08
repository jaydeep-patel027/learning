# Challenge: Instance Methods

# 1. Define a class Book with attributes title and author.
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    # 2. Create an instance method display_info that prints the book's title and author.
    # Note: It takes 'self' as the first parameter.
    def display_info(self):
        print(f"Book Title: '{self.title}' by {self.author}")

# 3. Instantiate the Book class and call the display_info method.
my_book = Book("The Great Gatsby", "F. Scott Fitzgerald")
my_book.display_info()
