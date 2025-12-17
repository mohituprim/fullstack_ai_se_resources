# Pythonic Thinking: Effective Python Best Practices

## 1. Know Which Version of Python You're Using

### Explanation
Python has multiple versions (2.x, 3.x) with significant differences. Python 2 reached end-of-life in 2020. Python 3.x has multiple sub-versions (3.7, 3.8, 3.9, 3.10, 3.11, 3.12+) with different features and capabilities. Knowing your version helps you:
- Use version-specific features correctly
- Avoid compatibility issues
- Ensure dependencies work properly
- Debug version-related problems

### Use Cases
- Setting up development environments
- Installing packages (some require specific Python versions)
- Using new language features (e.g., match/case requires Python 3.10+)
- Debugging compatibility issues
- Writing code that needs to work across multiple Python versions

### Examples

```python
# Method 1: Command line
# python3 --version
# Output: Python 3.12.0

# Method 2: In Python code
import sys
print(sys.version)
# Output: 3.12.0 (main, Oct 25 2023, 18:00:00) [Clang 15.0.0]

# Method 3: Version info tuple
import sys
print(sys.version_info)
# Output: sys.version_info(major=3, minor=12, micro=0, releaselevel='final', serial=0)

# Method 4: Check for specific version
import sys
if sys.version_info >= (3, 10):
    print("Can use match/case statements")
else:
    print("Need Python 3.10+ for match/case")

# Method 5: Check version in code for compatibility
import sys
if sys.version_info < (3, 8):
    raise RuntimeError("This script requires Python 3.8 or higher")
```

### Why It Matters
- **Feature Availability**: Some features like `walrus operator (:=)` require Python 3.8+, `match/case` requires 3.10+
- **Performance**: Newer versions have performance improvements
- **Security**: Older versions may have security vulnerabilities
- **Library Support**: Many modern libraries drop support for older Python versions

---

## 2. Follow the PEP 8 Style Guide

### Explanation
PEP 8 is the official Python style guide that defines coding conventions for readability and consistency. It covers naming conventions, code layout, whitespace, comments, and more. Following PEP 8 makes your code more readable and maintainable.

### Use Cases
- Writing production code
- Contributing to open-source projects
- Code reviews
- Team collaboration
- Maintaining consistency across projects

### Examples

```python
# ❌ BAD: Not following PEP 8
def calculateTotal(x,y):
    result=x+y
    return result

class myClass:
    def __init__(self,name):
        self.name=name

# ✅ GOOD: Following PEP 8
def calculate_total(x, y):
    """Calculate the sum of two numbers.
    
    Args:
        x (int): First number
        y (int): Second number
    
    Returns:
        int: Sum of x and y
    """
    result = x + y
    return result


class MyClass:
    """A sample class following PEP 8 conventions."""
    
    def __init__(self, name):
        """Initialize the class with a name.
        
        Args:
            name (str): The name to assign
        """
        self.name = name


# PEP 8 Naming Conventions:
# - Functions: snake_case (calculate_total)
# - Classes: PascalCase (MyClass)
# - Constants: UPPER_SNAKE_CASE (MAX_SIZE = 100)
# - Private: _leading_underscore (_internal_method)
# - Name mangling: __double_underscore (__private_method)

# PEP 8 Spacing:
# - Use 4 spaces for indentation (not tabs)
# - Maximum line length: 79 characters (or 99 for some teams)
# - Blank lines: 2 between top-level functions/classes, 1 between methods
# - Spaces around operators: x = y + z (not x=y+z)
# - No spaces inside parentheses: func(x, y) (not func( x, y ))

# PEP 8 Imports:
# - Standard library imports first
# - Third-party imports second
# - Local application imports last
# - Each group separated by blank line

import os
import sys

import requests
import numpy as np

from my_module import MyClass
from utils.helpers import helper_function
```

### Key PEP 8 Rules
1. **Indentation**: 4 spaces (never mix tabs and spaces)
2. **Line Length**: Maximum 79 characters (or 99)
3. **Blank Lines**: 2 between top-level definitions, 1 between methods
4. **Imports**: Grouped (stdlib, third-party, local) with blank lines
5. **Whitespace**: Around operators, after commas, not inside parentheses
6. **Naming**: snake_case for functions/variables, PascalCase for classes

---

## 3. Never Expect Python to Detect Errors at Compile Time

### Explanation
Python is an interpreted language, not compiled. It doesn't have a traditional compile-time phase like C++ or Java. Errors are only detected when the code is actually executed. This means:
- Syntax errors are caught when Python parses the file
- Type errors, attribute errors, and logic errors are only found at runtime
- You can't rely on static type checking unless you use tools like mypy

### Use Cases
- Understanding why errors appear only when running code
- Writing defensive code with proper error handling
- Using type hints and static type checkers (mypy)
- Testing code thoroughly before deployment

### Examples

```python
# ❌ This code will NOT show an error until runtime
def divide_numbers(a, b):
    return a / b

# This will work fine
result = divide_numbers(10, 2)  # Returns 5.0

# This will crash at runtime (ZeroDivisionError)
result = divide_numbers(10, 0)  # Runtime error!


# ❌ Type errors are not caught at "compile time"
def add_numbers(a, b):
    return a + b

# Python won't complain about this until runtime
result = add_numbers("hello", 5)  # TypeError: can only concatenate str (not "int") to str


# ❌ Attribute errors are runtime errors
class Person:
    def __init__(self, name):
        self.name = name

person = Person("Alice")
print(person.age)  # AttributeError: 'Person' object has no attribute 'age'
# This error only appears when this line executes


# ✅ Use type hints and static type checkers
from typing import List

def process_items(items: List[str]) -> int:
    """Process a list of strings and return count."""
    return len(items)

# Install mypy: pip install mypy
# Run: mypy script.py
# mypy will catch type errors before runtime


# ✅ Use defensive programming and error handling
def safe_divide(a, b):
    """Safely divide two numbers with error handling."""
    try:
        return a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
        return None
    except TypeError:
        print("Error: Both arguments must be numbers")
        return None


# ✅ Use assertions for debugging (removed in optimized mode)
def calculate_percentage(value, total):
    assert total != 0, "Total cannot be zero"
    assert value >= 0, "Value cannot be negative"
    return (value / total) * 100
```

### Why It Matters
- **Runtime Errors**: All errors happen when code executes, not before
- **Testing**: You must test your code to find errors
- **Type Safety**: Use type hints + mypy for static type checking
- **Defensive Programming**: Always validate inputs and handle exceptions

---

## 4. Write Helper Functions Instead of Complex Expressions

### Explanation
Complex expressions are hard to read, debug, and maintain. Breaking them into helper functions improves:
- **Readability**: Clear function names explain intent
- **Reusability**: Functions can be used multiple times
- **Testability**: Each function can be tested independently
- **Debugging**: Easier to identify where problems occur

### Use Cases
- Complex calculations or data transformations
- Repeated logic patterns
- Improving code readability
- Making code more maintainable
- Enabling unit testing

### Examples

```python
# ❌ BAD: Complex expression that's hard to read
from datetime import datetime, timedelta

users = [
    {"name": "Alice", "age": 25, "signup_date": "2023-01-15"},
    {"name": "Bob", "age": 30, "signup_date": "2022-06-20"},
    {"name": "Charlie", "age": 22, "signup_date": "2024-03-10"}
]

# Complex nested expression
active_users = [
    user for user in users 
    if (datetime.now() - datetime.strptime(user["signup_date"], "%Y-%m-%d")).days > 90 
    and user["age"] >= 18 
    and user["name"][0].isupper()
]


# ✅ GOOD: Using helper functions
def is_user_active(signup_date, days_threshold=90):
    """Check if user has been active for more than threshold days."""
    signup = datetime.strptime(signup_date, "%Y-%m-%d")
    days_since_signup = (datetime.now() - signup).days
    return days_since_signup > days_threshold


def is_adult(age, min_age=18):
    """Check if user is an adult."""
    return age >= min_age


def has_valid_name(name):
    """Check if name starts with uppercase letter."""
    return name and name[0].isupper()


def is_valid_user(user):
    """Check if user meets all criteria."""
    return (
        is_user_active(user["signup_date"]) and
        is_adult(user["age"]) and
        has_valid_name(user["name"])
    )


active_users = [user for user in users if is_valid_user(user)]


# Another Example: Complex calculation

# ❌ BAD: Hard to understand
def calculate_discount(price, quantity, is_member, has_coupon):
    return price * quantity * (1 - (0.1 if is_member else 0) - (0.05 if has_coupon else 0)) * (0.95 if quantity > 10 else 1)


# ✅ GOOD: Clear helper functions
def get_member_discount(is_member):
    """Return member discount percentage."""
    return 0.1 if is_member else 0.0


def get_coupon_discount(has_coupon):
    """Return coupon discount percentage."""
    return 0.05 if has_coupon else 0.0


def get_quantity_discount(quantity):
    """Return quantity discount multiplier."""
    return 0.95 if quantity > 10 else 1.0


def calculate_discount(price, quantity, is_member, has_coupon):
    """Calculate final price with all applicable discounts."""
    base_total = price * quantity
    member_discount = get_member_discount(is_member)
    coupon_discount = get_coupon_discount(has_coupon)
    total_discount = member_discount + coupon_discount
    discounted_total = base_total * (1 - total_discount)
    quantity_discount = get_quantity_discount(quantity)
    final_total = discounted_total * quantity_discount
    return final_total
```

### Benefits
- **Clarity**: Function names document what the code does
- **Maintainability**: Easy to modify individual parts
- **Testing**: Each function can be unit tested
- **Reusability**: Functions can be used in multiple places

---

## 5. Prefer Multiple-Assignment Unpacking over Indexing

### Explanation
Python's unpacking feature allows you to assign multiple variables from sequences in one line. This is more readable, less error-prone, and more Pythonic than using indices. Unpacking works with tuples, lists, and any iterable.

### Use Cases
- Returning multiple values from functions
- Swapping variables
- Processing structured data (tuples, lists)
- Working with dictionaries (keys, values, items)
- Parsing data structures

### Examples

```python
# ❌ BAD: Using indexing
def get_user_info():
    return ("Alice", 25, "Engineer")

user_info = get_user_info()
name = user_info[0]
age = user_info[1]
job = user_info[2]
print(f"{name} is {age} years old and works as a {job}")


# ✅ GOOD: Using unpacking
def get_user_info():
    return ("Alice", 25, "Engineer")

name, age, job = get_user_info()
print(f"{name} is {age} years old and works as a {job}")


# Swapping variables
# ❌ BAD: Using temporary variable
a = 10
b = 20
temp = a
a = b
b = temp

# ✅ GOOD: Using unpacking
a, b = 10, 20
a, b = b, a  # Swap in one line!
print(a, b)  # 20, 10


# Working with lists
# ❌ BAD: Indexing
coordinates = [3, 5, 7]
x = coordinates[0]
y = coordinates[1]
z = coordinates[2]

# ✅ GOOD: Unpacking
x, y, z = coordinates
print(f"Point at ({x}, {y}, {z})")


# Partial unpacking with *
# ✅ GOOD: Unpacking with rest
numbers = [1, 2, 3, 4, 5]
first, *rest = numbers
print(first)  # 1
print(rest)   # [2, 3, 4, 5]

first, second, *rest = numbers
print(first, second)  # 1, 2
print(rest)           # [3, 4, 5]

*beginning, last = numbers
print(beginning)  # [1, 2, 3, 4]
print(last)       # 5


# Dictionary unpacking
# ✅ GOOD: Unpacking dictionary items
user = {"name": "Bob", "age": 30, "city": "New York"}

for key, value in user.items():
    print(f"{key}: {value}")

# Unpacking keys
name, age, city = user.keys()
print(name, age, city)  # name age city

# Unpacking values
name_val, age_val, city_val = user.values()
print(name_val, age_val, city_val)  # Bob 30 New York


# Nested unpacking
# ✅ GOOD: Unpacking nested structures
data = [("Alice", 25), ("Bob", 30), ("Charlie", 22)]

for name, age in data:
    print(f"{name} is {age} years old")

# More complex nested unpacking
points = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
for x, y, z in points:
    print(f"Point: ({x}, {y}, {z})")


# Ignoring values with _
# ✅ GOOD: Using _ for unused values
user_data = ("Alice", "alice@email.com", "123-456-7890", "Engineer")
name, email, _, job = user_data  # Ignore phone number
print(f"{name} ({email}) works as a {job}")


# Multiple return values
# ✅ GOOD: Function returning multiple values
def calculate_stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

minimum, maximum, average = calculate_stats([10, 20, 30, 40, 50])
print(f"Min: {minimum}, Max: {maximum}, Avg: {average}")
```

### Benefits
- **Readability**: Clearer intent than indexing
- **Safety**: Avoids index errors
- **Conciseness**: Less code, more expressive
- **Pythonic**: Follows Python best practices

---

## 6. Always Surround Single-Element Tuples with Parentheses

### Explanation
In Python, a single-element tuple requires a trailing comma to distinguish it from a parenthesized expression. Without the comma, Python treats it as a regular expression in parentheses, not a tuple. This is a common source of bugs.

### Use Cases
- Creating single-element tuples
- Returning single values as tuples from functions
- Tuple unpacking with single elements
- API design where you want consistent tuple returns

### Examples

```python
# ❌ BAD: This is NOT a tuple, it's just parentheses
single_item = (42)
print(type(single_item))  # <class 'int'>, NOT tuple!

# ✅ GOOD: Trailing comma makes it a tuple
single_item = (42,)
print(type(single_item))  # <class 'tuple'>

# Alternative: Without parentheses (also works)
single_item = 42,
print(type(single_item))  # <class 'tuple'>


# Function returning single value as tuple
# ❌ BAD: Forgetting the comma
def get_status():
    return ("active")  # Returns string, not tuple!

status = get_status()
print(type(status))  # <class 'str'>

# ✅ GOOD: With trailing comma
def get_status():
    return ("active",)  # Returns tuple

status = get_status()
print(type(status))  # <class 'tuple'>


# Unpacking single-element tuple
# ❌ BAD: This won't work as expected
def get_user_id():
    return (12345)  # Returns int, not tuple

user_id = get_user_id()
# user_id, = get_user_id()  # This would fail with TypeError

# ✅ GOOD: Proper single-element tuple
def get_user_id():
    return (12345,)

user_id, = get_user_id()  # Unpacks correctly
print(user_id)  # 12345


# Consistency in API design
# ✅ GOOD: Always return tuples for consistency
def get_user_data(user_id):
    if user_id == 1:
        return ("Alice", 25)  # Multiple values
    else:
        return ("Unknown",)  # Single value as tuple (consistent return type)


# List of single-element tuples
# ✅ GOOD: Creating list of single-element tuples
tags = [("python",), ("javascript",), ("react",)]
for tag, in tags:  # Note the comma in unpacking
    print(tag)


# Dictionary with tuple keys
# ✅ GOOD: Single-element tuple as dictionary key
coordinates = {
    (0,): "origin",
    (1,): "point_one",
    (2, 3): "point_two_three"
}
print(coordinates[(0,)])  # "origin"
```

### Why It Matters
- **Type Safety**: Ensures you get a tuple, not a different type
- **Consistency**: Maintains consistent return types in functions
- **Unpacking**: Required for proper tuple unpacking
- **Bug Prevention**: Prevents subtle type-related bugs

### Common Pitfall
```python
# This is a common mistake:
my_tuple = (1)  # This is an int, not a tuple!
my_tuple = (1,)  # This is a tuple
```

---

## 7. Consider Conditional Expressions for Simple Inline Logic

### Explanation
Conditional expressions (ternary operators) provide a concise way to write simple if-else logic in a single line. They follow the format: `value_if_true if condition else value_if_false`. Use them for simple cases, but prefer if-else statements for complex logic.

### Use Cases
- Simple value assignments based on conditions
- Return statements with simple conditions
- List comprehensions with conditions
- Default value assignments
- Simple formatting or display logic

### Examples

```python
# ❌ BAD: Verbose if-else for simple case
def get_status(is_active):
    if is_active:
        status = "online"
    else:
        status = "offline"
    return status

# ✅ GOOD: Using conditional expression
def get_status(is_active):
    return "online" if is_active else "offline"


# Assigning values
# ❌ BAD: Verbose
age = 20
if age >= 18:
    category = "adult"
else:
    category = "minor"

# ✅ GOOD: Concise
age = 20
category = "adult" if age >= 18 else "minor"


# In list comprehensions
# ✅ GOOD: Conditional in comprehension
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_or_odd = ["even" if n % 2 == 0 else "odd" for n in numbers]
print(even_or_odd)  # ['odd', 'even', 'odd', 'even', ...]


# Multiple conditions (nested)
# ⚠️ CAUTION: Can become hard to read
score = 85
grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"
print(grade)  # "B"

# ✅ BETTER: For complex logic, use if-else
def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    else:
        return "F"


# Default values
# ✅ GOOD: Providing defaults
def greet_user(name=None):
    display_name = name if name else "Guest"
    return f"Hello, {display_name}!"

print(greet_user("Alice"))  # "Hello, Alice!"
print(greet_user())         # "Hello, Guest!"


# In function arguments
# ✅ GOOD: Conditional default values
def process_data(data, format_type="json"):
    output_format = format_type if format_type in ["json", "xml"] else "json"
    return f"Processing as {output_format}"


# Formatting strings
# ✅ GOOD: Conditional formatting
def format_price(price, include_currency=True):
    currency_symbol = "$" if include_currency else ""
    return f"{currency_symbol}{price:.2f}"

print(format_price(99.99))        # "$99.99"
print(format_price(99.99, False)) # "99.99"


# ❌ BAD: Too complex for conditional expression
def calculate_discount(price, quantity, is_member, has_coupon):
    # This is too complex - use if-else instead
    return price * 0.9 if is_member and quantity > 10 else price * 0.95 if has_coupon else price

# ✅ GOOD: Use if-else for complex logic
def calculate_discount(price, quantity, is_member, has_coupon):
    if is_member and quantity > 10:
        return price * 0.9
    elif has_coupon:
        return price * 0.95
    else:
        return price
```

### When to Use
- ✅ **Use conditional expressions for**: Simple true/false assignments, default values, simple formatting
- ❌ **Avoid conditional expressions for**: Complex nested conditions, multiple operations, logic that affects readability

### Best Practices
1. Keep it simple - one condition, two outcomes
2. Don't nest more than one level
3. Use if-else for complex logic
4. Prioritize readability over brevity

---

## 8. Prevent Repetition with Assignment Expressions (Walrus Operator)

### Explanation
The walrus operator (`:=`) was introduced in Python 3.8. It allows you to assign values to variables as part of an expression. This prevents repetition by avoiding the need to call functions or access values multiple times. It's called "walrus" because `:=` looks like a walrus's eyes and tusks.

### Use Cases
- Avoiding repeated function calls
- Simplifying while loops
- List comprehensions with conditions
- Reducing code duplication
- Improving performance by caching computed values

### Examples

```python
# ❌ BAD: Repeated function call
import re

text = "Hello, my email is alice@example.com and phone is 123-456-7890"
match = re.search(r'\d{3}-\d{3}-\d{4}', text)
if match:
    phone = match.group()
    print(f"Found phone: {phone}")
else:
    print("No phone found")

# ✅ GOOD: Using walrus operator
if match := re.search(r'\d{3}-\d{3}-\d{4}', text):
    print(f"Found phone: {match.group()}")
else:
    print("No phone found")


# While loops
# ❌ BAD: Repetitive pattern
while True:
    line = input("Enter a number (or 'quit' to exit): ")
    if line == 'quit':
        break
    number = int(line)
    print(f"You entered: {number}")

# ✅ GOOD: Using walrus operator
while (line := input("Enter a number (or 'quit' to exit): ")) != 'quit':
    number = int(line)
    print(f"You entered: {number}")


# List comprehensions
# ❌ BAD: Calling function twice
def expensive_calculation(x):
    # Simulate expensive operation
    return x ** 2 + 10

numbers = [1, 2, 3, 4, 5]
results = [expensive_calculation(n) for n in numbers if expensive_calculation(n) > 15]
# expensive_calculation is called twice for each number!

# ✅ GOOD: Using walrus operator
results = [result for n in numbers if (result := expensive_calculation(n)) > 15]
# expensive_calculation is called only once per number


# Reading files
# ❌ BAD: Repetitive file reading
file = open("data.txt", "r")
line = file.readline()
while line:
    process(line)
    line = file.readline()
file.close()

# ✅ GOOD: Using walrus operator
with open("data.txt", "r") as file:
    while line := file.readline():
        process(line)


# Parsing data
# ❌ BAD: Multiple checks
data = {"items": [1, 2, 3]}
if "items" in data and len(data["items"]) > 0:
    first_item = data["items"][0]
    print(f"First item: {first_item}")

# ✅ GOOD: Using walrus operator
if "items" in data and (items := data["items"]) and len(items) > 0:
    print(f"First item: {items[0]}")


# Caching expensive operations
# ❌ BAD: Repeated calculation
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = [n ** 2 for n in numbers if n ** 2 > 25]
# n ** 2 is calculated twice for each number

# ✅ GOOD: Using walrus operator
squares = [square for n in numbers if (square := n ** 2) > 25]
# n ** 2 is calculated only once


# Multiple conditions
# ✅ GOOD: Using walrus in complex conditions
def process_user(user_id):
    if (user := get_user(user_id)) and user.is_active and user.has_permission:
        return f"Processing {user.name}"
    return "User not available"

# Without walrus, you'd need:
# user = get_user(user_id)
# if user and user.is_active and user.has_permission:
#     ...
```

### When to Use
- ✅ **Use walrus operator when**: 
  - You need to use a computed value multiple times
  - You want to avoid repeated function calls
  - Simplifying while loops
  - Improving performance in comprehensions

- ❌ **Avoid walrus operator when**:
  - It makes code less readable
  - The assignment isn't needed elsewhere
  - It creates confusion about variable scope

### Important Notes
- Requires Python 3.8+
- Assignment expressions have lower precedence than most operators
- Use parentheses to ensure correct evaluation order
- Don't overuse - readability is more important than cleverness

---

## 9. Consider match for Destructuring in Flow Control; Avoid When if Statements Are Sufficient

### Explanation
The `match` statement (introduced in Python 3.10) is similar to switch statements in other languages but more powerful. It supports pattern matching, destructuring, and type checking. However, for simple conditions, traditional `if-elif-else` statements are often clearer and more appropriate.

### Use Cases
- Pattern matching on data structures
- Destructuring tuples, lists, dictionaries
- Type checking and handling different types
- Complex conditional logic with multiple patterns
- Replacing long if-elif chains with cleaner syntax

### Examples

```python
# Simple case - if-else is better
# ❌ OVERKILL: Using match for simple condition
def get_status_code(is_success):
    match is_success:
        case True:
            return 200
        case False:
            return 500

# ✅ BETTER: Simple if-else
def get_status_code(is_success):
    return 200 if is_success else 500


# Pattern matching with values
# ✅ GOOD: Using match for multiple values
def handle_http_status(code):
    match code:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:  # Default case
            return "Unknown Status"

# Equivalent if-else (more verbose)
def handle_http_status_if(code):
    if code == 200:
        return "OK"
    elif code == 404:
        return "Not Found"
    elif code == 500:
        return "Internal Server Error"
    else:
        return "Unknown Status"


# Destructuring tuples
# ✅ GOOD: Match with tuple destructuring
def process_point(point):
    match point:
        case (0, 0):
            return "Origin"
        case (x, 0):
            return f"On x-axis at {x}"
        case (0, y):
            return f"On y-axis at {y}"
        case (x, y):
            return f"Point at ({x}, {y})"

print(process_point((0, 0)))    # "Origin"
print(process_point((5, 0)))    # "On x-axis at 5"
print(process_point((0, 3)))    # "On y-axis at 3"
print(process_point((2, 4)))    # "Point at (2, 4)"


# Destructuring lists
# ✅ GOOD: Match with list patterns
def process_command(command):
    match command:
        case ["quit"]:
            return "Exiting..."
        case ["move", x, y]:
            return f"Moving to ({x}, {y})"
        case ["attack", target]:
            return f"Attacking {target}"
        case ["use", item, *args]:
            return f"Using {item} with {args}"
        case _:
            return "Unknown command"

print(process_command(["quit"]))              # "Exiting..."
print(process_command(["move", 10, 20]))      # "Moving to (10, 20)"
print(process_command(["attack", "goblin"]))  # "Attacking goblin"
print(process_command(["use", "potion", "health"]))  # "Using potion with ['health']"


# Type checking and destructuring
# ✅ GOOD: Match with type checking
def process_data(data):
    match data:
        case int(x) if x > 0:
            return f"Positive integer: {x}"
        case int(x):
            return f"Non-positive integer: {x}"
        case str(s):
            return f"String: {s}"
        case list(items) if len(items) > 0:
            return f"Non-empty list with {len(items)} items"
        case list():
            return "Empty list"
        case dict(d) if "name" in d:
            return f"Dictionary with name: {d['name']}"
        case _:
            return "Unknown type"

print(process_data(42))                    # "Positive integer: 42"
print(process_data("hello"))               # "String: hello"
print(process_data([1, 2, 3]))             # "Non-empty list with 3 items"
print(process_data({"name": "Alice"}))     # "Dictionary with name: Alice"


# Complex pattern matching
# ✅ GOOD: Match with guards and complex patterns
def evaluate_expression(expr):
    match expr:
        case ("add", x, y) if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            return x + y
        case ("multiply", x, y) if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            return x * y
        case ("divide", x, y) if y != 0:
            return x / y
        case ("divide", _, 0):
            return "Error: Division by zero"
        case _:
            return "Unknown expression"

print(evaluate_expression(("add", 5, 3)))        # 8
print(evaluate_expression(("multiply", 4, 7)))   # 28
print(evaluate_expression(("divide", 10, 2)))    # 5.0
print(evaluate_expression(("divide", 10, 0)))    # "Error: Division by zero"


# Dictionary pattern matching
# ✅ GOOD: Match with dictionary patterns
def process_user(user):
    match user:
        case {"name": name, "age": age, "role": "admin"}:
            return f"Admin user {name}, age {age}"
        case {"name": name, "age": age} if age >= 18:
            return f"Adult user {name}, age {age}"
        case {"name": name, "age": age}:
            return f"Minor user {name}, age {age}"
        case {"name": name}:
            return f"User {name} (age unknown)"
        case _:
            return "Invalid user data"

print(process_user({"name": "Alice", "age": 25, "role": "admin"}))  # "Admin user Alice, age 25"
print(process_user({"name": "Bob", "age": 20}))                     # "Adult user Bob, age 20"
print(process_user({"name": "Charlie", "age": 15}))                 # "Minor user Charlie, age 15"


# When NOT to use match
# ❌ BAD: Simple condition - if is better
def is_even(number):
    match number % 2:
        case 0:
            return True
        case _:
            return False

# ✅ GOOD: Simple if is clearer
def is_even(number):
    return number % 2 == 0
```

### When to Use match
- ✅ **Use match when**:
  - You have multiple distinct values to check
  - You need to destructure data structures
  - Pattern matching provides clearer code
  - You're checking types or complex patterns
  - Replacing long if-elif chains

- ❌ **Avoid match when**:
  - Simple boolean conditions (use if-else)
  - Only 2-3 simple cases (if-elif is clearer)
  - You need Python < 3.10 compatibility
  - The pattern matching doesn't add clarity

### Key Features of match
1. **Pattern Matching**: Match against values, types, and structures
2. **Destructuring**: Extract values from tuples, lists, dicts
3. **Guards**: Additional conditions with `if`
4. **Wildcards**: `_` matches anything
5. **Type Checking**: Match against types

### Best Practices
- Use `match` for complex pattern matching and destructuring
- Use `if-elif-else` for simple conditions
- Prefer readability over using the newest features
- Consider Python version compatibility (match requires 3.10+)

---

## Summary

These nine principles form the foundation of writing effective, Pythonic code:

1. **Know Your Python Version** - Essential for using features and avoiding compatibility issues
2. **Follow PEP 8** - Ensures code readability and consistency
3. **Runtime Error Awareness** - Understand Python's interpreted nature
4. **Helper Functions** - Improve readability and maintainability
5. **Unpacking over Indexing** - More Pythonic and safer
6. **Single-Element Tuples** - Proper syntax prevents bugs
7. **Conditional Expressions** - Concise for simple cases
8. **Assignment Expressions** - Reduce repetition (Python 3.8+)
9. **match Statements** - Powerful pattern matching (Python 3.10+)

Remember: **Readability and maintainability should always be prioritized over cleverness or brevity.**
