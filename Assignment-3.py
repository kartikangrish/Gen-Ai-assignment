# ==============================================================================
# ASSIGNMENT SET 3 SOLUTIONS
# ==============================================================================

# ------------------------------------------------------------------------------
# 1: Input and Type Conversion
# ------------------------------------------------------------------------------
print("--- 1: Input and Type Conversion ---")
# Taking two inputs
user_str = input("Enter a string: ")
user_num = input("Enter a number: ")

# Print both values and their types
print(f"Value 1: {user_str} | Type: {type(user_str)}")
print(f"Value 2: {user_num} | Type: {type(user_num)}")

# Convert the number to a float and print its type
converted_num = float(user_num)
print(f"Converted Value: {converted_num} | New Type: {type(converted_num)}")
print("\n")


# ------------------------------------------------------------------------------
# 2: Conditional Grading System
# ------------------------------------------------------------------------------
print("--- 2: Conditional Grading System ---")
try:
    mark = float(input("Enter student's mark: "))
    if mark >= 90:
        print("Grade: A+")
    elif mark >= 80:
        print("Grade: A")
    elif mark >= 70:
        print("Grade: B+")
    else:
        print("Grade: Failed")
except ValueError:
    print("Invalid input! Please enter a numerical value.")
print("\n")


# ------------------------------------------------------------------------------
# 3: Sum of Digits
# ------------------------------------------------------------------------------
print("--- 3: Sum of Digits ---")
def sum_of_digits(n):
    # Use absolute value to correctly handle negative inputs
    num = abs(n)
    total_sum = 0
    
    while num > 0:
        digit = num % 10
        total_sum += digit
        num = num // 10
        
    print(f"The sum of digits of {n} is: {total_sum}")
    return total_sum

# Example invocation
sum_of_digits(12345)
print("\n")


# ------------------------------------------------------------------------------
# 4: Menu-Driven Calculator
# ------------------------------------------------------------------------------
print("--- 4: Menu-Driven Calculator ---")
def calculator():
    while True:
        print("\nOptions:")
        print("1. Add\n2. Subtract\n3. Multiply\n4. Divide\n5. Exit")
        choice = input("Enter choice (1-5): ")
        
        if choice == '5':
            print("Exiting calculator. Goodbye!")
            break
            
        if choice not in ['1', '2', '3', '4']:
            print("Invalid choice! Please select a valid option.")
            continue
            
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            if choice == '1':
                print(f"Result: {num1 + num2}")
            elif choice == '2':
                print(f"Result: {num1 - num2}")
            elif choice == '3':
                print(f"Result: {num1 * num2}")
            elif choice == '4':
                if num2 == 0:
                    print("Error! Division by zero is not allowed.")
                else:
                    print(f"Result: {num1 / num2}")
        except ValueError:
            print("Invalid numerical input. Try again.")

# Uncomment the line below if you want the interactive loop to run on execution:
# calculator()
print("Calculator function loaded successfully.")
print("\n")


# ------------------------------------------------------------------------------
# 5: List Comprehension Practice
# ------------------------------------------------------------------------------
print("--- 5: List Comprehension Practice ---")
# A list of squares from 1 to 10
squares = [x**2 for x in range(1, 11)]
print("Squares (1-10):", squares)

# A list of even numbers from 1 to 20
evens = [x for x in range(1, 21) if x % 2 == 0]
print("Evens (1-20):  ", evens)

# A list of characters in the string "Python"
chars = [char for char in "Python"]
print("Characters:    ", chars)
print("\n")


# ------------------------------------------------------------------------------
# 6: Search in List
# ------------------------------------------------------------------------------
print("--- 6: Search in List ---")
search_list = [10, 23, 45, 78, 99, 105]
target_num = 78  # Example target

for element in search_list:
    if element == target_num:
        print("Found!")
        break
else:
    # Executes only if the loop completes without meeting a 'break'
    print("Not found")
print("\n")


# ------------------------------------------------------------------------------
# 7: Function with Variable Arguments
# ------------------------------------------------------------------------------
print("--- 7: Function with Variable Arguments ---")
def print_args_kwargs(*args, **kwargs):
    print(f"Positional args type: {type(args)} | Contents: {args}")
    print(f"Keyword args type:    {type(kwargs)} | Contents: {kwargs}")

# Example invocation
print_args_kwargs(1, 2, "three", status="active", version=3.1)
print("\n")


# ------------------------------------------------------------------------------
# 8: Global vs Local Variables
# ------------------------------------------------------------------------------
print("--- 8: Global vs Local Variables ---")
# Global variable definition
counter = 10

def modify_global():
    global counter
    counter += 5
    local_var = "I am local"
    print(f"Inside function -> Local Variable: {local_var}")
    print(f"Inside function -> Modified Global counter: {counter}")

print(f"Before function call -> Global counter: {counter}")
modify_global()
print(f"After function call -> Global counter: {counter}")
print("\n")


# ------------------------------------------------------------------------------
# 9: ASCII Conversion
# ------------------------------------------------------------------------------
print("--- 9: ASCII Conversion ---")
# Character input to ASCII value
char_input = 'A'
ascii_val = ord(char_input)
print(f"The ASCII value of '{char_input}' is {ascii_val}")

# ASCII value input to character
input_ascii = 97
char_val = chr(input_ascii)
print(f"The character for ASCII value {input_ascii} is '{char_val}'")
print("\n")


# ------------------------------------------------------------------------------
# 10: Range and Loop Patterns
# ------------------------------------------------------------------------------
print("--- 10: Range and Loop Patterns ---")

# 1. Numbers from 1 to 10
print("Numbers 1 to 10:")
for i in range(1, 11):
    print(i, end=" ")
print("\n")

# 2. Odd numbers from 1 to 20
print("Odd numbers 1 to 20:")
i = 1
while i <= 20:
    if i % 2 != 0:
        print(i, end=" ")
    i += 1
print("\n")

# 3. A pattern: 3, 7, 11, ..., up to a user-defined limit
user_limit = 30  # Hardcoded example limit
print(f"Pattern (step of 4) up to {user_limit}:")
for val in range(3, user_limit + 1, 4):
    print(val, end=" ")
print("\n")
