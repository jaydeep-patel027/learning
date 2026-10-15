import logging
import os
import shutil
import tempfile
from pathlib import Path
from typing import List, Optional

# Configure basic logging instead of relying on print statements inside functions
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Configurable file path via environment variable, expanded and resolved with pathlib
DEFAULT_FILE = Path(
    os.path.expanduser(os.getenv("EXPENSES_FILE", "expenses.txt"))
)


# 1. Function to add a new expense at the end of the file
def add_expense(
    item: str, amount: float | int | str, file_path: Path = DEFAULT_FILE
) -> bool:
    """Validates and appends a normalized expense record ('item,amount') to the file.

    Returns True on success, False if validation or file I/O fails.
    """
    try:
        normalized_amount = float(amount)
    except (ValueError, TypeError):
        logging.error(
            f"Invalid amount '{amount}' for item '{item}'. Amount must be numeric."
        )
        return False

    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"{item},{normalized_amount:.2f}\n")
        return True
    except PermissionError:
        logging.error(
            f"Permission denied: Cannot write to '{file_path}'. Close it and try again."
        )
        return False
    except OSError as e:
        logging.error(f"OS error while writing to '{file_path}': {e}")
        return False


# 2. Function to read and return every expense line from the file
def show_all(file_path: Path = DEFAULT_FILE) -> List[str]:
    """Reads all expense lines from the file (format: 'item,amount') and returns them as a list."""
    records: List[str] = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                cleaned = line.strip()
                if cleaned:
                    records.append(cleaned)
    except FileNotFoundError:
        logging.info(f"No expense file found at '{file_path}'.")
    except PermissionError:
        logging.error(
            f"Cannot open '{file_path}'. Close it and try again."
        )
    except OSError as e:
        logging.error(f"OS error while reading '{file_path}': {e}")

    return records


# 3 & 4. Function to calculate the total amount spent and skip damaged lines
def total_spent(file_path: Path = DEFAULT_FILE) -> Optional[float]:
    """Calculates and returns the total amount spent across all valid records.

    Returns 0.0 if the file does not exist, or None if a permission/OS error occurs.
    """
    total = 0.0
    bad_lines = 0

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    # Split "item,amount" into two parts (from the right in case item name has commas)
                    item, amount = line.strip().rsplit(",", 1)
                    total += float(amount)
                except ValueError:
                    bad_lines += 1
    except FileNotFoundError:
        logging.info(f"No expense file yet at '{file_path}'. Total is 0.0.")
        return 0.0
    except PermissionError:
        logging.error(
            f"Cannot open '{file_path}'. Close it and try again."
        )
        return None
    except OSError as e:
        logging.error(f"OS error while reading '{file_path}': {e}")
        return None

    if bad_lines:
        logging.warning(f"Skipped {bad_lines} damaged line(s).")
    return total


# 5. Function to empty the entire file safely
def clear_all(
    file_path: Path = DEFAULT_FILE, create_backup: bool = True
) -> bool:
    """Safely empties the expense file. Creates a '.bak' backup first if create_backup is True."""
    try:
        if create_backup and file_path.exists():
            backup_path = file_path.with_suffix(file_path.suffix + ".bak")
            shutil.copy2(file_path, backup_path)
            logging.info(f"Backup created at '{backup_path}'.")

        with open(file_path, "w", encoding="utf-8") as f:
            pass
        return True
    except PermissionError:
        logging.error(
            f"Permission denied: Cannot clear '{file_path}'. Close it and try again."
        )
        return False
    except OSError as e:
        logging.error(f"OS error while clearing '{file_path}': {e}")
        return False


# ==========================================================
# 6. Testing the Program (Step-by-Step in a Temporary Directory)
# ==========================================================
if __name__ == "__main__":
    # Using TemporaryDirectory so tests never delete or overwrite real user data
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_file = Path(tmp_dir) / "test_expenses.txt"

        print("--- Test 1: No file yet ---")
        print("Total:", total_spent(test_file))

        print("\n--- Test 2: Input validation & corrupted line handling ---")
        add_expense("Tea", 20, test_file)

        # Validating before writing rejects "abc" right away
        add_expense("Lunch", "abc", test_file)

        # Simulate an externally corrupted line in the file to exercise total_spent() skip-path
        with open(test_file, "a", encoding="utf-8") as f:
            f.write("Corrupted_Entry,abc\n")

        add_expense("Bus", 35, test_file)

        for record in show_all(test_file):
            print(record)
        print("Total:", total_spent(test_file))

        print("\n--- Test 3: Clear file (with backup) & test normal file (3 expenses) ---")
        clear_all(test_file, create_backup=True)
        add_expense("Tea", 20, test_file)
        add_expense("Bus", 35, test_file)
        add_expense("Snacks", 80, test_file)

        for record in show_all(test_file):
            print(record)
        print("Final Total:", total_spent(test_file))