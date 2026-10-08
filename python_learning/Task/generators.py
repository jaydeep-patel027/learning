# Challenge 1: Write a generator function countdown that takes a number and counts down to zero.
def countdown(num):
    """A generator that yields numbers counting down to zero."""
    while num >= 0:
        yield num
        num -= 1

# Challenge 2: Iterate over the generator and print each number.
print("Countdown starting:")
for number in countdown(5):
    print(number)
