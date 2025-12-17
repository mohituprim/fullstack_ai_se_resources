# Dictionaries: Effective Python Best Practices

## 1. Be Cautious when Relying on Dictionary Insertion Ordering

### Explanation
Python 3.7+ guarantees that dictionaries maintain insertion order. However, you should:
- Be aware of Python version requirements
- Understand that order is based on insertion, not key values
- Know when order matters vs when it doesn't
- Consider `OrderedDict` for explicit ordering needs

### Use Cases
- Maintaining order of operations
- Preserving data sequence
- Working with ordered data structures
- Understanding dictionary behavior

### Examples

```python
# Python 3.7+ maintains insertion order
# ✅ GOOD: Order is preserved
data = {}
data['first'] = 1
data['second'] = 2
data['third'] = 3
print(list(data.keys()))  # ['first', 'second', 'third']

# Order is based on insertion, not key values
# ✅ GOOD: Understanding insertion order
data = {}
data['zebra'] = 1
data['apple'] = 2
data['banana'] = 3
print(list(data.keys()))  # ['zebra', 'apple', 'banana'] - insertion order!

# ⚠️ CAUTION: Python < 3.7 doesn't guarantee order
# If you need order in older Python, use OrderedDict
from collections import OrderedDict

# ✅ GOOD: Explicit ordering with OrderedDict
ordered_data = OrderedDict()
ordered_data['first'] = 1
ordered_data['second'] = 2
ordered_data['third'] = 3
print(list(ordered_data.keys()))  # ['first', 'second', 'third']

# Order matters for iteration
# ✅ GOOD: Relying on order for processing
config = {}
config['database'] = 'postgresql'
config['host'] = 'localhost'
config['port'] = 5432

# Process in insertion order
for key, value in config.items():
    print(f"{key}: {value}")  # Guaranteed order in Python 3.7+

# When order doesn't matter
# ✅ GOOD: Using dict when order irrelevant
def count_words(text):
    word_count = {}
    for word in text.split():
        word_count[word] = word_count.get(word, 0) + 1
    return word_count  # Order doesn't matter for counting

# Merging dictionaries (Python 3.9+)
# ✅ GOOD: Preserving order in merges
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}
merged = {**dict1, **dict2}  # Order: a, b, c, d

# Reversing order
# ✅ GOOD: Creating reversed dictionary
original = {'a': 1, 'b': 2, 'c': 3}
reversed_dict = dict(reversed(list(original.items())))
print(reversed_dict)  # {'c': 3, 'b': 2, 'a': 1}
```

### Key Points
- **Python 3.7+**: Order guaranteed
- **Python < 3.7**: Use `OrderedDict` if order matters
- **Order is by insertion**, not by key values
- **Don't rely on order** unless you explicitly need it

---

## 2. Prefer get over in and KeyError to Handle Missing Dictionary Keys

### Explanation
Using `.get()` with a default value is cleaner and more Pythonic than checking `in` or catching `KeyError`. It's more readable and handles the common case of missing keys elegantly.

### Use Cases
- Accessing dictionary values safely
- Providing default values
- Avoiding KeyError exceptions
- Writing cleaner, more readable code

### Examples

```python
# ❌ BAD: Using 'in' check
data = {'name': 'Alice', 'age': 25}
if 'email' in data:
    email = data['email']
else:
    email = 'unknown@example.com'

# ❌ BAD: Using try/except
data = {'name': 'Alice', 'age': 25}
try:
    email = data['email']
except KeyError:
    email = 'unknown@example.com'

# ✅ GOOD: Using .get() with default
data = {'name': 'Alice', 'age': 25}
email = data.get('email', 'unknown@example.com')
print(email)  # 'unknown@example.com'

# Nested dictionaries
# ❌ BAD: Multiple 'in' checks
user = {
    'profile': {
        'contact': {
            'email': 'alice@example.com'
        }
    }
}

if 'profile' in user:
    if 'contact' in user['profile']:
        if 'email' in user['profile']['contact']:
            email = user['profile']['contact']['email']
        else:
            email = None
    else:
        email = None
else:
    email = None

# ✅ GOOD: Using .get() with chaining
email = user.get('profile', {}).get('contact', {}).get('email')
print(email)  # 'alice@example.com' or None

# ✅ BETTER: Using .get() with defaults
email = user.get('profile', {}).get('contact', {}).get('email', 'no-email@example.com')

# Counting with defaults
# ✅ GOOD: Using .get() for counters
word_count = {}
words = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']

for word in words:
    word_count[word] = word_count.get(word, 0) + 1
print(word_count)  # {'apple': 3, 'banana': 2, 'cherry': 1}

# Configuration with defaults
# ✅ GOOD: Using .get() for config
config = {'host': 'localhost', 'port': 5432}
database = config.get('database', 'postgresql')
timeout = config.get('timeout', 30)
debug = config.get('debug', False)

# When you need to know if key exists
# ✅ GOOD: Using .get() with None check
data = {'name': 'Alice'}
email = data.get('email')
if email is None:
    print("Email not provided")
else:
    print(f"Email: {email}")

# ✅ GOOD: Using 'in' when you only need to check existence
if 'email' in data:
    print("Email key exists")

# Default value types
# ✅ GOOD: Using appropriate defaults
settings = {}
max_retries = settings.get('max_retries', 3)  # int default
timeout = settings.get('timeout', 30.0)  # float default
enabled = settings.get('enabled', True)  # bool default
tags = settings.get('tags', [])  # list default (be careful - see next section!)
```

### Benefits
- **Cleaner code**: Less verbose than if/else or try/except
- **Readable**: Intent is clear
- **Safe**: No exceptions for missing keys
- **Flexible**: Easy to provide defaults

---

## 3. Prefer defaultdict over setdefault to Handle Missing Items in Internal State

### Explanation
`defaultdict` from collections is more efficient and cleaner than using `.setdefault()` repeatedly. It automatically creates default values for missing keys, making code more readable and performant.

### Use Cases
- Grouping items by key
- Building nested structures
- Counting occurrences
- Accumulating values

### Examples

```python
from collections import defaultdict

# ❌ BAD: Using setdefault (verbose and slower)
word_groups = {}
words = ['apple', 'banana', 'apricot', 'berry', 'avocado']

for word in words:
    first_letter = word[0]
    if first_letter not in word_groups:
        word_groups[first_letter] = []
    word_groups[first_letter].append(word)

# ❌ BAD: Using setdefault (better but still not ideal)
word_groups = {}
for word in words:
    first_letter = word[0]
    word_groups.setdefault(first_letter, []).append(word)

# ✅ GOOD: Using defaultdict
word_groups = defaultdict(list)
for word in words:
    first_letter = word[0]
    word_groups[first_letter].append(word)  # Automatically creates list if missing

print(dict(word_groups))  # {'a': ['apple', 'apricot', 'avocado'], 'b': ['banana', 'berry']}

# Counting
# ❌ BAD: Using regular dict with get
word_count = {}
words = ['apple', 'banana', 'apple', 'cherry']

for word in words:
    word_count[word] = word_count.get(word, 0) + 1

# ✅ GOOD: Using defaultdict with int
word_count = defaultdict(int)
for word in words:
    word_count[word] += 1  # Automatically starts at 0

print(dict(word_count))  # {'apple': 2, 'banana': 1, 'cherry': 1}

# Nested structures
# ✅ GOOD: Using defaultdict for nested dicts
nested_data = defaultdict(dict)
nested_data['user1']['name'] = 'Alice'
nested_data['user1']['age'] = 25
nested_data['user2']['name'] = 'Bob'
print(dict(nested_data))

# Grouping by multiple criteria
# ✅ GOOD: Complex grouping with defaultdict
students = [
    {'name': 'Alice', 'grade': 'A', 'subject': 'Math'},
    {'name': 'Bob', 'grade': 'B', 'subject': 'Math'},
    {'name': 'Charlie', 'grade': 'A', 'subject': 'Science'},
]

# Group by subject, then by grade
grouped = defaultdict(lambda: defaultdict(list))
for student in students:
    grouped[student['subject']][student['grade']].append(student['name'])

print(dict(grouped))
# {'Math': {'A': ['Alice'], 'B': ['Bob']}, 'Science': {'A': ['Charlie']}}

# Sets as defaults
# ✅ GOOD: Using defaultdict with set
tags_by_category = defaultdict(set)
items = [
    ('fruit', 'apple'),
    ('fruit', 'banana'),
    ('vegetable', 'carrot'),
    ('fruit', 'apple'),  # Duplicate
]

for category, item in items:
    tags_by_category[category].add(item)  # Set automatically created

print(dict(tags_by_category))
# {'fruit': {'apple', 'banana'}, 'vegetable': {'carrot'}}

# Custom default factory
# ✅ GOOD: Using callable for complex defaults
def create_user():
    return {'name': '', 'age': 0, 'scores': []}

users = defaultdict(create_user)
users['alice']['name'] = 'Alice'
users['alice']['age'] = 25
users['bob']['name'] = 'Bob'
print(dict(users))
```

### When to Use
- ✅ **defaultdict**: When you frequently add to missing keys
- ⚠️ **setdefault**: When you only occasionally need defaults
- ✅ **get()**: When you just need to read with defaults

### Performance
`defaultdict` is faster than `setdefault` because it doesn't need to check and set on every access - it automatically creates the default when the key is missing.

---

## 4. Know How to Construct Key-Dependent Default Values with __missing__

### Explanation
The `__missing__` method allows you to create custom default values that depend on the key being accessed. This is more powerful than `defaultdict` when defaults need to be computed based on the key.

### Use Cases
- Creating defaults based on key values
- Implementing custom dictionary behavior
- Lazy initialization
- Key-dependent computations

### Examples

```python
# ✅ GOOD: Custom dict with __missing__
class KeyDependentDict(dict):
    def __missing__(self, key):
        # Default value depends on the key
        if key.startswith('user_'):
            return {'type': 'user', 'id': key}
        elif key.startswith('admin_'):
            return {'type': 'admin', 'id': key}
        else:
            return {'type': 'unknown', 'id': key}

data = KeyDependentDict()
print(data['user_123'])  # {'type': 'user', 'id': 'user_123'}
print(data['admin_456'])  # {'type': 'admin', 'id': 'admin_456'}

# File extension mapping
# ✅ GOOD: Default based on file extension
class FileTypeDict(dict):
    def __missing__(self, key):
        extension = key.split('.')[-1] if '.' in key else 'unknown'
        mime_types = {
            'txt': 'text/plain',
            'pdf': 'application/pdf',
            'jpg': 'image/jpeg',
            'png': 'image/png',
        }
        return mime_types.get(extension, 'application/octet-stream')

file_types = FileTypeDict()
print(file_types['document.pdf'])  # 'application/pdf'
print(file_types['image.jpg'])     # 'image/jpeg'
print(file_types['unknown.xyz'])   # 'application/octet-stream'

# Lazy computation
# ✅ GOOD: Computing values on demand
class ComputedDict(dict):
    def __missing__(self, key):
        # Compute expensive value only when accessed
        value = self._compute_value(key)
        self[key] = value  # Cache it
        return value
    
    def _compute_value(self, key):
        # Simulate expensive computation
        return f"computed_{key}"

data = ComputedDict()
print(data['key1'])  # Computes and caches
print(data['key1'])  # Uses cached value

# Range-based defaults
# ✅ GOOD: Defaults based on numeric ranges
class RangeDict(dict):
    def __missing__(self, key):
        if isinstance(key, (int, float)):
            if key < 0:
                return 'negative'
            elif key < 10:
                return 'small'
            elif key < 100:
                return 'medium'
            else:
                return 'large'
        return 'unknown'

ranges = RangeDict()
print(ranges[5])   # 'small'
print(ranges[50])  # 'medium'
print(ranges[500]) # 'large'
print(ranges[-5])  # 'negative'

# Pattern matching
# ✅ GOOD: Defaults based on key patterns
class PatternDict(dict):
    def __missing__(self, key):
        import re
        if re.match(r'^\d+$', str(key)):
            return {'type': 'numeric', 'value': int(key)}
        elif re.match(r'^[A-Z]+$', str(key)):
            return {'type': 'uppercase', 'value': key}
        elif re.match(r'^[a-z]+$', str(key)):
            return {'type': 'lowercase', 'value': key}
        return {'type': 'mixed', 'value': key}

patterns = PatternDict()
print(patterns['123'])    # {'type': 'numeric', 'value': 123}
print(patterns['HELLO'])  # {'type': 'uppercase', 'value': 'HELLO'}
print(patterns['hello'])  # {'type': 'lowercase', 'value': 'hello'}
```

### Key Points
- `__missing__` is called when key is not found
- Can compute defaults based on key
- Can cache computed values
- More flexible than `defaultdict` for complex logic

---

## 5. Compose Classes Instead of Deeply Nesting Dictionaries, Lists, and Tuples

### Explanation
Deeply nested dictionaries become hard to read, maintain, and debug. Using classes (or dataclasses) provides:
- Better structure and organization
- Type safety and validation
- Easier to understand and maintain
- Better IDE support

### Use Cases
- Complex data structures
- Configuration objects
- API responses
- Data models
- Replacing nested dicts/lists

### Examples

```python
# ❌ BAD: Deeply nested dictionaries
user_data = {
    'profile': {
        'personal': {
            'name': 'Alice',
            'age': 25,
            'contact': {
                'email': 'alice@example.com',
                'phone': '123-456-7890',
                'address': {
                    'street': '123 Main St',
                    'city': 'New York',
                    'zip': '10001'
                }
            }
        },
        'settings': {
            'notifications': True,
            'theme': 'dark'
        }
    }
}

# Accessing is verbose and error-prone
email = user_data['profile']['personal']['contact']['email']
# What if any key is missing? KeyError!

# ✅ GOOD: Using classes
from dataclasses import dataclass
from typing import Optional

@dataclass
class Address:
    street: str
    city: str
    zip_code: str

@dataclass
class Contact:
    email: str
    phone: str
    address: Address

@dataclass
class PersonalInfo:
    name: str
    age: int
    contact: Contact

@dataclass
class Settings:
    notifications: bool
    theme: str

@dataclass
class Profile:
    personal: PersonalInfo
    settings: Settings

@dataclass
class User:
    profile: Profile

# Creating is clear and type-safe
user = User(
    profile=Profile(
        personal=PersonalInfo(
            name='Alice',
            age=25,
            contact=Contact(
                email='alice@example.com',
                phone='123-456-7890',
                address=Address(
                    street='123 Main St',
                    city='New York',
                    zip_code='10001'
                )
            )
        ),
        settings=Settings(
            notifications=True,
            theme='dark'
        )
    )
)

# Accessing is clear
email = user.profile.personal.contact.email
print(email)  # 'alice@example.com'

# With validation
# ✅ GOOD: Adding validation
@dataclass
class Contact:
    email: str
    phone: str
    address: Address
    
    def __post_init__(self):
        if '@' not in self.email:
            raise ValueError("Invalid email address")

# API response modeling
# ❌ BAD: Nested dict for API response
api_response = {
    'status': 'success',
    'data': {
        'users': [
            {'id': 1, 'name': 'Alice', 'scores': [85, 90, 88]},
            {'id': 2, 'name': 'Bob', 'scores': [92, 87, 91]}
        ]
    }
}

# ✅ GOOD: Using classes
@dataclass
class User:
    id: int
    name: str
    scores: list[int]

@dataclass
class UserData:
    users: list[User]

@dataclass
class APIResponse:
    status: str
    data: UserData

# Easier to work with
response = APIResponse(
    status='success',
    data=UserData(
        users=[
            User(id=1, name='Alice', scores=[85, 90, 88]),
            User(id=2, name='Bob', scores=[92, 87, 91])
        ]
    )
)

# Accessing is type-safe and clear
for user in response.data.users:
    avg_score = sum(user.scores) / len(user.scores)
    print(f"{user.name}: {avg_score:.1f}")

# Configuration objects
# ❌ BAD: Nested dict for config
config = {
    'database': {
        'host': 'localhost',
        'port': 5432,
        'credentials': {
            'username': 'admin',
            'password': 'secret'
        }
    },
    'cache': {
        'enabled': True,
        'ttl': 3600
    }
}

# ✅ GOOD: Using classes
@dataclass
class DatabaseCredentials:
    username: str
    password: str

@dataclass
class DatabaseConfig:
    host: str
    port: int
    credentials: DatabaseCredentials

@dataclass
class CacheConfig:
    enabled: bool
    ttl: int

@dataclass
class AppConfig:
    database: DatabaseConfig
    cache: CacheConfig

config = AppConfig(
    database=DatabaseConfig(
        host='localhost',
        port=5432,
        credentials=DatabaseCredentials(
            username='admin',
            password='secret'
        )
    ),
    cache=CacheConfig(
        enabled=True,
        ttl=3600
    )
)
```

### Benefits
- **Type safety**: IDE autocomplete and type checking
- **Readability**: Clear structure and relationships
- **Maintainability**: Easy to modify and extend
- **Validation**: Can add validation logic
- **Documentation**: Self-documenting code

---

## Summary

These five principles help you work effectively with dictionaries:

1. **Insertion Order** - Be aware of when order matters (Python 3.7+)
2. **get() method** - Prefer over 'in' checks or KeyError handling
3. **defaultdict** - Use for frequently adding to missing keys
4. **__missing__** - Implement for key-dependent defaults
5. **Classes over nested dicts** - Use dataclasses for complex structures

Remember: **Write clear, maintainable code that's easy to understand and debug.**
