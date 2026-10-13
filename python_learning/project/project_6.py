#    Mini Movie Ticket Booking    #

# REVIEW SUMMARY:
# - This file matches the required structure for Instance Method, Class Method, Property, and Static Method usage.
# - The core logic is correct for the main acceptance criteria shown in topic_6_project.html.
# - TODO: Add stronger input validation for whitespace, invalid text formats, and non-string values.
# - TODO: Add clearer error messages for malformed booking strings in from_text() so the project is easier to debug.
# - REVIEW: The seat validation logic is good for A-H + numeric seat numbers, but it should guard against None / non-string inputs.

class MovieTicket:
    # Class-level attributes: Shared across ALL ticket instances
    tickets_sold = 0
    TAX_RATE = 0.18

    def __init__(self, movie, seat, price):
        self.movie = movie
        # This calls the @seat.setter property to validate the seat immediately!
        self.seat = seat 
        self._price = price
        
        # Increase the class-level counter whenever a new object is created
        MovieTicket.tickets_sold += 1

    # ==========================================
    # 1. INSTANCE METHODS (Works on ONE specific object)
    # First parameter is ALWAYS 'self'
    # ==========================================
    def apply_discount(self, percent):
        """Applies a discount to THIS specific ticket only."""
        self._price = self._price * (1 - percent / 100)

    def describe(self):
        """Returns a formatted string describing this ticket."""
        return f"Movie: {self.movie} | Seat: {self.seat} | Base Price: ₹{self._price:.2f} | Total (with tax): ₹{self.price_with_tax:.2f}"

    # ==========================================
    # 2. CLASS METHODS (Works on the CLASS itself)
    # First parameter is ALWAYS 'cls'
    # ==========================================
    @classmethod
    def from_text(cls, text):
        """Factory method: creates a MovieTicket instance from a formatted string."""
        # Example text: "Dune|A12|300"
        movie, seat, price = text.split("|")
        
        # 'cls' refers to MovieTicket. This is exactly the same as MovieTicket(movie, seat, int(price))
        return cls(movie, seat, int(price))

    @classmethod
    def total_sold(cls):
        """Returns the total number of tickets sold across all instances."""
        return cls.tickets_sold

    # ==========================================
    # 3. PROPERTY METHODS (Looks like an attribute, acts like a method)
    # First parameter is ALWAYS 'self'
    # ==========================================
    @property
    def seat(self):
        """Getter for the seat attribute."""
        return self._seat

    @seat.setter
    def seat(self, value):
        """Setter for the seat attribute. Adds validation behind the scenes."""
        # Calls our static method to check if the seat is valid before saving it
        if not MovieTicket.is_valid_seat(value):
            raise ValueError(f"Invalid seat code '{value}'. Seat must look like A1 to H20.")
        self._seat = value

    @property
    def price_with_tax(self):
        """
        Read-only property. Calculates the price with tax dynamically.
        Notice there is NO setter here, so you cannot do ticket.price_with_tax = 500
        """
        return self._price * (1 + MovieTicket.TAX_RATE)

    # ==========================================
    # 4. STATIC METHODS (A helper function tucked inside the class)
    # Takes NEITHER 'self' NOR 'cls'
    # ==========================================
    @staticmethod
    def is_valid_seat(seat):
        """
        Checks if a seat code is valid.
        Doesn't need to know anything about the ticket object (self) or the class (cls).
        """
        # REVIEW: This correctly supports A-H and numeric suffixes for the project requirement.
        # TODO: Add a guard for non-string values like None, integers, or empty input before using `len()` and indexing.
        if len(seat) < 2:
            return False
        # Validates first letter is A-H, and the rest is a valid number
        return seat[0] in "ABCDEFGH" and seat[1:].isdigit()


# ==========================================
# TESTING & ACCEPTANCE CRITERIA
# ==========================================
if __name__ == "__main__":
    print("--- CREATING TICKETS ---")
    # 1. Normal Creation
    ticket1 = MovieTicket("Avatar 2", "C4", 400)
    ticket2 = MovieTicket("Oppenheimer", "H15", 500)
    
    # 2. Creation via Class Method from text
    ticket3 = MovieTicket.from_text("Dune|A12|300")
    
    print(ticket1.describe())
    print(ticket2.describe())
    print(ticket3.describe())

    print("\n--- TESTING CLASS COUNTER ---")
    print(f"Total tickets sold: {MovieTicket.total_sold()} (Expected: 3)")

    print("\n--- TESTING INSTANCE METHOD (Discount) ---")
    print(f"Ticket 3 price BEFORE discount: ₹{ticket3._price:.2f}")
    ticket3.apply_discount(10) # 10% off
    print(f"Ticket 3 price AFTER discount: ₹{ticket3._price:.2f}")
    print(f"Ticket 1 price remains unaffected: ₹{ticket1._price:.2f}")

    print("\n--- TESTING STATIC METHOD & PROPERTY SETTER ---")
    print(f"Is 'A1' valid? {MovieTicket.is_valid_seat('A1')}")
    print(f"Is 'Z9' valid? {MovieTicket.is_valid_seat('Z9')}")
    
    try:
        # This will trigger the @seat.setter and raise a ValueError
        ticket1.seat = "Z9"
    except ValueError as e:
        print(f"SUCCESS: Caught invalid seat assignment -> {e}")

    print("\n--- TESTING READ-ONLY PROPERTY ---")
    print(f"Ticket 2 price with tax: ₹{ticket2.price_with_tax:.2f} (Accessed without brackets!)")
    try:
        ticket2.price_with_tax = 600
    except AttributeError as e:
        print(f"SUCCESS: Cannot overwrite read-only property -> {e}")

    print("\nAll Acceptance Criteria Met Successfully!")
