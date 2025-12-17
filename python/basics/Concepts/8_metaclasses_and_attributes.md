# Metaclasses and Attributes: Effective Python Best Practices

## 1. Use Plain Attributes Instead of Setter and Getter Methods

### Explanation
Python's philosophy favors direct attribute access over getter/setter methods. Use plain attributes unless you need validation or computed values, then use `@property`.

### Use Cases
- Simple data access
- Avoiding unnecessary complexity
- Following Python conventions
- When properties aren't needed

### Examples

```python
# ❌ BAD: Unnecessary getters/setters (Java style)
class User:
    def __init__(self, name):
        self._name = name
    
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name

user = User("Alice")
name = user.get_name()  # Verbose
user.set_name("Bob")    # Verbose

# ✅ GOOD: Plain attributes (Pythonic)
class User:
    def __init__(self, name):
        self.name = name  # Direct access

user = User("Alice")
name = user.name         # Simple
user.name = "Bob"        # Simple

# When you need validation - use @property
# ✅ GOOD: Property when needed
class User:
    def __init__(self, name):
        self._name = name
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

user = User("Alice")
user.name = "Bob"  # Still looks like attribute access
# user.name = ""   # Raises ValueError
```

### Python Philosophy
- **Direct access**: Prefer `obj.attr` over `obj.get_attr()`
- **Properties when needed**: Use `@property` for validation/computation
- **Trust users**: "We're all consenting adults"

---

## 2. Consider @property Instead of Refactoring Attributes

### Explanation
If you need to add validation or computation to existing attributes, use `@property` instead of changing all call sites. It maintains the attribute access interface.

### Use Cases
- Adding validation to existing code
- Converting attributes to computed values
- Maintaining backward compatibility
- Gradual refactoring

### Examples

```python
# Existing code with plain attribute
class User:
    def __init__(self, name):
        self.name = name  # Used everywhere in codebase

# Need to add validation
# ❌ BAD: Change to getter/setter (breaks all call sites)
class User:
    def __init__(self, name):
        self.set_name(name)  # Breaks existing code!
    
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        if not name:
            raise ValueError("Name required")
        self._name = name

# ✅ GOOD: Use @property (maintains interface)
class User:
    def __init__(self, name):
        self.name = name  # Still works!
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name required")
        self._name = value

# Converting to computed value
# ✅ GOOD: Attribute -> computed property
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # self.area = width * height  # Stale if width/height change

# Add as property
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    @property
    def area(self):
        return self.width * self.height  # Always current

rect = Rectangle(10, 5)
print(rect.area)  # 50
rect.width = 20
print(rect.area)  # 100 (automatically updated)
```

### Benefits
- **Backward compatible**: Existing code still works
- **Gradual migration**: Can add properties incrementally
- **Clean interface**: Still looks like attribute access

---

## 3. Use Descriptors for Reusable @property Methods

### Explanation
When you need the same property logic in multiple classes, use descriptors instead of duplicating `@property` code. Descriptors are reusable property implementations.

### Use Cases
- Reusable validation logic
- Shared property behavior
- DRY principle
- Complex property logic

### Examples

```python
# ❌ BAD: Duplicated @property code
class User:
    def __init__(self, email):
        self._email = email
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if '@' not in value:
            raise ValueError("Invalid email")
        self._email = value

class Admin:
    def __init__(self, email):
        self._email = email
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if '@' not in value:  # Duplicated logic!
            raise ValueError("Invalid email")
        self._email = value

# ✅ GOOD: Reusable descriptor
class EmailDescriptor:
    def __init__(self):
        self._name = None
    
    def __set_name__(self, owner, name):
        self._name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f'_{self._name}')
    
    def __set__(self, obj, value):
        if '@' not in value:
            raise ValueError("Invalid email")
        setattr(obj, f'_{self._name}', value)

class User:
    email = EmailDescriptor()  # Reusable!
    
    def __init__(self, email):
        self.email = email

class Admin:
    email = EmailDescriptor()  # Same descriptor
    
    def __init__(self, email):
        self.email = email

# Validated descriptor
# ✅ GOOD: Generic validation descriptor
class Validated:
    def __init__(self, validator):
        self.validator = validator
        self._name = None
    
    def __set_name__(self, owner, name):
        self._name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f'_{self._name}')
    
    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"Invalid value: {value}")
        setattr(obj, f'_{self._name}', value)

def is_positive(value):
    return isinstance(value, (int, float)) and value > 0

class Product:
    price = Validated(is_positive)
    quantity = Validated(is_positive)
    
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity
```

### Benefits
- **Reusable**: Write once, use many times
- **DRY**: Don't repeat yourself
- **Maintainable**: Change logic in one place
- **Flexible**: Can parameterize behavior

---

## 4. Use __getattr__, __getattribute__, and __setattr__ for Lazy Attributes

### Explanation
These special methods allow you to intercept attribute access and create attributes on-demand. Useful for lazy loading and dynamic attributes.

### Use Cases
- Lazy loading expensive attributes
- Dynamic attribute creation
- Proxy objects
- Attribute access interception

### Examples

```python
# Lazy loading with __getattr__
# ✅ GOOD: Load on first access
class LazyUser:
    def __init__(self, user_id):
        self.user_id = user_id
        self._profile = None
    
    def __getattr__(self, name):
        if name == 'profile':
            if self._profile is None:
                print(f"Loading profile for user {self.user_id}")
                self._profile = self._load_profile()
            return self._profile
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")
    
    def _load_profile(self):
        # Expensive operation
        return {'name': 'Alice', 'age': 25}

user = LazyUser(123)
# Profile not loaded yet
profile = user.profile  # Loads now
print(profile)  # {'name': 'Alice', 'age': 25}

# __getattribute__ vs __getattr__
# ✅ GOOD: Understanding the difference
class AttrDemo:
    def __init__(self):
        self.existing = "I exist"
    
    def __getattribute__(self, name):
        print(f"__getattribute__ called for '{name}'")
        return super().__getattribute__(name)  # Must call super!
    
    def __getattr__(self, name):
        print(f"__getattr__ called for '{name}'")
        return f"Default value for {name}"

obj = AttrDemo()
print(obj.existing)  # __getattribute__ called, returns "I exist"
print(obj.missing)   # __getattribute__ called, then __getattr__ called

# Dynamic attributes
# ✅ GOOD: Creating attributes dynamically
class DynamicObject:
    def __getattr__(self, name):
        # Create attribute on first access
        value = f"Generated: {name}"
        setattr(self, name, value)  # Cache it
        return value

obj = DynamicObject()
print(obj.anything)  # "Generated: anything"
print(obj.anything)  # Cached, no __getattr__ call

# __setattr__ for validation
# ✅ GOOD: Intercepting attribute setting
class ValidatedObject:
    def __init__(self):
        self._data = {}
    
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        elif not isinstance(value, str):
            raise TypeError(f"{name} must be a string")
        else:
            self._data[name] = value
    
    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{name}' not found")

obj = ValidatedObject()
obj.name = "Alice"  # OK
# obj.age = 25      # TypeError
```

### Key Differences
- **__getattr__**: Called only when attribute not found
- **__getattribute__**: Called for ALL attribute access (must call super)
- **__setattr__**: Called for ALL attribute assignment

---

## 5. Validate Subclasses with __init_subclass__

### Explanation
`__init_subclass__` (Python 3.6+) is called when a class is subclassed. Use it to validate subclass definitions and enforce requirements.

### Use Cases
- Validating subclass definitions
- Enforcing interface requirements
- Registering subclasses
- Class-level validation

### Examples

```python
# ✅ GOOD: Validating required methods
class BaseAPI:
    required_methods = ['connect', 'disconnect']
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for method in cls.required_methods:
            if not hasattr(cls, method):
                raise TypeError(f"{cls.__name__} must implement {method}")

class DatabaseAPI(BaseAPI):
    def connect(self):
        pass
    
    def disconnect(self):
        pass
# OK - has required methods

# class BadAPI(BaseAPI):
#     pass
# TypeError: BadAPI must implement connect

# Enforcing attributes
# ✅ GOOD: Requiring class attributes
class Plugin:
    def __init_subclass__(cls, name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if name is None:
            raise TypeError(f"{cls.__name__} must specify 'name'")
        cls.plugin_name = name

class MyPlugin(Plugin, name="my_plugin"):
    pass

print(MyPlugin.plugin_name)  # "my_plugin"

# Registering subclasses
# ✅ GOOD: Auto-registration
class Animal:
    _registry = {}
    
    def __init_subclass__(cls, species=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if species:
            cls._registry[species] = cls

class Dog(Animal, species="dog"):
    pass

class Cat(Animal, species="cat"):
    pass

print(Animal._registry)  # {'dog': <class '__main__.Dog'>, 'cat': <class '__main__.Cat'>}
```

### Benefits
- **Early validation**: Catches errors at class definition time
- **Clear errors**: Immediate feedback on subclass issues
- **Automatic**: No manual registration needed

---

## 6. Register Class Existence with __init_subclass__

### Explanation
Use `__init_subclass__` to automatically register subclasses in a registry, enabling plugin systems and dynamic class discovery.

### Use Cases
- Plugin systems
- Class registries
- Dynamic class discovery
- Factory patterns

### Examples

```python
# ✅ GOOD: Auto-registration
class Processor:
    _processors = {}
    
    def __init_subclass__(cls, processor_type=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if processor_type:
            cls._processors[processor_type] = cls
    
    @classmethod
    def create(cls, processor_type):
        processor_class = cls._processors.get(processor_type)
        if processor_class:
            return processor_class()
        raise ValueError(f"Unknown processor: {processor_type}")

class TextProcessor(Processor, processor_type="text"):
    def process(self, data):
        return f"Text: {data}"

class ImageProcessor(Processor, processor_type="image"):
    def process(self, data):
        return f"Image: {data}"

# Auto-registered!
text_proc = Processor.create("text")
image_proc = Processor.create("image")

# Plugin system
# ✅ GOOD: Plugin registration
class Plugin:
    _plugins = []
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._plugins.append(cls)
    
    @classmethod
    def get_all_plugins(cls):
        return cls._plugins

class PluginA(Plugin):
    pass

class PluginB(Plugin):
    pass

print(Plugin.get_all_plugins())  # [<class '__main__.PluginA'>, <class '__main__.PluginB'>]
```

---

## 7. Annotate Class Attributes with __set_name__

### Explanation
`__set_name__` (Python 3.6+) is called on descriptors when the class they belong to is defined. Use it to know the attribute name without hardcoding.

### Use Cases
- Descriptors that need attribute names
- Automatic attribute name detection
- Better error messages
- Dynamic attribute handling

### Examples

```python
# ✅ GOOD: Using __set_name__
class Validated:
    def __init__(self):
        self._name = None  # Will be set by __set_name__
    
    def __set_name__(self, owner, name):
        self._name = name  # Automatically gets attribute name!
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f'_{self._name}')
    
    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError(f"{self._name} must be a string")
        setattr(obj, f'_{self._name}', value)

class User:
    name = Validated()  # __set_name__ called with 'name'
    email = Validated()  # __set_name__ called with 'email'
    
    def __init__(self, name, email):
        self.name = name
        self.email = email

# Better error messages
user = User("Alice", "alice@example.com")
# user.name = 123  # TypeError: name must be a string (knows it's 'name'!)

# Without __set_name__ (old way)
# ❌ BAD: Hardcoding names
class Validated:
    def __init__(self, name):
        self._name = name  # Must specify manually

class User:
    name = Validated('name')  # Repetitive!
    email = Validated('email')
```

### Benefits
- **Automatic**: No need to specify attribute name
- **DRY**: Don't repeat attribute name
- **Better errors**: Can use actual attribute name in messages

---

## 8. Consider Class Body Definition Order to Establish Relationships Between Attributes

### Explanation
The order attributes are defined in a class matters for descriptors and properties that depend on each other. Define dependencies before dependents.

### Use Cases
- Descriptors with dependencies
- Properties that reference other properties
- Initialization order
- Class-level relationships

### Examples

```python
# ✅ GOOD: Order matters for dependencies
class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    @property
    def diameter(self):
        return self.radius * 2  # Depends on radius
    
    @property
    def area(self):
        return 3.14159 * self.radius ** 2  # Depends on radius
    
    @property
    def circumference(self):
        return 3.14159 * self.diameter  # Depends on diameter (which depends on radius)

# Order: radius -> diameter -> circumference

# Descriptors
# ✅ GOOD: Define base descriptors first
class BaseDescriptor:
    def __set_name__(self, owner, name):
        self._name = name

class DependentDescriptor(BaseDescriptor):
    def __init__(self, depends_on):
        self.depends_on = depends_on
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        base_value = getattr(obj, self.depends_on)
        return base_value * 2

class MyClass:
    base = BaseDescriptor()  # Define first
    derived = DependentDescriptor('base')  # Depends on 'base'
```

### Best Practice
- Define base/independent attributes first
- Define dependent attributes after
- Consider initialization order in `__init__`

---

## 9. Prefer Class Decorators over Metaclasses for Composable Class Extensions

### Explanation
Class decorators are simpler and more composable than metaclasses. Use them for adding functionality to classes unless you need the full power of metaclasses.

### Use Cases
- Adding functionality to classes
- Composable class extensions
- Simpler than metaclasses
- Multiple independent extensions

### Examples

```python
# ✅ GOOD: Class decorator (simple)
def add_timing(cls):
    """Add timing to all methods."""
    for name, method in vars(cls).items():
        if callable(method) and not name.startswith('_'):
            setattr(cls, name, timing_decorator(method))
    return cls

@add_timing
class Calculator:
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b

# ✅ GOOD: Composable decorators
def add_logging(cls):
    # Add logging
    return cls

def add_validation(cls):
    # Add validation
    return cls

@add_logging
@add_validation
@add_timing
class MyClass:
    pass
# All decorators applied!

# ❌ BAD: Metaclass (more complex)
class TimingMeta(type):
    def __new__(cls, name, bases, dct):
        # Complex metaclass logic
        return super().__new__(cls, name, bases, dct)

class Calculator(metaclass=TimingMeta):
    pass
# Harder to compose multiple metaclasses

# When to use metaclasses
# ✅ Use metaclasses when:
# - Need to modify class creation process
# - Need to control MRO
# - Need to modify class dictionary before creation
# - Complex class transformation

# ✅ Use decorators when:
# - Simple class modification
# - Adding functionality
# - Want composability
# - Simpler is better
```

### Benefits
- **Simpler**: Easier to understand and write
- **Composable**: Can stack multiple decorators
- **Readable**: Clear what each decorator does
- **Flexible**: Easy to add/remove functionality

---

## Summary

These nine principles help you work effectively with attributes and class customization:

1. **Plain attributes** - Prefer over getters/setters
2. **@property** - Use instead of refactoring when adding validation
3. **Descriptors** - Use for reusable property logic
4. **__getattr__/__setattr__** - Use for lazy attributes
5. **__init_subclass__** - Validate subclasses
6. **__init_subclass__** - Register subclasses automatically
7. **__set_name__** - Annotate descriptors with attribute names
8. **Definition order** - Consider for attribute dependencies
9. **Class decorators** - Prefer over metaclasses for composability

Remember: **Keep it simple. Use advanced features only when needed, and prefer simpler solutions.**
