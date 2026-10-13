

"""
MODULE DOCSTRING (Added for better explanation):
Timing of Python Concepts Demonstrated:
1. METACLASS (ProductMeta): Executes at CLASS DEFINITION time.
2. DECORATOR (require_stock): Executes at METHOD CALL time.
3. ABSTRACT BASE CLASS (ABC): Executes at OBJECT CREATION time.
"""

from abc import abstractmethod, ABCMeta


# ==========================================
# 1. METACLASS (Runs at Class DEFINITION Time)
# ==========================================
class ProductMeta(ABCMeta):
   
    
    registry = {}

    def __new__(mcs, name, bases, namespace):
     
        
        cls = super().__new__(mcs, name, bases, namespace)

        if bases:
            if "category" not in namespace:
                # Improved Error Message as per TODO
                raise TypeError(
                    f"Fatal Error: Class '{name}' must define a 'category' attribute. "
                    "Developer Contract: every concrete product class must define category."
                )

            mcs.registry[name] = cls

        return cls


# ==========================================
# 2. DECORATOR (Runs at Method CALL Time)
# ==========================================
def require_stock(func):
    """Decorator to enforce stock validation before proceeding with a purchase."""

    
    def wrapper(self, *args, **kwargs):
        if self.stock <= 0:
            raise ValueError(
                f"Purchase Blocked: '{self.name}' is completely out of stock!"
            )

        print(
            f"[STORE LOG] Security check passed. Processing purchase for '{self.name}'..."
        )

        return func(self, *args, **kwargs)

    return wrapper


# ==========================================
# 3. ABSTRACT BASE CLASS (Runs at Object CREATION Time)
# ==========================================
class Product(metaclass=ProductMeta):
    """
    Abstract Base Class representing a generic store product.
    
    Why it cannot be instantiated: 
    This class inherits from ABCMeta and contains an abstract method `shipping_cost`. 
    Therefore, Python prevents direct instantiation of `Product`.
    
    What child classes must implement:
    Every child class must implement the `shipping_cost(self)` method and must 
    define a `category` class attribute (enforced by ProductMeta).
    """

    
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    @abstractmethod
    def shipping_cost(self):
        pass

    @require_stock
    def purchase(self):

        
        self.stock -= 1
        total_cost = self.price + self.shipping_cost()
        return total_cost


# ==========================================
# 4. CONCRETE PRODUCT CLASSES
# ==========================================
class Book(Product):

    
    category = "book"

    def shipping_cost(self):
        return 40


class Electronics(Product):

    category = "electronics"

    def shipping_cost(self):
        return 150


# ==========================================
# 5. TESTING & ACCEPTANCE CRITERIA
# ==========================================
if __name__ == "__main__":

    
    print("--- 1. METACLASS REGISTRY TEST ---")
    assert "Book" in ProductMeta.registry, "Book should be in registry"
    assert "Electronics" in ProductMeta.registry, "Electronics should be in registry"
    print(f"Registered Products: {list(ProductMeta.registry.keys())} -> ASSERT PASSED")

    print("\n--- 2. METACLASS DEFINITION ERROR TEST ---")
    try:
        class Toy(Product):
            def shipping_cost(self):
                return 30
        assert False, "TypeError was not raised for missing 'category' attribute!"
    except TypeError as e:
        assert "every concrete product class must define category" in str(e).lower()
        print(f"Metaclass successfully blocked bad class definition: {e} -> ASSERT PASSED")

    print("\n--- 3. ABSTRACT BASE CLASS CREATION TEST ---")
    try:
        generic_product = Product("Generic Box", 100, 5)
        assert False, "TypeError was not raised for generic Product instantiation!"
    except TypeError as e:
        assert "Can't instantiate abstract class" in str(e)
        print(f"ABC successfully blocked generic Product creation: {e} -> ASSERT PASSED")

    try:
        class Magazine(Product):
            category = "magazine"
            # Missing shipping_cost method

        my_mag = Magazine("Tech Monthly", 50, 10)
        assert False, "TypeError was not raised for incomplete child creation!"
    except TypeError as e:
        assert "abstract method" in str(e).lower()
        print(f"ABC successfully blocked incomplete child creation: {e} -> ASSERT PASSED")

    print("\n--- 4. DECORATOR GUARD & PURCHASE LOOP TEST ---")
    my_book = Book("Dune", 500, stock=2)
    my_laptop = Electronics("Dell XPS", 85000, stock=1)

    print(f"Initial '{my_book.name}' stock: {my_book.stock}")

    # Buy twice to exhaust stock
    cost1 = my_book.purchase()
    assert cost1 == 540, "Incorrect total cost calculation for Book"
    cost2 = my_book.purchase()
    assert cost2 == 540
    assert my_book.stock == 0, "Stock should be 0 after 2 purchases"

    # 3rd purchase should raise ValueError due to decorator
    try:
        my_book.purchase()
        assert False, "ValueError was not raised for out-of-stock item!"
    except ValueError as e:
        assert "completely out of stock" in str(e).lower()
        print(f"Decorator successfully blocked purchase: {e} -> ASSERT PASSED")

    print(f"\nBuying the laptop...")
    laptop_cost = my_laptop.purchase()
    assert laptop_cost == 85150, "Incorrect total cost calculation for Electronics"
    print(f"Total cost: ₹{laptop_cost} -> ASSERT PASSED")
    print("\nAll assert-based tests completed successfully!")
