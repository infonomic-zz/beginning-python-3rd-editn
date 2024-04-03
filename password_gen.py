# Password Generator Project
import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the PyPassword Generator!")
nr_letters = int(input("How many letters would you like in your password?\n"))
nr_symbols = int(input("How many symbols would you like?\n"))
nr_numbers = int(input("How many numbers would you like?\n"))

place_holder = []

# Select letters
for char in range(0, nr_letters):
    place_holder.append(random.choice(letters))

# Select symbols
for char in range(0, nr_symbols):
    place_holder.append(random.choice(symbols))

# Select numbers
for char in range(0, nr_numbers):
    place_holder.append(random.choice(numbers))

print(place_holder)
random.shuffle(place_holder)
print(place_holder)

password = ""
for char in place_holder:
    password += char

print(f"Your password is: {password}")
