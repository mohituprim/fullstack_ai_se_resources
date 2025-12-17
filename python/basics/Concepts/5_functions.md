# Functions: Effective Python Best Practices

## 1. Know That Function Arguments Can Be Mutated

### Explanation
Python passes arguments by object reference. Mutable objects (lists, dicts, sets) passed to functions can be modified, and changes persist after the function returns. Immutable objects (strings, tuples, numbers) cannot be changed.

### Use Cases
- Understanding function side effects
- Avoiding unexpected mutations
- Designing functions that modify data
- Preventing bugs from accidental mutations

### Examples

```python
# Mutable objects - CAN be modified
# ❌ BAD: Unexpected mutation
def add_item(items, item):
    items.append(item)  # Modifies original list!
    return items

my_list = [1, 2, 3]
result = add_item(my_list, 4)
print(my_list)  # [1, 2, 3, 4] - Original was modified!
print(result)   # [1, 2, 3, 4]

# ✅ GOOD: Explicit mutation (documented)
def add_item(items, item):
    """Adds item to the list. Modifies the original list."""
    items.append(item)
    return items

# ✅ GOOD: Avoid mutation (create new list)
def add_item(items, item):
    """Returns new list with item added. Original unchanged."""
    return items + [item]  # Creates new list

my_list = [1, 2, 3]
result = add_item(my_list, 4)
print(my_list)  # [1, 2, 3] - Original unchanged
print(result)   # [1, 2, 3, 4]

# Dictionaries
# ❌ BAD: Unexpected mutation
def update_user(user, key, value):
    user[key] = value  # Modifies original dict!
    return user

user_data = {'name': 'Alice', 'age': 25}
update_user(user_data, 'age', 26)
print(user_data)  # {'name': 'Alice', 'age': 26} - Modified!

# ✅ GOOD: Return new dict
def update_user(user, key, value):
    """Returns new dict with updated value. Original unchanged."""
    return {**user, key: value}  # Creates new dict

user_data = {'name': 'Alice', 'age': 25}
new_user = update_user(user_data, 'age', 26)
print(user_data)  # {'name': 'Alice', 'age': 25} - Unchanged
print(new_user)   # {'name': 'Alice', 'age': 26}

# Immutable objects - CANNOT be modified
# ✅ GOOD: Immutable objects are safe
def modify_string(text):
    text = text.upper()  # Creates new string, doesn't modify original
    return text

original = "hello"
result = modify_string(original)
print(original)  # "hello" - Unchanged
print(result)    # "HELLO"

# Default arguments - MUTABLE DEFAULTS ARE DANGEROUS!
# ❌ BAD: Mutable default argument
def add_item(item, items=[]):  # DANGER! Same list reused!
    items.append(item)
    return items

list1 = add_item(1)
list2 = add_item(2)
print(list1)  # [1, 2] - Unexpected!
print(list2)  # [1, 2] - Same list!

# ✅ GOOD: Use None as default
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

list1 = add_item(1)
list2 = add_item(2)
print(list1)  # [1] - Correct!
print(list2)  # [2] - Correct!
```

### Key Points
- **Mutable objects** (list, dict, set): Can be modified in functions
- **Immutable objects** (str, tuple, int): Cannot be modified
- **Default arguments**: Never use mutable defaults (use None)
- **Document mutations**: Make it clear if function modifies arguments

---

## 2. Return Dedicated Result Objects Instead of Requiring Function Callers to Unpack More Than Three Variables

### Explanation
When a function returns multiple values, unpacking more than 3 variables becomes error-prone and hard to remember. Use a dedicated class or dataclass to group related return values.

### Use Cases
- Functions returning multiple related values
- Improving code readability
- Reducing unpacking errors
- Making return values self-documenting

### Examples

```python
# ❌ BAD: Returning many values (hard to unpack correctly)
def process_data(data):
    min_val = min(data)
    max_val = max(data)
    avg_val = sum(data) / len(data)
    median_val = sorted(data)[len(data) // 2]
    std_dev = calculate_std_dev(data)
    return min_val, max_val, avg_val, median_val, std_dev

# Easy to get order wrong!
min_val, max_val, avg_val, median_val, std_dev = process_data([1, 2, 3, 4, 5])
# What if you forget the order? What does each value mean?

# ✅ GOOD: Using dataclass
from dataclasses import dataclass

@dataclass
class Statistics:
    minimum: float
    maximum: float
    average: float
    median: float
    standard_deviation: float

def process_data(data):
    return Statistics(
        minimum=min(data),
        maximum=max(data),
        average=sum(data) / len(data),
        median=sorted(data)[len(data) // 2],
        standard_deviation=calculate_std_dev(data)
    )

# Clear and self-documenting
stats = process_data([1, 2, 3, 4, 5])
print(f"Average: {stats.average}")
print(f"Min: {stats.minimum}, Max: {stats.maximum}")

# API response example
# ❌ BAD: Tuple unpacking
def fetch_user_data(user_id):
    user = get_user(user_id)
    permissions = get_permissions(user_id)
    settings = get_settings(user_id)
    return user, permissions, settings

user, perms, settings = fetch_user_data(123)
# What's the order? What does each value contain?

# ✅ GOOD: Using dataclass
@dataclass
class UserData:
    user: dict
    permissions: list
    settings: dict

def fetch_user_data(user_id):
    return UserData(
        user=get_user(user_id),
        permissions=get_permissions(user_id),
        settings=get_settings(user_id)
    )

data = fetch_user_data(123)
print(data.user['name'])
print(data.permissions)

# File processing example
# ❌ BAD: Multiple return values
def process_file(filename):
    lines = read_lines(filename)
    word_count = count_words(lines)
    char_count = count_chars(lines)
    errors = find_errors(lines)
    return lines, word_count, char_count, errors

# ✅ GOOD: Result object
@dataclass
class FileProcessResult:
    lines: list
    word_count: int
    char_count: int
    errors: list

def process_file(filename):
    lines = read_lines(filename)
    return FileProcessResult(
        lines=lines,
        word_count=count_words(lines),
        char_count=count_chars(lines),
        errors=find_errors(lines)
    )

result = process_file('data.txt')
print(f"Words: {result.word_count}, Errors: {len(result.errors)}")
```

### Benefits
- **Self-documenting**: Field names explain what values are
- **Type safety**: IDE autocomplete and type checking
- **Less error-prone**: No order to remember
- **Extensible**: Easy to add more fields later

---

## 3. Prefer Raising Exceptions to Returning None

### Explanation
Returning `None` to indicate errors forces callers to check for None everywhere, which is easy to forget and leads to AttributeError. Raising exceptions is more Pythonic and makes errors explicit.

### Use Cases
- Error handling
- Making failures explicit
- Preventing None-related bugs
- Following Python conventions

### Examples

```python
# ❌ BAD: Returning None for errors
def divide(a, b):
    if b == 0:
        return None  # Error case
    return a / b

result = divide(10, 0)
if result is None:
    print("Error: Division by zero")
else:
    print(f"Result: {result}")

# Easy to forget the check!
result = divide(10, 0)
print(result * 2)  # TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'

# ✅ GOOD: Raising exceptions
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

try:
    result = divide(10, 0)
except ValueError as e:
    print(f"Error: {e}")

# Or let it propagate
result = divide(10, 2)  # Works fine
print(result * 2)  # No None check needed

# Dictionary lookup
# ❌ BAD: Returning None
def get_user_email(user_id):
    user = users.get(user_id)
    if user:
        return user.get('email')
    return None  # Ambiguous: user not found or no email?

email = get_user_email(123)
if email:  # What if email is None vs user not found?
    send_email(email)

# ✅ GOOD: Raising exceptions
def get_user_email(user_id):
    if user_id not in users:
        raise KeyError(f"User {user_id} not found")
    user = users[user_id]
    if 'email' not in user:
        raise ValueError(f"User {user_id} has no email")
    return user['email']

try:
    email = get_user_email(123)
    send_email(email)
except KeyError as e:
    print(f"User error: {e}")
except ValueError as e:
    print(f"Data error: {e}")

# File operations
# ❌ BAD: Returning None
def read_config_file(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None  # Can't distinguish error types!

config = read_config_file('config.json')
if config is None:
    print("Error reading config")  # Which error?

# ✅ GOOD: Let exceptions propagate
def read_config_file(filename):
    with open(filename) as f:
        return json.load(f)
    # FileNotFoundError and JSONDecodeError propagate naturally

try:
    config = read_config_file('config.json')
except FileNotFoundError:
    print("Config file not found")
except json.JSONDecodeError:
    print("Invalid JSON in config file")
```

### When to Return None
- ✅ **Return None**: When "no value" is a valid, expected result (not an error)
- ❌ **Raise Exception**: When "no value" indicates an error or unexpected condition

---

## 4. Know How Closures Interact with Variable Scope and nonlocal

### Explanation
Closures capture variables from enclosing scope. Understanding `local`, `nonlocal`, and `global` scope is crucial for writing correct closure code.

### Use Cases
- Writing closures and nested functions
- Understanding variable scope
- Modifying outer scope variables
- Avoiding common closure pitfalls

### Examples

```python
# Closure basics
# ✅ GOOD: Closure captures outer variable
def outer_function(x):
    def inner_function(y):
        return x + y  # x is captured from outer scope
    return inner_function

add_five = outer_function(5)
print(add_five(3))  # 8

# Variable binding in loops - COMMON PITFALL!
# ❌ BAD: All closures reference same variable
functions = []
for i in range(3):
    functions.append(lambda: i)  # All capture same 'i'!

print([f() for f in functions])  # [2, 2, 2] - All return 2!

# ✅ GOOD: Capture value, not variable
functions = []
for i in range(3):
    functions.append(lambda i=i: i)  # Default argument captures value

print([f() for f in functions])  # [0, 1, 2] - Correct!

# ✅ BETTER: Use function factory
def make_function(value):
    return lambda: value

functions = [make_function(i) for i in range(3)]
print([f() for f in functions])  # [0, 1, 2]

# Modifying outer variables
# ❌ BAD: Can't modify outer variable directly
def counter():
    count = 0
    def increment():
        count += 1  # UnboundLocalError!
        return count
    return increment

# ✅ GOOD: Using nonlocal
def counter():
    count = 0
    def increment():
        nonlocal count  # Declare we're modifying outer variable
        count += 1
        return count
    return increment

c = counter()
print(c())  # 1
print(c())  # 2
print(c())  # 3

# Nested scopes
# ✅ GOOD: Understanding scope levels
def outer():
    x = "outer"
    def middle():
        x = "middle"
        def inner():
            nonlocal x  # Modifies middle's x
            x = "inner"
            return x
        inner()
        return x
    result = middle()
    return result, x

print(outer())  # ('inner', 'outer')

# Global vs nonlocal
# ✅ GOOD: Understanding global
count = 0  # Global variable

def increment_global():
    global count
    count += 1

def counter_local():
    count = 0  # Local variable
    def increment():
        nonlocal count  # Refers to counter_local's count
        count += 1
        return count
    return increment

increment_global()
print(count)  # 1 (global)

c = counter_local()
print(c())  # 1 (local to counter_local)
print(count)  # Still 1 (global unchanged)
```

### Scope Rules
- **Local**: Variables assigned in function (default)
- **nonlocal**: Variables in enclosing (non-global) scope
- **global**: Module-level variables
- **LEGB**: Local → Enclosing → Global → Built-in

---

## 5. Reduce Visual Noise with Variable Positional Arguments

### Explanation
`*args` allows functions to accept any number of positional arguments, making APIs more flexible and reducing the need for list arguments.

### Use Cases
- Functions accepting variable number of arguments
- Wrapper functions
- Flexible APIs
- Reducing visual noise

### Examples

```python
# ❌ BAD: Requiring list argument
def log_messages(messages):
    for msg in messages:
        print(f"LOG: {msg}")

log_messages(["Error occurred", "Warning: low memory", "Info: started"])

# ✅ GOOD: Using *args
def log_messages(*messages):
    for msg in messages:
        print(f"LOG: {msg}")

log_messages("Error occurred", "Warning: low memory", "Info: started")

# Sum function
# ✅ GOOD: Variable arguments
def sum_numbers(*numbers):
    return sum(numbers)

print(sum_numbers(1, 2, 3, 4, 5))  # 15
print(sum_numbers(10, 20))         # 30

# Formatting
# ✅ GOOD: Flexible formatting
def format_items(*items, separator=", "):
    return separator.join(str(item) for item in items)

print(format_items("apple", "banana", "cherry"))  # "apple, banana, cherry"
print(format_items(1, 2, 3, separator=" | "))    # "1 | 2 | 3"

# Wrapper functions
# ✅ GOOD: Passing through arguments
def debug_log(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        return func(*args, **kwargs)
    return wrapper

@debug_log
def add(a, b):
    return a + b

print(add(2, 3))  # Prints debug info, then returns 5
```

### Best Practices
- Use `*args` when number of arguments varies
- Keep `*args` after regular arguments
- Document what `*args` represents
- Consider type hints: `*args: int`

---

## 6. Provide Optional Behavior with Keyword Arguments

### Explanation
Keyword arguments make function calls more readable and allow optional parameters with defaults. They're essential for functions with many parameters.

### Use Cases
- Functions with optional parameters
- Improving call site readability
- Providing sensible defaults
- Making APIs more flexible

### Examples

```python
# ❌ BAD: Many positional arguments (hard to remember order)
def create_user(name, age, email, phone, city, country, active, admin):
    return {
        'name': name, 'age': age, 'email': email,
        'phone': phone, 'city': city, 'country': country,
        'active': active, 'admin': admin
    }

# Hard to remember order!
user = create_user("Alice", 25, "alice@example.com", "123-456", 
                   "NYC", "USA", True, False)

# ✅ GOOD: Using keyword arguments
def create_user(name, age, email, phone=None, city=None, 
                country="USA", active=True, admin=False):
    return {
        'name': name, 'age': age, 'email': email,
        'phone': phone, 'city': city, 'country': country,
        'active': active, 'admin': admin
    }

# Much clearer!
user = create_user(
    name="Alice",
    age=25,
    email="alice@example.com",
    city="NYC",
    active=True
)

# Configuration functions
# ✅ GOOD: Keyword arguments for config
def connect_database(host="localhost", port=5432, database="mydb",
                     username="admin", password="", ssl=False):
    print(f"Connecting to {host}:{port}/{database}")

# Flexible calls
connect_database()
connect_database(host="remote.server.com", port=3306)
connect_database(database="production", ssl=True)

# Mixing positional and keyword
# ✅ GOOD: Positional required, keyword optional
def send_email(to, subject, body, from_addr=None, cc=None, bcc=None):
    # to, subject, body are required (positional)
    # from_addr, cc, bcc are optional (keyword)
    pass

send_email("user@example.com", "Hello", "Message body")
send_email("user@example.com", "Hello", "Message body", 
           from_addr="sender@example.com", cc=["cc@example.com"])
```

### Benefits
- **Readability**: Clear what each argument means
- **Flexibility**: Easy to add new optional parameters
- **Defaults**: Sensible defaults reduce boilerplate
- **Order independence**: Can specify in any order

---

## 7. Use None and Docstrings to Specify Dynamic Default Arguments

### Explanation
Mutable default arguments are dangerous (shared across calls). Use `None` as default and create new objects inside the function. Document this pattern clearly.

### Use Cases
- Avoiding mutable default argument bugs
- Creating fresh objects per call
- Documenting default behavior
- Writing safe functions

### Examples

```python
# ❌ BAD: Mutable default (DANGEROUS!)
def process_items(items, processed=[]):  # Same list reused!
    processed.append("processed")
    return processed

list1 = process_items([1, 2, 3])
list2 = process_items([4, 5, 6])
print(list1)  # ['processed', 'processed'] - Wrong!
print(list2)  # ['processed', 'processed'] - Same list!

# ✅ GOOD: Use None as default
def process_items(items, processed=None):
    """
    Process items and optionally append to processed list.
    
    Args:
        items: List of items to process
        processed: Optional list to append to. If None, creates new list.
    
    Returns:
        List of processed items
    """
    if processed is None:
        processed = []
    processed.append("processed")
    return processed

list1 = process_items([1, 2, 3])
list2 = process_items([4, 5, 6])
print(list1)  # ['processed'] - Correct!
print(list2)  # ['processed'] - New list!

# Timestamp example
# ❌ BAD: Mutable default
def log_event(message, timestamp=datetime.now()):  # Same timestamp!
    return f"{timestamp}: {message}"

# ✅ GOOD: None default
def log_event(message, timestamp=None):
    """
    Log an event with optional timestamp.
    
    Args:
        message: Event message
        timestamp: Optional datetime. If None, uses current time.
    """
    if timestamp is None:
        timestamp = datetime.now()
    return f"{timestamp}: {message}"

# Dictionary defaults
# ✅ GOOD: None for dict defaults
def update_config(key, value, config=None):
    """
    Update configuration dictionary.
    
    Args:
        key: Configuration key
        value: Configuration value
        config: Optional config dict. If None, creates new dict.
    """
    if config is None:
        config = {}
    config[key] = value
    return config
```

### Pattern
1. Use `None` as default
2. Check `if arg is None:`
3. Create new object inside function
4. Document in docstring

---

## 8. Enforce Clarity with Keyword-Only and Positional-Only Arguments

### Explanation
Python 3 allows you to enforce keyword-only arguments (after `*`) and positional-only arguments (before `/`). This makes APIs clearer and prevents mistakes.

### Use Cases
- Preventing argument order mistakes
- Making APIs more explicit
- Improving code clarity
- Enforcing usage patterns

### Examples

```python
# Keyword-only arguments (after *)
# ✅ GOOD: Force keyword usage for clarity
def safe_divide(numerator, denominator, *, ignore_zero=False):
    """
    Divide two numbers.
    
    Args:
        numerator: Number to divide
        denominator: Number to divide by
        ignore_zero: If True, returns 0 instead of raising error
    """
    if denominator == 0:
        if ignore_zero:
            return 0
        raise ValueError("Cannot divide by zero")
    return numerator / denominator

# Must use keyword for ignore_zero
result = safe_divide(10, 2, ignore_zero=True)  # OK
# result = safe_divide(10, 2, True)  # TypeError!

# Positional-only arguments (before /)
# ✅ GOOD: Force positional usage
def pow(x, y, /, mod=None):
    """
    Power function with positional-only base and exponent.
    
    Args:
        x: Base (positional only)
        y: Exponent (positional only)
        mod: Optional modulus (keyword allowed)
    """
    result = x ** y
    if mod is not None:
        result %= mod
    return result

# Must use positional for x, y
result = pow(2, 3, mod=5)  # OK
# result = pow(x=2, y=3)  # TypeError!

# Combined
# ✅ GOOD: Both positional-only and keyword-only
def process_data(data, /, *, validate=True, format="json"):
    """
    Process data with enforced argument style.
    
    Args:
        data: Input data (positional only)
        validate: Whether to validate (keyword only)
        format: Output format (keyword only)
    """
    if validate:
        # validate data
        pass
    # process with format
    return processed_data

# Usage
result = process_data(my_data, validate=True, format="xml")
# result = process_data(data=my_data)  # TypeError!
# result = process_data(my_data, True, "xml")  # TypeError!
```

### Benefits
- **Clarity**: Makes function calls more explicit
- **Safety**: Prevents argument order mistakes
- **Documentation**: Self-documenting API design
- **Flexibility**: Can evolve API without breaking changes

---

## 9. Define Function Decorators with functools.wraps

### Explanation
When creating decorators, use `@functools.wraps` to preserve the original function's metadata (name, docstring, etc.). Without it, decorated functions lose their identity.

### Use Cases
- Writing decorators
- Preserving function metadata
- Debugging and introspection
- Maintaining function identity

### Examples

```python
from functools import wraps

# ❌ BAD: Decorator without wraps
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Greet someone."""
    return f"Hello, {name}!"

print(greet.__name__)   # "wrapper" - Wrong!
print(greet.__doc__)    # None - Lost!

# ✅ GOOD: Using functools.wraps
def my_decorator(func):
    @wraps(func)  # Preserves metadata
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Greet someone."""
    return f"Hello, {name}!"

print(greet.__name__)   # "greet" - Correct!
print(greet.__doc__)    # "Greet someone." - Preserved!

# Timing decorator
# ✅ GOOD: Preserving metadata
import time
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def slow_function():
    """This function is slow."""
    time.sleep(1)
    return "Done"

# Metadata preserved
print(slow_function.__name__)  # "slow_function"
print(slow_function.__doc__)   # "This function is slow."
```

### Why It Matters
- **Debugging**: Stack traces show correct function names
- **Introspection**: Tools can see original function info
- **Documentation**: Docstrings are preserved
- **Identity**: Function maintains its original identity

---

## 10. Prefer functools.partial over lambda Expressions for Glue Functions

### Explanation
`functools.partial` creates new functions with some arguments pre-filled. It's more readable and debuggable than lambda expressions for this purpose.

### Use Cases
- Creating specialized functions
- Reducing repetition
- Improving readability
- Function composition

### Examples

```python
from functools import partial

# ❌ BAD: Using lambda (less readable)
def multiply(x, y):
    return x * y

double = lambda x: multiply(2, x)
triple = lambda x: multiply(3, x)

# ✅ GOOD: Using partial
double = partial(multiply, 2)
triple = partial(multiply, 3)

print(double(5))   # 10
print(triple(5))   # 15

# Multiple arguments
# ❌ BAD: Lambda with multiple args
def power(base, exponent, modulus=None):
    result = base ** exponent
    if modulus:
        result %= modulus
    return result

square = lambda x: power(x, 2)
cube = lambda x: power(x, 3)

# ✅ GOOD: Partial is clearer
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

# Function composition
# ✅ GOOD: Using partial for callbacks
def process_data(data, transform, validate=True):
    if validate:
        # validate
        pass
    return transform(data)

# Create specialized processors
process_strict = partial(process_data, validate=True)
process_fast = partial(process_data, validate=False)

# Sorting
# ✅ GOOD: Partial for key functions
from operator import itemgetter

data = [('Alice', 25), ('Bob', 30), ('Charlie', 22)]
sort_by_age = partial(sorted, key=itemgetter(1))
print(sort_by_age(data))  # Sorted by age

# When lambda is still appropriate
# ✅ GOOD: Lambda for simple, one-off functions
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
# Lambda is fine here - simple and clear

# But partial can be better for reuse
square_func = partial(pow, y=2)
squared = list(map(square_func, numbers))
```

### When to Use
- ✅ **partial**: When creating reusable specialized functions
- ✅ **lambda**: For simple, one-off transformations
- ✅ **partial**: When you want better debugging (shows function name)
- ✅ **lambda**: When expression is very simple and inline

---

## Summary

These ten principles help you write effective functions:

1. **Argument Mutation** - Understand that mutable arguments can be modified
2. **Result Objects** - Use dataclasses for multiple return values
3. **Exceptions over None** - Raise exceptions for errors, not None
4. **Closures and Scope** - Understand local, nonlocal, global
5. **Variable Arguments** - Use *args for flexibility
6. **Keyword Arguments** - Use for optional parameters
7. **None Defaults** - Use None for mutable defaults
8. **Argument Enforcement** - Use / and * for clarity
9. **functools.wraps** - Preserve metadata in decorators
10. **partial over lambda** - Prefer partial for glue functions

Remember: **Write functions that are clear, safe, and easy to use correctly.**
