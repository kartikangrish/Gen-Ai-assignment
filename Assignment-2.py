# ==============================================================================
# ASSIGNMENT-2 SOLUTIONS
# ==============================================================================

# 1. What is 7 to the power of 4?
ans_1 = 7 ** 4
print(ans_1)  # Expected Output: 2401


# 2. Split this string into a list:
s = "Hi there Sam!"
ans_2 = s.split()
print(ans_2)  # Expected Output: ['Hi', 'there', 'Sam!']


# 3. Given the variables, use .format() to print the string:
planet = "Earth"
diameter = 12742
print("The diameter of {} is {} kilometers.".format(planet, diameter))


# 4. Given this nested list, use indexing to grab the word "hello"
lst = [3, 2, [3, 4], [5, [100, 200, ['hello']], 23, 11], 1, 7]
ans_4 = lst[3][1][2][0]
print(ans_4)  # Expected Output: 'hello'


# 5. Given this nested dictionary grab the word "hello". 
d = {'k1': [1, 2, 3, {'tricky': ['oh', 'man', 'inception', {'target': [1, 2, 3, 'hello']}]}]}
ans_5 = d['k1'][3]['tricky'][3]['target'][3]
print(ans_5)  # Expected Output: 'hello'


# 6. What is the main difference between a tuple and a list?
"""
The main difference is that lists are mutable (can be changed), 
whereas tuples are immutable (cannot be changed after creation).
"""


# 7. Create a function that grabs the email website domain
def domainGet(email):
    return email.split('@')[-1]

# Test
print(domainGet('user@domain.com'))  # Expected Output: 'domain.com'


# 8. Create a basic function that returns True if the word 'dog' is contained in the input string.
def findDog(st):
    return 'dog' in st.lower()

# Test
print(findDog('Is there a dog here?'))  # Expected Output: True


# 9. Create a function that counts the number of times the word "dog" occurs in a string.
def countDog(st):
    count = 0
    for word in st.lower().split():
        if 'dog' in word:  # Handles edge cases if punctuation is attached
            count += 1
    return count

# Test
print(countDog('This dog runs faster than the other dog dude!'))  # Expected Output: 2


# 10. Use lambda expressions and the filter() function to filter out words from a list that don't start with the letter 's'.
seq = ['soup', 'dog', 'salad', 'cat', 'great']
filtered_seq = list(filter(lambda word: word.startswith('s'), seq))
print(filtered_seq)  # Expected Output: ['soup', 'salad']


# ==============================================================================
# Final Problem
# ==============================================================================
def caught_speeding(speed, is_birthday):
    # If it's your birthday, your speed limits increase by 5
    if is_birthday:
        speed_limit_low = 65
        speed_limit_high = 85
    else:
        speed_limit_low = 60
        speed_limit_high = 80
        
    # Determine the ticket category
    if speed <= speed_limit_low:
        return 'No Ticket'
    elif speed <= speed_limit_high:
        return 'Small Ticket'
    else:
        return 'Big Ticket'

# Tests
print(caught_speeding(81, True))   # Expected Output: 'Small Ticket'
print(caught_speeding(81, False))  # Expected Output: 'Big Ticket'
