from abc import abstractmethod, ABCMeta

# ==========================================
# 1. METACLASS (Runs at Class DEFINITION Time)
# ==========================================
class ProductMeta(ABCMeta):
    # This dictionary automatically keeps track of every valid product type.
    registry = {}

    def __new__(mcs, name, bases, namespace):
        # Create the class using the parent's logic first
        cls = super().__new__(mcs, name, bases, namespace)
        
        # 'bases' is empty for the base Product class itself, so we skip it.
        # But for child classes (like Book), bases is not empty.
        if bases:                                  
            if "category" not in namespace:
                # If a developer forgets the category, crash the program IMMEDIATELY.
                raise TypeError(f"Fatal Error: Class '{name}' must define a 'category' attribute.")
            
            # If valid, register it automatically! No manual lists needed.
            mcs.registry[name] = cls               
            
        return cls

# ==========================================
# 2. DECORATOR (Runs at Method CALL Time)
# ==========================================
def require_stock(func):
    def wrapper(self, *args, **kwargs):
        # 1. Guard check: Is there stock?
        if self.stock <= 0:
            raise ValueError(f"Purchase Blocked: '{self.name}' is completely out of stock!")
        
        # 2. Log the purchase attempt
        print(f"[STORE LOG] Security check passed. Processing purchase for '{self.name}'...")
        
        # 3. Actually run the purchase method
        return func(self, *args, **kwargs)
    return wrapper

# ==========================================
# 3. ABSTRACT BASE CLASS (Runs at Object CREATION Time)
# ==========================================
class Product(metaclass=ProductMeta):
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    # The ABC forces every child to have this exact method.
    @abstractmethod
    def shipping_cost(self):
        pass

    # Notice: There is no print statement and no stock check in this method!
    # The decorator handles all of that.
    @require_stock
    def purchase(self):
        self.stock -= 1
        total_cost = self.price + self.shipping_cost()
        return total_cost

# ==========================================
# 4. CONCRETE PRODUCT CLASSES
# ==========================================
# The metaclass sees these being defined and adds them to the registry automatically.
class Book(Product):
    category = "book"
    
    def shipping_cost(self):
        return 40  # Flat ₹40 shipping for books

class Electronics(Product):
    category = "electronics"
    
    def shipping_cost(self):
        return 150  # Heavy boxes, ₹150 shipping


# ==========================================
# 5. TESTING & ACCEPTANCE CRITERIA
# ==========================================
if __name__ == "__main__":
    print("--- 1. METACLASS REGISTRY TEST ---")
    # Notice we didn't manually append anything, but the dictionary is populated!
    print(f"Registered Products: {list(ProductMeta.registry.keys())}")


    print("\n--- 2. METACLASS DEFINITION ERROR TEST ---")
    try:
        # We try to create a class WITHOUT a category.
        class Toy(Product):
            def shipping_cost(self): return 30
    except TypeError as e:
        print(f"Metaclass successfully blocked bad class definition: {e}")


    print("\n--- 3. ABSTRACT BASE CLASS CREATION TEST ---")
    try:
        # Trying to create an instance of the abstract parent
        generic_product = Product("Generic Box", 100, 5)
    except TypeError as e:
        print(f"ABC successfully blocked generic Product creation: {e}")

    try:
        # Trying to create an object of a class that forgot shipping_cost()
        class Magazine(Product):
            category = "magazine"
            # Developer forgot to write def shipping_cost(self): ...
            
        my_mag = Magazine("Tech Monthly", 50, 10)
    except TypeError as e:
        print(f"ABC successfully blocked incomplete child creation: {e}")


    print("\n--- 4. DECORATOR GUARD & PURCHASE LOOP TEST ---")
    # Create valid objects
    my_book = Book("Dune", 500, stock=2)
    my_laptop = Electronics("Dell XPS", 85000, stock=1)

    print(f"Initial '{my_book.name}' stock: {my_book.stock}")
    
    # Buy until stock runs out
    try:
        print(f"Total cost: ₹{my_book.purchase()}")
        print(f"Total cost: ₹{my_book.purchase()}")
        
        # This 3rd purchase will trigger the decorator's ValueError
        print(f"Total cost: ₹{my_book.purchase()}") 
    except ValueError as e:
        print(f"Decorator successfully blocked purchase: {e}")

    print(f"\nBuying the laptop...")
    print(f"Total cost: ₹{my_laptop.purchase()}")