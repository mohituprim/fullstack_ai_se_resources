# Classes and Interfaces: Effective Python Best Practices

## 1. Accept Functions Instead of Classes for Simple Interfaces

### Explanation
Python's first-class functions mean you can often use simple functions instead of creating classes with a single method. This reduces boilerplate and makes code more Pythonic.

### Use Cases
- Simple callable interfaces
- Strategy pattern
- Callback functions
- Replacing single-method classes

### Examples

```python
# ❌ BAD: Class with single method (unnecessary)
class Sorter:
    def __init__(self, reverse=False):
        self.reverse = reverse
    
    def sort(self, items):
        return sorted(items, reverse=self.reverse)

sorter = Sorter(reverse=True)
result = sorter.sort([3, 1, 4, 1, 5])

# ✅ GOOD: Simple function
def sort_items(items, reverse=False):
    return sorted(items, reverse=reverse)

result = sort_items([3, 1, 4, 1, 5], reverse=True)

# Strategy pattern
# ❌ BAD: Class-based strategy
class DiscountStrategy:
    def calculate(self, price):
        raise NotImplementedError

class RegularDiscount(DiscountStrategy):
    def calculate(self, price):
        return price * 0.9

class VIPDiscount(DiscountStrategy):
    def calculate(self, price):
        return price * 0.8

# ✅ GOOD: Function-based strategy
def regular_discount(price):
    return price * 0.9

def vip_discount(price):
    return price * 0.8

# Use directly
def apply_discount(price, discount_func):
    return discount_func(price)

result = apply_discount(100, vip_discount)

# Callbacks
# ❌ BAD: Class for callback
class EventHandler:
    def handle(self, event):
        print(f"Handling {event}")

handler = EventHandler()
register_callback(handler.handle)

# ✅ GOOD: Function callback
def handle_event(event):
    print(f"Handling {event}")

register_callback(handle_event)

# When classes are appropriate
# ✅ GOOD: Class when you need state
class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
        return self.count

# ✅ GOOD: Class when you need multiple related methods
class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def validate(self):
        # validation logic
        pass
    
    def transform(self):
        # transformation logic
        pass
    
    def save(self):
        # save logic
        pass
```

### When to Use
- ✅ **Functions**: Simple, stateless operations
- ✅ **Classes**: When you need state or multiple related methods

---

## 2. Prefer Object-Oriented Polymorphism over Functions with isinstance Checks

### Explanation
Using `isinstance()` checks to handle different types is fragile and violates the open/closed principle. Use polymorphism - let objects handle their own behavior through methods.

### Use Cases
- Handling different types
- Extensible design
- Avoiding type checking
- Following OOP principles

### Examples

```python
# ❌ BAD: Using isinstance checks
def process_animal(animal):
    if isinstance(animal, Dog):
        return animal.bark()
    elif isinstance(animal, Cat):
        return animal.meow()
    elif isinstance(animal, Bird):
        return animal.tweet()
    else:
        raise TypeError("Unknown animal")

# Adding new animal requires modifying this function!

# ✅ GOOD: Polymorphism
class Animal:
    def make_sound(self):
        raise NotImplementedError

class Dog(Animal):
    def make_sound(self):
        return "Woof!"

class Cat(Animal):
    def make_sound(self):
        return "Meow!"

class Bird(Animal):
    def make_sound(self):
        return "Tweet!"

def process_animal(animal):
    return animal.make_sound()  # Works for any Animal!

# Adding new animals doesn't require changing process_animal

# Shape example
# ❌ BAD: Type checking
def calculate_area(shape):
    if isinstance(shape, Circle):
        return 3.14159 * shape.radius ** 2
    elif isinstance(shape, Rectangle):
        return shape.width * shape.height
    elif isinstance(shape, Triangle):
        return 0.5 * shape.base * shape.height

# ✅ GOOD: Polymorphism
class Shape:
    def area(self):
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

def calculate_area(shape):
    return shape.area()  # Works for any Shape!

# File processing
# ❌ BAD: Type checking
def process_file(file_obj):
    if isinstance(file_obj, TextFile):
        return file_obj.read_text()
    elif isinstance(file_obj, ImageFile):
        return file_obj.read_image()
    elif isinstance(file_obj, AudioFile):
        return file_obj.read_audio()

# ✅ GOOD: Polymorphism
class File:
    def read(self):
        raise NotImplementedError

class TextFile(File):
    def read(self):
        return self.read_text()

class ImageFile(File):
    def read(self):
        return self.read_image()

def process_file(file_obj):
    return file_obj.read()
```

### Benefits
- **Extensible**: Add new types without modifying existing code
- **Maintainable**: Each class handles its own behavior
- **Testable**: Easy to test each class independently
- **Pythonic**: Follows duck typing principles

---

## 3. Consider functools.singledispatch for Functional-Style Programming Instead of Object-Oriented Polymorphism

### Explanation
`functools.singledispatch` provides function-based polymorphism. It's useful when you can't modify classes or prefer functional style over OOP.

### Use Cases
- Working with built-in types
- Functional programming style
- When you can't modify classes
- Type-based function overloading

### Examples

```python
from functools import singledispatch

# ✅ GOOD: Using singledispatch
@singledispatch
def process(data):
    raise TypeError(f"Unsupported type: {type(data)}")

@process.register
def _(data: str):
    return f"Processing string: {data}"

@process.register
def _(data: int):
    return f"Processing integer: {data * 2}"

@process.register
def _(data: list):
    return f"Processing list with {len(data)} items"

print(process("hello"))     # "Processing string: hello"
print(process(42))          # "Processing integer: 84"
print(process([1, 2, 3]))  # "Processing list with 3 items"

# JSON serialization example
# ✅ GOOD: singledispatch for serialization
@singledispatch
def to_json(obj):
    raise TypeError(f"Cannot serialize {type(obj)}")

@to_json.register
def _(obj: dict):
    return "{" + ", ".join(f'"{k}": {to_json(v)}' for k, v in obj.items()) + "}"

@to_json.register
def _(obj: list):
    return "[" + ", ".join(to_json(item) for item in obj) + "]"

@to_json.register
def _(obj: str):
    return f'"{obj}"'

@to_json.register
def _(obj: (int, float)):
    return str(obj)

@to_json.register
def _(obj: bool):
    return "true" if obj else "false"

@to_json.register
def _(obj: type(None)):
    return "null"

# When to use
# ✅ Use singledispatch when:
# - Working with built-in types
# - Can't modify classes
# - Prefer functional style
# - Need type-based dispatch

# ✅ Use polymorphism when:
# - You control the classes
# - Want to encapsulate behavior
# - Need state with behavior
```

### Benefits
- **Flexible**: Works with any types
- **Functional**: Function-based approach
- **Extensible**: Easy to add new type handlers
- **Clean**: No isinstance checks needed

---

## 4. Prefer dataclasses for Defining Lightweight Classes

### Explanation
`dataclasses` (Python 3.7+) automatically generate common methods like `__init__`, `__repr__`, `__eq__`, reducing boilerplate for simple data classes.

### Use Cases
- Data containers
- Configuration objects
- Simple value objects
- Reducing boilerplate

### Examples

```python
from dataclasses import dataclass

# ❌ BAD: Manual class with boilerplate
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

# ✅ GOOD: Using dataclass
@dataclass
class Point:
    x: float
    y: float

# Automatically gets __init__, __repr__, __eq__, etc.!

p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
print(p1)        # Point(x=1.0, y=2.0)
print(p1 == p2)   # True

# With defaults
@dataclass
class User:
    name: str
    age: int
    email: str = ""
    active: bool = True

user = User("Alice", 25)
print(user)  # User(name='Alice', age=25, email='', active=True)

# With methods
@dataclass
class Rectangle:
    width: float
    height: float
    
    def area(self):
        return self.width * self.height

rect = Rectangle(10, 5)
print(rect.area())  # 50

# Field customization
from dataclasses import field

@dataclass
class Inventory:
    items: list = field(default_factory=list)
    total: float = 0.0

# Comparison
@dataclass(order=True)
class Person:
    name: str
    age: int

people = [Person("Bob", 30), Person("Alice", 25)]
sorted_people = sorted(people)  # Sorted by fields in order
```

### Benefits
- **Less boilerplate**: Auto-generates common methods
- **Type hints**: Encourages type annotations
- **Readable**: Clear, concise syntax
- **Maintainable**: Easy to add fields

---

## 5. Use @classmethod Polymorphism to Construct Objects Generically

### Explanation
`@classmethod` allows alternative constructors, enabling polymorphic object creation. Different subclasses can have different construction logic.

### Use Cases
- Alternative constructors
- Factory methods
- Polymorphic construction
- Flexible object creation

### Examples

```python
# ✅ GOOD: Using @classmethod for alternative constructors
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    @classmethod
    def from_string(cls, date_string):
        """Create Date from 'YYYY-MM-DD' string."""
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)
    
    @classmethod
    def from_timestamp(cls, timestamp):
        """Create Date from Unix timestamp."""
        from datetime import datetime
        dt = datetime.fromtimestamp(timestamp)
        return cls(dt.year, dt.month, dt.day)
    
    def __repr__(self):
        return f"Date({self.year}, {self.month}, {self.day})"

# Different ways to create
date1 = Date(2024, 1, 15)
date2 = Date.from_string("2024-01-15")
date3 = Date.from_timestamp(1705276800)

# Polymorphic construction
# ✅ GOOD: Each subclass can have different construction
class Animal:
    @classmethod
    def create(cls, animal_type, *args, **kwargs):
        """Factory method for creating animals."""
        if animal_type == "dog":
            return Dog(*args, **kwargs)
        elif animal_type == "cat":
            return Cat(*args, **kwargs)
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")

class Dog(Animal):
    def __init__(self, name):
        self.name = name

class Cat(Animal):
    def __init__(self, name, lives=9):
        self.name = name
        self.lives = lives

# Generic construction
dog = Animal.create("dog", "Rex")
cat = Animal.create("cat", "Fluffy", lives=7)

# Database models
# ✅ GOOD: Different construction methods
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['email'])
    
    @classmethod
    def from_database(cls, user_id):
        # Fetch from database
        data = fetch_user_from_db(user_id)
        return cls.from_dict(data)
```

### Benefits
- **Flexible**: Multiple ways to create objects
- **Polymorphic**: Works with inheritance
- **Clear**: Explicit alternative constructors
- **Maintainable**: Easy to add new construction methods

---

## 6. Initialize Parent Classes with super

### Explanation
Always use `super()` to call parent class methods. It handles method resolution order (MRO) correctly and works with multiple inheritance.

### Use Cases
- Calling parent class methods
- Multiple inheritance
- Maintaining MRO
- Future-proofing code

### Examples

```python
# ❌ BAD: Direct parent class call
class Parent:
    def __init__(self, name):
        self.name = name

class Child(Parent):
    def __init__(self, name, age):
        Parent.__init__(self, name)  # Hard-coded parent
        self.age = age

# Breaks with multiple inheritance!

# ✅ GOOD: Using super()
class Parent:
    def __init__(self, name):
        self.name = name

class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)  # Uses MRO
        self.age = age

# Multiple inheritance
# ✅ GOOD: super() handles MRO correctly
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        print("B")
        super().method()

class C(A):
    def method(self):
        print("C")
        super().method()

class D(B, C):
    def method(self):
        print("D")
        super().method()

d = D()
d.method()
# Output:
# D
# B
# C
# A
# (Correct MRO: D -> B -> C -> A)

# ❌ BAD: Direct calls break MRO
class D(B, C):
    def method(self):
        print("D")
        B.method(self)  # Skips C!
        C.method(self)

# With arguments
# ✅ GOOD: super() with arguments
class Parent:
    def __init__(self, name, **kwargs):
        self.name = name
        super().__init__(**kwargs)  # Pass through to object

class Child(Parent):
    def __init__(self, name, age, **kwargs):
        self.age = age
        super().__init__(name, **kwargs)
```

### Benefits
- **MRO correct**: Handles method resolution order
- **Multiple inheritance**: Works with complex hierarchies
- **Future-proof**: Adapts if class hierarchy changes
- **Pythonic**: Standard way to call parent methods

---

## 7. Consider Composing Functionality with Mix-in Classes

### Explanation
Mix-ins are classes designed to be inherited alongside other classes to add functionality. They're useful for code reuse without deep inheritance hierarchies.

### Use Cases
- Adding optional functionality
- Code reuse
- Avoiding deep inheritance
- Composing behaviors

### Examples

```python
# ✅ GOOD: Using mix-ins
class SerializableMixin:
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()}
    
    def to_json(self):
        import json
        return json.dumps(self.to_dict())

class TimestampMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from datetime import datetime
        self.created_at = datetime.now()

class User(SerializableMixin, TimestampMixin):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        super().__init__()  # Initialize mix-ins

user = User("Alice", "alice@example.com")
print(user.to_dict())      # Has serialization
print(user.created_at)     # Has timestamp

# Logging mix-in
# ✅ GOOD: Adding logging capability
class LoggableMixin:
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")

class Database(LoggableMixin):
    def connect(self):
        self.log("Connecting to database")
        # connection logic

class API(LoggableMixin):
    def request(self, endpoint):
        self.log(f"Requesting {endpoint}")
        # request logic

# Comparison mix-in
# ✅ GOOD: Adding comparison operators
class ComparableMixin:
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __lt__(self, other):
        return self.value < other.value

class Product(ComparableMixin):
    def __init__(self, name, price):
        self.name = name
        self.value = price  # For comparison
```

### Best Practices
- **Single responsibility**: Each mix-in adds one feature
- **No __init__ conflicts**: Use `**kwargs` pattern
- **Document dependencies**: Make mix-in requirements clear
- **Use sparingly**: Don't overuse mix-ins

---

## 8. Prefer Public Attributes over Private Ones

### Explanation
Python doesn't have true private attributes. The `_` prefix is a convention, and `__` name mangling is rarely needed. Prefer public attributes and document their usage.

### Use Cases
- Simple data access
- Avoiding unnecessary complexity
- Following Python conventions
- Making code more accessible

### Examples

```python
# ❌ BAD: Unnecessary "private" attributes
class User:
    def __init__(self, name):
        self.__name = name  # Name mangling - rarely needed
    
    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name

# ✅ GOOD: Public attributes
class User:
    def __init__(self, name):
        self.name = name  # Public - Pythonic

user = User("Alice")
print(user.name)  # Direct access
user.name = "Bob"  # Direct assignment

# When to use _ (protected)
# ✅ GOOD: Convention for "internal use"
class User:
    def __init__(self, name):
        self.name = name
        self._internal_cache = {}  # Convention: internal use
    
    def process(self):
        # Uses _internal_cache
        pass

# When to use __ (name mangling)
# ✅ GOOD: Avoiding name conflicts in inheritance
class Base:
    def __init__(self):
        self.__private = "base"  # Becomes _Base__private

class Derived(Base):
    def __init__(self):
        super().__init__()
        self.__private = "derived"  # Becomes _Derived__private
        # No conflict!

# Property for computed attributes
# ✅ GOOD: Use @property when you need logic
class Circle:
    def __init__(self, radius):
        self.radius = radius  # Public
    
    @property
    def area(self):
        return 3.14159 * self.radius ** 2  # Computed

circle = Circle(5)
print(circle.radius)  # 5
print(circle.area)    # 78.54 (computed)
```

### Python Philosophy
- **"We're all consenting adults"**: Trust users to use attributes correctly
- **Documentation over enforcement**: Document intended usage
- **Simplicity**: Avoid unnecessary complexity

---

## 9. Prefer dataclasses for Creating Immutable Objects

### Explanation
Dataclasses with `frozen=True` create immutable objects (like named tuples but with more features). They're perfect for value objects that shouldn't change.

### Use Cases
- Value objects
- Immutable data structures
- Functional programming
- Thread-safe objects

### Examples

```python
from dataclasses import dataclass

# ❌ BAD: Mutable by default
@dataclass
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
p.x = 3.0  # Can modify - might not be desired

# ✅ GOOD: Immutable with frozen=True
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
# p.x = 3.0  # FrozenInstanceError!

# Creating new instances
# ✅ GOOD: Create new instead of modifying
@dataclass(frozen=True)
class Point:
    x: float
    y: float
    
    def move(self, dx, dy):
        return Point(self.x + dx, self.y + dy)

p1 = Point(1.0, 2.0)
p2 = p1.move(3.0, 4.0)  # New instance
print(p2)  # Point(x=4.0, y=6.0)

# Hashable (can use in sets/dicts)
# ✅ GOOD: Immutable objects are hashable
@dataclass(frozen=True)
class User:
    name: str
    email: str

users = {User("Alice", "alice@example.com")}  # Can use in set
user_dict = {User("Bob", "bob@example.com"): "data"}  # Can use as key

# Comparison
# ✅ GOOD: Immutable objects can be compared
@dataclass(frozen=True, order=True)
class Product:
    name: str
    price: float

products = [
    Product("B", 20),
    Product("A", 10),
    Product("C", 30)
]
sorted_products = sorted(products)  # Sorted by name, then price
```

### Benefits
- **Thread-safe**: Can't be modified after creation
- **Hashable**: Can use in sets and as dict keys
- **Predictable**: Value never changes
- **Functional**: Aligns with functional programming

---

## 10. Inherit from collections.abc Classes for Custom Container Types

### Explanation
The `collections.abc` module provides abstract base classes for containers. Inheriting from them ensures your custom containers work correctly with Python's built-in functions.

### Use Cases
- Custom container types
- Ensuring protocol compliance
- Making containers work with built-ins
- Type checking

### Examples

```python
from collections.abc import Sequence, MutableSequence, Mapping

# ✅ GOOD: Inheriting from Sequence
class MyList(Sequence):
    def __init__(self, items):
        self._items = list(items)
    
    def __getitem__(self, index):
        return self._items[index]
    
    def __len__(self):
        return len(self._items)
    
    # Sequence provides: __contains__, __iter__, __reversed__, index, count

my_list = MyList([1, 2, 3, 4, 5])
print(3 in my_list)        # True (from Sequence)
print(my_list.index(3))   # 2 (from Sequence)
print(list(reversed(my_list)))  # [5, 4, 3, 2, 1] (from Sequence)

# Mutable sequence
# ✅ GOOD: Inheriting from MutableSequence
class Stack(MutableSequence):
    def __init__(self):
        self._items = []
    
    def __getitem__(self, index):
        return self._items[index]
    
    def __setitem__(self, index, value):
        self._items[index] = value
    
    def __delitem__(self, index):
        del self._items[index]
    
    def __len__(self):
        return len(self._items)
    
    def insert(self, index, value):
        self._items.insert(index, value)
    
    # MutableSequence provides: append, reverse, extend, pop, remove, etc.

stack = Stack()
stack.append(1)
stack.append(2)
stack.append(3)
print(list(stack))  # [1, 2, 3]

# Custom mapping
# ✅ GOOD: Inheriting from Mapping
class CaseInsensitiveDict(Mapping):
    def __init__(self, data):
        self._data = {k.lower(): v for k, v in data.items()}
    
    def __getitem__(self, key):
        return self._data[key.lower()]
    
    def __iter__(self):
        return iter(self._data)
    
    def __len__(self):
        return len(self._data)

d = CaseInsensitiveDict({"Name": "Alice", "Age": 25})
print(d["name"])   # "Alice" (case insensitive)
print(d["NAME"])   # "Alice"
print(len(d))      # 2
```

### Benefits
- **Protocol compliance**: Works with built-in functions
- **Type checking**: Recognized by type checkers
- **Less code**: Inherit common methods
- **Standard**: Follows Python conventions

---

## Summary

These ten principles help you design effective classes and interfaces:

1. **Functions over classes** - Use functions for simple interfaces
2. **Polymorphism over isinstance** - Let objects handle their behavior
3. **singledispatch** - Consider for functional-style polymorphism
4. **dataclasses** - Use for lightweight data classes
5. **@classmethod** - Use for polymorphic construction
6. **super()** - Always use for parent class calls
7. **Mix-ins** - Compose functionality without deep inheritance
8. **Public attributes** - Prefer over private (Pythonic)
9. **frozen dataclasses** - Use for immutable objects
10. **collections.abc** - Inherit for custom containers

Remember: **Keep it simple, use Python's features effectively, and follow Python conventions.**
