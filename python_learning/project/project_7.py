import os

FILE = "expenses.txt"  # File name where all daily expenses are stored

# TODO: Make `FILE` configurable (env var, CLI arg, or config file) so tests
# TODO: and production don't accidentally write to the same path.
# TODO: Consider using `pathlib.Path` and `os.path.expanduser` for robust paths.
# TODO: Consider adding an explicit `encoding="utf-8"` when opening files to
# TODO: avoid platform-specific defaults.


# 1. Function to add a new expense at the end of the file
def add_expense(item, amount):
    # "a" (append) mode keeps old lines intact and writes the new line at the end
    # `with` automatically closes the file once writing is done
    with open(FILE, "a") as f:
        f.write(f"{item},{amount}\n")

    # TODO: Add input validation for `amount` (ensure numeric) or clearly
    # TODO: document that `amount` may be any string (tests rely on damaged
    # TODO: lines). Prefer storing a normalized numeric format (e.g. float or
    # TODO: Decimal) to avoid parsing issues later.
    # TODO: Catch and handle `PermissionError` and `OSError` here so callers get
    # TODO: a clear error/return value instead of a crash.
    # TODO: Consider returning a boolean or raising a well-documented exception
    # TODO: instead of silently returning None.


# 2. Function to read and print every expense line from the file
def show_all():
    try:
        # "r" (read) mode opens the file for reading only
        with open(FILE, "r") as f:
            for line in f:
                print(line.strip())
    except FileNotFoundError:
        # Runs if expenses.txt does not exist yet, preventing a crash
        print("No expense file yet.")
    except PermissionError:
        # Runs if the file is locked or read-only
        print("Cannot open the file. Close it and try again.")

    # TODO: `show_all()` prints directly. For better testability and separation
    # TODO: of concerns, consider returning a list of records and let the caller
    # TODO: decide how to display them. Also prefer `logging` over `print`.
    # TODO: Add `encoding="utf-8"` and a small docstring describing the format.


# 3 & 4. Function to calculate the total amount spent and skip damaged lines
def total_spent():
    total = 0
    bad_lines = 0

    # Outer try: protects opening and reading the whole file
    try:
        with open(FILE, "r") as f:
            for line in f:
                # Inner try: checks one line at a time so a bad line doesn't stop the loop
                try:
                    item, amount = line.strip().split(
                        ","
                    )  # Split "item,amount" into two parts
                    total += float(amount)  # Convert amount text to a number and add
                except ValueError:
                    bad_lines += (
                        1  # Damaged line (e.g., "Lunch,abc"): skip it and count it
                    )
    except FileNotFoundError:
        # TODO: Instead of printing here, consider returning 0 and logging the
        # TODO: missing file. Printing inside a utility makes it harder to test.
        print("No expense file yet. Total is 0.")
    except PermissionError:
        # TODO: Consider re-raising a custom exception or returning `None` so
        # TODO: callers can detect error states separately from a valid total.
        print("Cannot open the file. Close it and try again.")

    if bad_lines:
        print(f"Skipped {bad_lines} damaged line(s).")
    return total


# 5. Function to empty the entire file
def clear_all():
    # DANGER: "w" (write) mode immediately ERASES all existing data in the file!
    with open(FILE, "w") as f:
        pass

    # TODO: This is destructive. Add a safety step (backup, confirm, or move to
    # TODO: a temporary file) before truncating in production code.
    # TODO: Catch and handle `PermissionError` and `OSError` here.


# ==========================================================
# 6. Testing the Program (Step-by-Step)
# ==========================================================
if __name__ == "__main__":
    # Remove any old file first so we can test the "no file yet" case
    if os.path.exists(FILE):
        os.remove(FILE)

    print("--- Test 1: No file yet ---")
    print("Total:", total_spent())

    print("\n--- Test 2: File with a bad line ---")
    add_expense("Tea", 20)
    # TODO: The next line intentionally writes a bad value ("abc") so the
    # TODO: `total_spent()` skip-path gets exercised. In real code, avoid
    # TODO: inserting invalid data; instead validate before writing.
    add_expense("Lunch", "abc")  # Damaged line: triggers ValueError and gets skipped
    add_expense("Bus", 35)
    show_all()
    print("Total:", total_spent())

    print("\n--- Test 3: Clear file & test normal file (3 expenses) ---")
    # TODO: Tests currently operate on the real `FILE` in the working
    # TODO: directory. Prefer using `tempfile.TemporaryDirectory()` or a test
    # TODO: fixture so unit tests do not delete user data.
    clear_all()  # Erases the old test data using "w" mode
    add_expense("Tea", 20)
    add_expense("Bus", 35)
    add_expense("Snacks", 80)
    show_all()
    print("Final Total:", total_spent())
