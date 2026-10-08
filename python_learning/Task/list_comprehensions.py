# Challenge 1: Create a list of squares of numbers from 1 to 10 using a list comprehension.
squares = [x**2 for x in range(1, 11)]
print("Squares of numbers from 1 to 10:", squares)

# Challenge 2: Use a list comprehension to filter out even numbers from a list of numbers from 1 to 20.
# Note: 'Filtering out' even numbers implies keeping the odd numbers.
filtered_numbers = [x for x in range(1, 21) if x % 2 != 0]
print("List after filtering out even numbers (keeping odds):", filtered_numbers)

# (Alternative interpretation: extracting even numbers)
even_numbers = [x for x in range(1, 21) if x % 2 == 0]
print("List of only even numbers:", even_numbers)
