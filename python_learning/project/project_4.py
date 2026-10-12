class BankAccount:
    """
    Blueprint for a bank account demonstrating Encapsulation.
    Manages core operations like deposits, withdrawals, and balance tracking.
    """
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._validate_amount(balance, allow_zero=True)
        self.__balance = float(balance)  # Encapsulation: __ makes the balance private

    def _validate_amount(self, amount, allow_zero=False):
        """Helper method to validate if the amount is a valid numeric value."""
        # Check for non-numeric types (blocks strings, None, and booleans)
        if type(amount) not in (int, float):
            raise TypeError(f"Invalid input type: {type(amount).__name__}. Amount must be a number.")
        
        # Check for zero or negative values
        if amount < 0 or (amount == 0 and not allow_zero):
            raise ValueError(f"Amount must be greater than zero. Attempted: {amount}")

    def deposit(self, amount):
        """Deposits a valid numeric amount into the account."""
        self._validate_amount(amount)
        self.__balance += float(amount)

    def withdraw(self, amount):
        """Withdraws a valid amount if sufficient funds exist."""
        self._validate_amount(amount)
        if amount > self.__balance:
            raise ValueError(f"Insufficient funds for {self.owner}. Balance: ₹{self.__balance}")
        self.__balance -= float(amount)

    def get_balance(self):
        """Returns the current balance securely."""
        return self.__balance

    def _change(self, amount):
        """Protected method: Child classes use this to safely modify the balance."""
        self.__balance += float(amount)

    def month_end(self):
        """Base month-end logic. Basic accounts do not earn interest or pay fees."""
        return 0.0


class SavingsAccount(BankAccount):
    """
    SavingsAccount inherits from BankAccount.
    Earns monthly interest.
    """
    def __init__(self, owner, balance=0, rate=0.04):
        super().__init__(owner, balance)  # Calls the parent's __init__
        self.rate = rate

    def month_end(self):
        """Polymorphism: Calculates and adds monthly interest, returning the interest amount."""
        interest = self.get_balance() * self.rate / 12
        self._change(interest)
        return interest


class CurrentAccount(BankAccount):
    """
    CurrentAccount inherits from BankAccount.
    Charges a flat monthly maintenance fee.
    """
    def month_end(self):
        """Polymorphism: Charges a monthly fee, returning the fee amount."""
        fee = -50.0
        self._change(fee)
        return fee


if __name__ == "__main__":
    print("--- 1. BUILDING OBJECTS & TESTING ENCAPSULATION ---")
    riya = SavingsAccount("Riya", 10000)
    
    # Testing valid deposit and withdraw (Printing is now outside the business logic)
    riya.deposit(500)
    print(f"Success: Deposited ₹500. New balance: ₹{riya.get_balance()}")
    
    riya.withdraw(200)
    print(f"Success: Withdrew ₹200. New balance: ₹{riya.get_balance()}")


    print("\n--- 2. TESTING NON-NUMERIC VALIDATION ---")
    for bad_input in ["500", None, [100]]:
        try:
            riya.deposit(bad_input)
        except TypeError as e:
            print(f"BLOCKED by Type Validation: {e}")


    print("\n--- 3. TESTING EDGE CASES ---")
    # Test: deposit(0) and deposit(-10)
    for amount in [0, -10]:
        try:
            riya.deposit(amount)
        except ValueError as e:
            print(f"BLOCKED Deposit ({amount}): {e}")

    # Test: withdraw(0) and withdraw(-10)
    for amount in [0, -10]:
        try:
            riya.withdraw(amount)
        except ValueError as e:
            print(f"BLOCKED Withdraw ({amount}): {e}")

    # Test: withdrawing exactly the full balance
    exact_balance = riya.get_balance()
    riya.withdraw(exact_balance)
    print(f"Success: Withdrew exact full balance (₹{exact_balance}). New balance: ₹{riya.get_balance()}")

    # Test: month_end() for a basic BankAccount
    basic_acc = BankAccount("TestUser", 100)
    bal_before = basic_acc.get_balance()
    basic_acc.month_end()
    bal_after = basic_acc.get_balance()
    print(f"Basic Account month_end check -> Unchanged: {bal_before == bal_after} (Balance remains ₹{bal_after})")


    print("\n--- 4. RUNNING MONTH-END PROCESS (SET 1) ---")
    accounts_set_1 = [
        SavingsAccount("Riya", 10000),
        CurrentAccount("Arjun", 5000),
        SavingsAccount("Meera", 2500),
        BankAccount("Kabir", 3000)
    ]
    
    # Process month-end and handle printing based on returned values
    for acc in accounts_set_1:
        change = acc.month_end()
        if change > 0:
            print(f"-> {acc.owner}'s {type(acc).__name__} earned ₹{change:.2f} in interest.")
        elif change < 0:
            print(f"-> {acc.owner}'s {type(acc).__name__} was charged a ₹{abs(change):.2f} monthly fee.")

    print("\n--- SET 1 BALANCES AFTER MONTH END ---")
    print(f"{'Owner':<10} | {'Type':<15} | {'Balance (₹)'}")
    print("-" * 45)
    for acc in accounts_set_1:
        print(f"{acc.owner:<10} | {type(acc).__name__:<15} | ₹{acc.get_balance():.2f}")


    print("\n--- 5. RUNNING MONTH-END PROCESS (SET 2) ---")
    accounts_set_2 = [
        CurrentAccount("Business Corp", 50000),
        BankAccount("Student Basic", 500),
        SavingsAccount("Grandma Nest", 200000, rate=0.06)
    ]
    
    for acc in accounts_set_2:
        acc.month_end()
        
    print("\n--- SET 2 BALANCES AFTER MONTH END ---")
    print(f"{'Owner':<15} | {'Type':<15} | {'Balance (₹)'}")
    print("-" * 50)
    for acc in accounts_set_2:
        print(f"{acc.owner:<15} | {type(acc).__name__:<15} | ₹{acc.get_balance():.2f}")
