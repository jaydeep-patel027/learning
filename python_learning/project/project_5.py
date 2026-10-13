# SENIOR REVIEW: The project matches the required topic well. Keep the original junior comments and logic as-is.
# TODO: Continue improving explanation in comments so future readers can clearly understand the timing of each Python concept.
# REVIEW: Metaclass validates class creation, decorator validates method call, and ABC prevents invalid object creation.

from abc import abstractmethod, ABCMeta

# REVIEW: Good overall structure for the project. The implementation covers the three required concepts in a single example: metaclass registration, decorator-based stock guard, and abstract base class enforcement.
# TODO: Keep this pattern as a learning example, but add clearer comments/docstrings so future readers understand the timing of each mechanism: metaclass at class definition time, decorator at method call time, and ABC at object creation time.
# REVIEW: This project aligns with the topic requirements from the HTML brief: automatic registry, category check, stock guard, and abstract shipping_cost rule.


# ==========================================
# 1. METACLASS (Runs at Class DEFINITION Time)
# ==========================================
class ProductMeta(ABCMeta):
    # REVIEW: The registry mechanism is appropriate and the automatic registration approach is a strong design decision.
    # TODO: Consider adding a clearer error message for the developer-facing contract: "every concrete product class must define category".
    registry = {}

    def __new__(mcs, name, bases, namespace):
        # REVIEW: Using __new__ to validate the class definition is the correct metaclass pattern.
        # TODO: This is a good place to also validate naming or other product rules if the project grows later.
        cls = super().__new__(mcs, name, bases, namespace)

        if bases:
            if "category" not in namespace:
                raise TypeError(
                    f"Fatal Error: Class '{name}' must define a 'category' attribute."
                )

            mcs.registry[name] = cls

        return cls


# ==========================================
# 2. DECORATOR (Runs at Method CALL Time)
# ==========================================
def require_stock(func):
    # REVIEW: The decorator correctly centralizes the stock check, which matches the learning objective and keeps purchase logic reusable.
    # TODO: Keep the decorator as the sole place for stock validation; avoid moving this logic into child purchase methods later.
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
    # REVIEW: Declaring Product as an abstract base is correct because the shipping_cost behavior is required for all product implementations.
    # TODO: Optional improvement: add a docstring explaining why Product cannot be instantiated and what each child must implement.
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    @abstractmethod
    def shipping_cost(self):
        pass

    @require_stock
    def purchase(self):
        # REVIEW: This method has no stock check or print logic, which is exactly what the decorator is meant to handle.
        # TODO: This is a good example of separation of concerns; keep it this way in future exercises.
        self.stock -= 1
        total_cost = self.price + self.shipping_cost()
        return total_cost


# ==========================================
# 4. CONCRETE PRODUCT CLASSES
# ==========================================
class Book(Product):
    # REVIEW: Book is a valid concrete child class and implements the required shipping_cost method.
    # TODO: Good example; no change needed here.
    category = "book"

    def shipping_cost(self):
        return 40


class Electronics(Product):
    # REVIEW: Electronics also follows the required pattern and is registered automatically through the metaclass.
    category = "electronics"

    def shipping_cost(self):
        return 150


# ==========================================
# 5. TESTING & ACCEPTANCE CRITERIA
# ==========================================
if __name__ == "__main__":
    # REVIEW: The test flow covers all key acceptance rules: registry output, invalid class definition, abstract class prevention, missing method prevention, and stock exhaustion.
    # TODO: Consider converting these prints into assert-based tests for cleaner quality checks and easier grading.
    print("--- 1. METACLASS REGISTRY TEST ---")
    print(f"Registered Products: {list(ProductMeta.registry.keys())}")

    print("\n--- 2. METACLASS DEFINITION ERROR TEST ---")
    try:

        class Toy(Product):
            def shipping_cost(self):
                return 30

    except TypeError as e:
        print(f"Metaclass successfully blocked bad class definition: {e}")

    print("\n--- 3. ABSTRACT BASE CLASS CREATION TEST ---")
    try:
        generic_product = Product("Generic Box", 100, 5)
    except TypeError as e:
        print(f"ABC successfully blocked generic Product creation: {e}")

    try:

        class Magazine(Product):
            category = "magazine"

        my_mag = Magazine("Tech Monthly", 50, 10)
    except TypeError as e:
        print(f"ABC successfully blocked incomplete child creation: {e}")

    print("\n--- 4. DECORATOR GUARD & PURCHASE LOOP TEST ---")
    my_book = Book("Dune", 500, stock=2)
    my_laptop = Electronics("Dell XPS", 85000, stock=1)

    print(f"Initial '{my_book.name}' stock: {my_book.stock}")

    try:
        print(f"Total cost: ₹{my_book.purchase()}")
        print(f"Total cost: ₹{my_book.purchase()}")
        print(f"Total cost: ₹{my_book.purchase()}")
    except ValueError as e:
        print(f"Decorator successfully blocked purchase: {e}")

    print(f"\nBuying the laptop...")
    print(f"Total cost: ₹{my_laptop.purchase()}")
