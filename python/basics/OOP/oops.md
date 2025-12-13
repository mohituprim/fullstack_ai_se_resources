What is Object Oriented programming ?
Object Oriented Programming (OOP) is a programming paradigm based on the concept of "objects". Objects are data structures that contain data, in the form of fields (often called **attributes** or **properties**), and code, in the form of procedures (often known as **methods**).

OOP allows you to structure your code in a way that models real-world entities and their interactions. The main principles of OOP are:

- **Encapsulation**: Bundling data and methods that operate on that data within one unit (the class).
- **Abstraction**: Hiding complex reality while exposing only the necessary parts.
- **Inheritance**: Mechanism by which one class can inherit attributes and methods from another class.
- **Polymorphism**: Ability to use functions or methods in different ways depending on the context.

### Example in Python

```python
class Vehicle:
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def honk(self):
        print("Beep beep!")

class Car(Vehicle):
    def honk(self):
        print("Car horn: Honk honk!")

my_car = Car("Toyota", "Corolla")
my_car.honk()  # Output: Car horn: Honk honk!
```

In this example, `Vehicle` is a parent class, and `Car` is a derived class inheriting properties and behavior from `Vehicle`, but also overriding the `honk` method (demonstrating polymorphism).

OOP makes it easier to organize, reuse, and maintain your code—especially for large or complex projects.
Benifits 
- Scalability
- Efficiency
- Reusability


### Constructor in Python

A **constructor** in Python is a special method used for initializing (constructing) objects from a class. In Python, the constructor method is always named `__init__`. It is called automatically when you create a new object of a class.

**Type:**  
The constructor is a special **instance method** with the name `__init__`.

#### Example:

```python
class Person:
    def __init__(self, name, age):  # This is the constructor
        self.name = name
        self.age = age

# Creating an object will call the constructor
person1 = Person("Alice", 30)
print(person1.name)  # Output: Alice
print(person1.age)   # Output: 30
```

Here, `__init__` is the constructor that sets up a new `Person` object with the provided `name` and `age`.

#### Types of Constructors in Python

In Python, there are mainly three types of constructors:

1. **Default Constructor**  
   - A constructor that does not take any arguments except `self`.  
   - It is used when no custom initialization is needed for the object.

   ```python
   class Dog:
       def __init__(self):
           print("Default constructor called")

   dog1 = Dog()  # Output: Default constructor called
   ```

2. **Parameterized Constructor**  
   - A constructor that can accept arguments, allowing you to set instance variables at creation time.

   ```python
   class Animal:
       def __init__(self, name, species):
           self.name = name
           self.species = species

   animal1 = Animal("Charlie", "Cat")
   print(animal1.name)     # Output: Charlie
   print(animal1.species)  # Output: Cat
   ```

3. **Copy Constructor**  
   - Although Python does not have a built-in copy constructor as in some other languages, you can create one by passing an existing object to the constructor to make a copy.

   ```python
   class Point:
       def __init__(self, x=0, y=0):
           self.x = x
           self.y = y

       # Copy constructor
       @classmethod
       def from_point(cls, point_obj):
           return cls(point_obj.x, point_obj.y)

   p1 = Point(2, 3)
   p2 = Point.from_point(p1)
   print(p2.x, p2.y)  # Output: 2 3
   ```

**Summary Table:**

| Constructor Type      | Syntax Example                                  | Purpose                       |
|---------------------- |------------------------------------------------|-------------------------------|
| Default Constructor   | `def __init__(self):`                          | No custom initialization      |
| Parameterized         | `def __init__(self, arg1, arg2):`              | Set instance variables        |
| Copy Constructor      | `@classmethod ... def from_obj(cls, obj):`      | Make a copy of another object |

> **Note:**  
> The `__init__` method is always the initializer/constrctor, Python does not support method overloading by argument types or counts. Use default values or `*args`/`**kwargs` to achieve flexibility.
