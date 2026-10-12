class BankAccount:
    # 1. Classes and Objects: This is the blueprint
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance  # Encapsulation: __ makes the balance private

    def deposit(self, amount):
        # Validation protects against bad data
        if amount <= 0:
            raise ValueError(f"Amount must be positive. Attempted: ₹{amount}")
        self.__balance += amount
        print(f"Success: Deposited ₹{amount} to {self.owner}'s account.")

    def withdraw(self, amount):
        # Validation protects against overdrafting
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.__balance:
            raise ValueError(f"Failed: Insufficient funds for {self.owner}. Balance: ₹{self.__balance}")
        self.__balance -= amount
        print(f"Success: Withdrew ₹{amount} from {self.owner}'s account.")

    def get_balance(self):
        return self.__balance

    def _change(self, amount):
        # Protected method: Child classes use this to safely modify the balance
        self.__balance += amount

    def month_end(self):
        # Basic account does nothing at month end
        pass


# 2. Inheritance: SavingsAccount gets everything from BankAccount
class SavingsAccount(BankAccount):
    def __init__(self, owner, balance=0, rate=0.04):
        super().__init__(owner, balance)  # Calls the parent's __init__
        self.rate = rate

    def month_end(self):
        # 3. Polymorphism: Savings version of month_end
        interest = self.get_balance() * self.rate / 12
        self._change(interest)
        print(f"-> {self.owner}'s Savings Account earned ₹{interest:.2f} in interest.")


# Inheritance: CurrentAccount gets everything from BankAccount
class CurrentAccount(BankAccount):
    def month_end(self):
        # Polymorphism: Current version of month_end
        self._change(-50)
        print(f"-> {self.owner}'s Current Account was charged a ₹50.00 monthly fee.")



if __name__ == "__main__":
    print("--- 1. BUILDING OBJECTS & TESTING ENCAPSULATION ---")
    # Creating an object
    riya = SavingsAccount("Riya", 10000)
    
    # Testing valid deposit and withdraw
    riya.deposit(500)
    riya.withdraw(200)

    # Testing Encapsulation protections
    try:
        print("\nAttempting invalid deposit (Negative amount)...")
        riya.deposit(-1000)
    except ValueError as e:
        print(f"BLOCKED by Encapsulation: {e}")

    try:
        print("\nAttempting invalid withdrawal (Too much money)...")
        riya.withdraw(999999)
    except ValueError as e:
        print(f"BLOCKED by Encapsulation: {e}")

    print("\n--- 2. RUNNING MONTH-END PROCESS (SET 1) ---")
    # Creating a list of different account types
    accounts_set_1 = [
        SavingsAccount("Riya", 10000),
        CurrentAccount("Arjun", 5000),
        SavingsAccount("Meera", 2500),
        BankAccount("Kabir", 3000)
    ]

    # One simple loop demonstrating Polymorphism
    for acc in accounts_set_1:
        acc.month_end()

    print("\n--- SET 1 BALANCES AFTER MONTH END ---")
    print(f"{'Owner':<10} | {'Type':<15} | {'Balance (₹)'}")
    print("-" * 45)
    for acc in accounts_set_1:
        print(f"{acc.owner:<10} | {type(acc).__name__:<15} | ₹{acc.get_balance():.2f}")


    print("\n--- 3. RUNNING MONTH-END PROCESS (SET 2) ---")
    # Second set of accounts as required by Acceptance Criteria
    accounts_set_2 = [
        CurrentAccount("Business Corp", 50000),
        BankAccount("Student Basic", 500),
        SavingsAccount("Grandma Nest", 200000, rate=0.06) # Higher rate
    ]

    for acc in accounts_set_2:
        acc.month_end()

    print("\n--- SET 2 BALANCES AFTER MONTH END ---")
    print(f"{'Owner':<15} | {'Type':<15} | {'Balance (₹)'}")
    print("-" * 50)
    for acc in accounts_set_2:
        print(f"{acc.owner:<15} | {type(acc).__name__:<15} | ₹{acc.get_balance():.2f}")
