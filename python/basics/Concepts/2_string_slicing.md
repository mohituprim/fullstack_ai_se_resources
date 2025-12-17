# Strings and Slicing: Effective Python Best Practices

## 1. Know the Differences Between bytes and str

### Explanation
Python has two types for representing sequences of characters:
- **`str`**: Unicode text strings (human-readable text)
- **`bytes`**: Raw binary data (8-bit sequences)

Understanding the difference is crucial for:
- Working with files (text vs binary)
- Network communication
- Data encoding/decoding
- API interactions

### Use Cases
- Reading/writing files (text vs binary mode)
- Network programming (HTTP, sockets)
- Working with APIs that return binary data
- Data serialization
- Cryptography operations

### Examples

```python
# str - Unicode text strings
text = "Hello, 世界"  # Can contain any Unicode character
print(type(text))     # <class 'str'>
print(len(text))      # 10 (characters, not bytes)

# bytes - Raw binary data
binary_data = b"Hello, World"  # Only ASCII characters allowed
print(type(binary_data))        # <class 'bytes'>
print(len(binary_data))         # 12 (bytes)

# ❌ BAD: Mixing str and bytes
text = "Hello"
binary = b"World"
# result = text + binary  # TypeError: can only concatenate str (not "bytes") to str

# ✅ GOOD: Convert between str and bytes
text = "Hello, 世界"
# Encoding: str -> bytes
encoded = text.encode('utf-8')
print(encoded)  # b'Hello, \xe4\xb8\x96\xe7\x95\x8c'
print(type(encoded))  # <class 'bytes'>

# Decoding: bytes -> str
decoded = encoded.decode('utf-8')
print(decoded)  # "Hello, 世界"
print(type(decoded))  # <class 'str'>

# File operations
# ✅ GOOD: Text mode (returns str)
with open('text_file.txt', 'r', encoding='utf-8') as f:
    content = f.read()  # Returns str
    print(type(content))  # <class 'str'>

# ✅ GOOD: Binary mode (returns bytes)
with open('image.jpg', 'rb') as f:
    image_data = f.read()  # Returns bytes
    print(type(image_data))  # <class 'bytes'>

# Network operations
# ✅ GOOD: HTTP responses
import requests
response = requests.get('https://api.example.com/data')
# response.text is str
# response.content is bytes

# Working with different encodings
text = "Hello, 世界"
utf8_bytes = text.encode('utf-8')
ascii_bytes = text.encode('ascii', errors='ignore')  # Drops non-ASCII
print(utf8_bytes)   # b'Hello, \xe4\xb8\x96\xe7\x95\x8c'
print(ascii_bytes)  # b'Hello, '
```

### Key Differences
- **str**: Immutable sequence of Unicode characters, human-readable
- **bytes**: Immutable sequence of 8-bit values, binary data
- **Conversion**: Use `.encode()` (str→bytes) and `.decode()` (bytes→str)
- **Default encoding**: UTF-8 (recommended)

---

## 2. Prefer Interpolated F-Strings over C-Style Format Strings and str.format

### Explanation
F-strings (formatted string literals) were introduced in Python 3.6. They provide:
- Better readability
- Better performance
- More concise syntax
- Direct expression evaluation

### Use Cases
- String formatting and templating
- Debugging (embedding variable values)
- Logging messages
- Building dynamic strings
- Displaying formatted output

### Examples

```python
name = "Alice"
age = 25
score = 95.5

# ❌ BAD: C-style formatting (old, less readable)
message = "Hello, %s! You are %d years old. Score: %.2f" % (name, age, score)
print(message)

# ❌ BAD: str.format (verbose)
message = "Hello, {}! You are {} years old. Score: {:.2f}".format(name, age, score)
print(message)

# ❌ BAD: str.format with named arguments (better but still verbose)
message = "Hello, {name}! You are {age} years old. Score: {score:.2f}".format(
    name=name, age=age, score=score
)
print(message)

# ✅ GOOD: F-strings (Python 3.6+)
message = f"Hello, {name}! You are {age} years old. Score: {score:.2f}"
print(message)

# F-strings with expressions
# ✅ GOOD: Direct expression evaluation
x = 10
y = 20
result = f"The sum of {x} and {y} is {x + y}"
print(result)  # "The sum of 10 and 20 is 30"

# F-strings with method calls
# ✅ GOOD: Calling methods directly
text = "hello world"
formatted = f"Uppercase: {text.upper()}, Title: {text.title()}"
print(formatted)

# F-strings with formatting options
# ✅ GOOD: Number formatting
price = 99.99
formatted_price = f"Price: ${price:.2f}"  # "Price: $99.99"
percentage = 0.85
formatted_pct = f"Percentage: {percentage:.1%}"  # "Percentage: 85.0%"

# F-strings with alignment
# ✅ GOOD: Text alignment
name = "Alice"
print(f"|{name:>10}|")   # Right align: "|     Alice|"
print(f"|{name:<10}|")   # Left align: "|Alice     |"
print(f"|{name:^10}|")   # Center: "|  Alice   |"

# F-strings with dates
# ✅ GOOD: Date formatting
from datetime import datetime
now = datetime.now()
formatted_date = f"Today is {now:%Y-%m-%d %H:%M:%S}"
print(formatted_date)

# F-strings in loops
# ✅ GOOD: Building strings in loops
items = ["apple", "banana", "cherry"]
formatted_items = ", ".join(f"{i+1}. {item}" for i, item in enumerate(items))
print(formatted_items)  # "1. apple, 2. banana, 3. cherry"

# F-strings with dictionaries
# ✅ GOOD: Dictionary access
user = {"name": "Bob", "age": 30}
info = f"User: {user['name']}, Age: {user['age']}"
print(info)

# Nested f-strings
# ✅ GOOD: Nested expressions
width = 10
value = 42
formatted = f"Value: {value:{width}d}"  # "Value:         42"
```

### Performance Comparison
F-strings are faster than both `%` formatting and `.format()` because they're evaluated at runtime and don't require function calls.

### When to Use Each
- ✅ **F-strings**: Always prefer (Python 3.6+)
- ⚠️ **str.format**: Use when you need to reuse format strings
- ❌ **% formatting**: Legacy code only

---

## 3. Understand the Difference Between repr and str when Printing Objects

### Explanation
Python has two ways to represent objects as strings:
- **`str()`**: Human-readable representation (for end users)
- **`repr()`**: Developer-friendly representation (for debugging)

The `repr()` should ideally be valid Python code that could recreate the object.

### Use Cases
- Debugging and development
- Logging
- Displaying objects to users
- Creating string representations of custom classes
- Understanding object state

### Examples

```python
# Built-in types
text = "Hello\nWorld"
print(str(text))   # Human-readable: "Hello
                   # World"
print(repr(text))  # Developer-friendly: "'Hello\\nWorld'"

number = 42
print(str(number))   # "42"
print(repr(number))  # "42" (same for simple types)

# Lists
items = [1, 2, 3, "hello"]
print(str(items))   # "[1, 2, 3, 'hello']"
print(repr(items))  # "[1, 2, 3, 'hello']" (same for lists)

# Custom classes
# ❌ BAD: No __str__ or __repr__ defined
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("Alice", 25)
print(str(person))   # "<__main__.Person object at 0x...>"
print(repr(person))   # "<__main__.Person object at 0x...>"

# ✅ GOOD: Define both __str__ and __repr__
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        """Human-readable representation."""
        return f"{self.name}, {self.age} years old"
    
    def __repr__(self):
        """Developer-friendly representation (should be valid Python code)."""
        return f"Person(name={self.name!r}, age={self.age})"

person = Person("Alice", 25)
print(str(person))   # "Alice, 25 years old"
print(repr(person))  # "Person(name='Alice', age=25)"

# repr() should ideally recreate the object
person_repr = repr(person)
# Could potentially do: eval(person_repr) to recreate

# Special characters
text = "Hello\nWorld\tTab"
print(str(text))   # Shows actual newlines and tabs
print(repr(text))  # Shows escape sequences: "'Hello\\nWorld\\tTab'"

# Dates
from datetime import datetime
now = datetime.now()
print(str(now))   # "2024-01-15 10:30:45.123456"
print(repr(now))  # "datetime.datetime(2024, 1, 15, 10, 30, 45, 123456)"

# Using in f-strings
person = Person("Bob", 30)
print(f"User: {person}")        # Uses __str__: "User: Bob, 30 years old"
print(f"Debug: {person!r}")     # Uses __repr__: "Debug: Person(name='Bob', age=30)"
print(f"Debug: {person!s}")     # Explicitly uses __str__
```

### Key Rules
1. **`__str__`**: For end users, should be readable
2. **`__repr__`**: For developers, should be unambiguous and ideally recreate the object
3. **Fallback**: If `__str__` is not defined, Python uses `__repr__`
4. **Best practice**: Always define `__repr__`, optionally define `__str__`

---

## 4. Prefer Explicit String Concatenation over Implicit, Especially in Lists

### Explanation
String concatenation can be done in multiple ways:
- **Explicit**: Using `+` operator or `join()`
- **Implicit**: Automatic concatenation in some contexts

For multiple strings, `join()` is more efficient than repeated `+` operations.

### Use Cases
- Building strings from multiple parts
- Combining list elements into a string
- Creating formatted output
- Performance-critical string operations

### Examples

```python
# ✅ GOOD: Explicit concatenation with +
first = "Hello"
second = "World"
result = first + " " + second
print(result)  # "Hello World"

# ❌ BAD: Implicit concatenation (can be confusing)
# This works but is not recommended
text = "Hello" "World"  # Implicit concatenation
print(text)  # "HelloWorld"

# This is even more confusing
text = ("This is a long string that "
        "spans multiple lines using "
        "implicit concatenation")
print(text)

# ✅ BETTER: Explicit with parentheses and +
text = ("This is a long string that " +
        "spans multiple lines using " +
        "explicit concatenation")

# ✅ BEST: Using join() for multiple strings
# ❌ BAD: Repeated concatenation (inefficient)
words = ["Hello", "World", "Python"]
result = ""
for word in words:
    result += word + " "  # Creates new string each time!
print(result.strip())

# ✅ GOOD: Using join() (efficient)
words = ["Hello", "World", "Python"]
result = " ".join(words)
print(result)  # "Hello World Python"

# join() is much faster for many strings
# ❌ BAD: O(n²) time complexity
result = ""
for i in range(1000):
    result += str(i)  # Creates new string each iteration

# ✅ GOOD: O(n) time complexity
numbers = [str(i) for i in range(1000)]
result = "".join(numbers)

# Building strings with separators
# ✅ GOOD: join() with separator
items = ["apple", "banana", "cherry"]
csv_line = ",".join(items)  # "apple,banana,cherry"
path = "/".join(["usr", "local", "bin"])  # "usr/local/bin"

# Conditional joining
# ✅ GOOD: Filtering before joining
words = ["Hello", "", "World", None, "Python"]
# Filter out empty/None values
result = " ".join(word for word in words if word)
print(result)  # "Hello World Python"

# Formatting while joining
# ✅ GOOD: Formatting elements during join
numbers = [1, 2, 3, 4, 5]
formatted = ", ".join(f"#{n}" for n in numbers)
print(formatted)  # "#1, #2, #3, #4, #5"

# Building SQL queries (example)
# ✅ GOOD: Using join for SQL
columns = ["name", "age", "email"]
query = f"SELECT {', '.join(columns)} FROM users"
print(query)  # "SELECT name, age, email FROM users"

# Performance comparison
import time

# Method 1: Repeated concatenation
start = time.time()
result = ""
for i in range(10000):
    result += str(i)
time1 = time.time() - start

# Method 2: join()
start = time.time()
result = "".join(str(i) for i in range(10000))
time2 = time.time() - start

print(f"Concatenation: {time1:.4f}s")
print(f"Join: {time2:.4f}s")  # Much faster!
```

### Best Practices
1. **Use `join()`** for combining multiple strings (faster, more Pythonic)
2. **Use `+`** for simple concatenation of 2-3 strings
3. **Avoid** repeated `+` in loops (creates many temporary strings)
4. **Be explicit** - make concatenation clear and obvious

---

## 5. Know How to Slice Sequences

### Explanation
Slicing is a powerful Python feature for extracting subsequences from sequences (lists, strings, tuples). Syntax: `sequence[start:stop:step]`

- **start**: Inclusive beginning index (default: 0)
- **stop**: Exclusive ending index (default: end)
- **step**: Step size (default: 1)

### Use Cases
- Extracting substrings/subsequences
- Reversing sequences
- Getting every nth element
- Copying sequences
- Processing data in chunks

### Examples

```python
# Basic slicing
text = "Hello, World"
print(text[0:5])      # "Hello" (indices 0-4)
print(text[7:12])     # "World" (indices 7-11)
print(text[:5])       # "Hello" (from start to index 4)
print(text[7:])       # "World" (from index 7 to end)
print(text[:])        # "Hello, World" (entire string, creates copy)

# Negative indices
text = "Hello, World"
print(text[-5:])      # "World" (last 5 characters)
print(text[:-7])      # "Hello" (everything except last 7)
print(text[-12:-7])   # "Hello" (using negative indices)

# Step parameter
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(numbers[::2])   # [0, 2, 4, 6, 8] (every 2nd element)
print(numbers[1::2])  # [1, 3, 5, 7, 9] (every 2nd starting from 1)
print(numbers[::3])   # [0, 3, 6, 9] (every 3rd element)

# Reversing sequences
text = "Hello"
print(text[::-1])     # "olleH" (reversed)
numbers = [1, 2, 3, 4, 5]
print(numbers[::-1])  # [5, 4, 3, 2, 1]

# Copying (shallow copy)
original = [1, 2, 3, 4, 5]
copy = original[:]     # Creates new list
copy[0] = 99
print(original)        # [1, 2, 3, 4, 5] (unchanged)
print(copy)            # [99, 2, 3, 4, 5]

# Slicing lists
items = ["apple", "banana", "cherry", "date", "elderberry"]
print(items[1:4])     # ["banana", "cherry", "date"]
print(items[:3])      # ["apple", "banana", "cherry"]
print(items[2:])      # ["cherry", "date", "elderberry"]

# Out-of-bounds slicing (safe!)
text = "Hello"
print(text[0:100])    # "Hello" (doesn't raise error)
print(text[-100:5])   # "Hello" (doesn't raise error)

# Modifying slices
numbers = [0, 1, 2, 3, 4, 5]
numbers[1:4] = [10, 20, 30]  # Replace slice
print(numbers)        # [0, 10, 20, 30, 4, 5]

numbers = [0, 1, 2, 3, 4, 5]
numbers[1:4] = []     # Delete slice
print(numbers)        # [0, 4, 5]

# Advanced slicing patterns
data = list(range(20))
print(data[::2])           # Even indices: [0, 2, 4, 6, ...]
print(data[1::2])          # Odd indices: [1, 3, 5, 7, ...]
print(data[5:15:2])        # Every 2nd from index 5 to 15
print(data[-10::2])        # Every 2nd from last 10 elements

# String manipulation
email = "user@example.com"
username = email[:email.index("@")]      # "user"
domain = email[email.index("@")+1:]      # "example.com"

# Extracting file extensions
filename = "document.pdf"
extension = filename[filename.rfind(".")+1:]  # "pdf"
```

### Slicing Rules
1. **Indices**: Can be positive (from start) or negative (from end)
2. **Bounds**: Out-of-bounds indices don't raise errors
3. **Copying**: `sequence[:]` creates a shallow copy
4. **Reversing**: `sequence[::-1]` reverses the sequence
5. **Step**: Negative step reverses direction

---

## 6. Avoid Striding and Slicing in a Single Expression

### Explanation
While Python allows combining slicing and striding (step), it can make code hard to read and understand. It's often clearer to separate these operations or use alternative approaches.

### Use Cases
- Code readability
- Maintaining complex code
- Avoiding confusion
- Making intent clear

### Examples

```python
# ❌ BAD: Complex striding and slicing (hard to read)
data = list(range(20))
result = data[2:15:3]  # What does this do?
print(result)  # [2, 5, 8, 11, 14] - every 3rd from index 2 to 15

# ✅ GOOD: More explicit approach
data = list(range(20))
slice_data = data[2:15]  # First, get the slice
result = slice_data[::3]  # Then, stride through it
print(result)  # [2, 5, 8, 11, 14]

# ✅ BETTER: Use list comprehension for clarity
data = list(range(20))
result = [data[i] for i in range(2, 15, 3)]
print(result)  # [2, 5, 8, 11, 14] - clearer intent

# Another example
# ❌ BAD: Complex slicing with negative indices and stride
text = "Hello, World, Python, Programming"
result = text[-20:-1:2]  # Very confusing!

# ✅ GOOD: Break it down
text = "Hello, World, Python, Programming"
slice_text = text[-20:-1]  # Get the slice first
result = slice_text[::2]   # Then stride
print(result)

# ✅ BETTER: Use positive indices when possible
text = "Hello, World, Python, Programming"
start = len(text) - 20
end = len(text) - 1
result = text[start:end:2]  # More readable

# Real-world example: Processing data
# ❌ BAD: Complex expression
data = [i for i in range(100)]
processed = data[10:50:5][::-1]  # Hard to understand

# ✅ GOOD: Step by step
data = [i for i in range(100)]
slice1 = data[10:50:5]  # Every 5th from 10 to 50
processed = slice1[::-1]  # Reverse it
print(processed)

# ✅ BETTER: Use itertools for complex patterns
from itertools import islice
data = list(range(100))
# Get every 5th element from index 10 to 50, then reverse
processed = list(islice(data, 10, 50, 5))[::-1]

# When it's acceptable
# ✅ OK: Simple, common patterns
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
evens = numbers[::2]      # Simple, clear: every 2nd
reversed = numbers[::-1]  # Simple, clear: reversed
```

### Best Practices
1. **Separate operations** when combining slicing and striding
2. **Use list comprehensions** for complex patterns
3. **Add comments** if you must use complex slicing
4. **Prefer clarity** over brevity
5. **Use itertools** for advanced iteration patterns

---

## 7. Prefer Catch-All Unpacking over Slicing

### Explanation
Python 3 introduced extended unpacking with `*` operator, which is more readable and flexible than slicing for extracting parts of sequences. It clearly shows what you're extracting.

### Use Cases
- Extracting first/last elements
- Separating head and tail
- Processing structured data
- Making code more readable

### Examples

```python
# ❌ BAD: Using slicing
items = ["apple", "banana", "cherry", "date", "elderberry"]
first = items[0]
rest = items[1:]
print(first)  # "apple"
print(rest)   # ["banana", "cherry", "date", "elderberry"]

# ✅ GOOD: Using unpacking
items = ["apple", "banana", "cherry", "date", "elderberry"]
first, *rest = items
print(first)  # "apple"
print(rest)   # ["banana", "cherry", "date", "elderberry"]

# Extracting multiple elements
# ❌ BAD: Using slicing
items = [1, 2, 3, 4, 5, 6, 7, 8, 9]
first = items[0]
second = items[1]
rest = items[2:]
print(first, second, rest)

# ✅ GOOD: Using unpacking
items = [1, 2, 3, 4, 5, 6, 7, 8, 9]
first, second, *rest = items
print(first, second, rest)  # 1, 2, [3, 4, 5, 6, 7, 8, 9]

# Extracting from both ends
# ❌ BAD: Using slicing
items = [1, 2, 3, 4, 5, 6, 7, 8, 9]
first = items[0]
middle = items[1:-1]
last = items[-1]
print(first, middle, last)

# ✅ GOOD: Using unpacking
items = [1, 2, 3, 4, 5, 6, 7, 8, 9]
first, *middle, last = items
print(first, middle, last)  # 1, [2, 3, 4, 5, 6, 7, 8], 9

# Processing command-line arguments
# ✅ GOOD: Using unpacking
args = ["script.py", "arg1", "arg2", "arg3", "arg4"]
script_name, *arguments = args
print(f"Script: {script_name}")
print(f"Arguments: {arguments}")

# Parsing structured data
# ✅ GOOD: Unpacking tuples/lists
records = [
    ("Alice", 25, "Engineer", "New York"),
    ("Bob", 30, "Designer", "San Francisco"),
    ("Charlie", 22, "Developer", "Boston")
]

for name, age, *details in records:
    print(f"{name} ({age}): {details}")

# Handling variable-length data
# ✅ GOOD: Flexible unpacking
def process_data(*args):
    if len(args) >= 2:
        first, second, *rest = args
        print(f"First: {first}, Second: {second}, Rest: {rest}")
    else:
        print("Not enough arguments")

process_data(1, 2, 3, 4, 5)  # First: 1, Second: 2, Rest: [3, 4, 5]

# Ignoring parts of data
# ✅ GOOD: Using _ for ignored values
data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
first, *_, last = data  # Ignore middle values
print(first, last)  # 1, 9

# Nested unpacking
# ✅ GOOD: Complex unpacking patterns
data = [
    ("Alice", ["apple", "banana", "cherry"]),
    ("Bob", ["date", "elderberry"]),
    ("Charlie", ["fig"])
]

for name, (first_fruit, *other_fruits) in data:
    print(f"{name}: first={first_fruit}, others={other_fruits}")

# Edge cases
# ✅ GOOD: Handles empty sequences gracefully
items = [1]
first, *rest = items
print(first)  # 1
print(rest)   # [] (empty list, not error)

items = []
# first, *rest = items  # ValueError: not enough values to unpack

# Safe unpacking with defaults
items = []
first, *rest = items if items else [None]
print(first, rest)  # None, []

# Function return values
# ✅ GOOD: Unpacking function returns
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

data = [10, 20, 30, 40, 50]
minimum, maximum, *average = [get_stats(data)[0], get_stats(data)[1], get_stats(data)[2]]
# Better:
minimum, maximum, average = get_stats(data)
```

### Benefits of Unpacking
1. **Readability**: Clear intent of what you're extracting
2. **Flexibility**: Works with any iterable
3. **Safety**: Handles edge cases gracefully
4. **Pythonic**: More idiomatic Python code

### When to Use
- ✅ **Unpacking**: When you know the structure and want clarity
- ⚠️ **Slicing**: When you need specific indices or ranges
- ✅ **Both**: Can be combined for complex cases

---

## Summary

These seven principles help you work effectively with strings and sequences in Python:

1. **bytes vs str** - Understand when to use each for text vs binary data
2. **F-strings** - Prefer f-strings for string formatting (Python 3.6+)
3. **repr vs str** - Use repr for debugging, str for display
4. **String Concatenation** - Use `join()` for multiple strings, explicit `+` for simple cases
5. **Slicing** - Master sequence slicing for extracting subsequences
6. **Avoid Complex Slicing** - Keep slicing expressions simple and readable
7. **Catch-All Unpacking** - Prefer `*` unpacking over slicing when appropriate

Remember: **Clarity and readability should always be prioritized over cleverness.**
