from Engine import *
from Vehicle import *

engine = Engine("V6")
vehicle = Vehicle("Car", True, engine)
vehicle.engine.startEngine()
'''
What is composition?
--------------------
Composition is an object-oriented design principle where one class includes (or "has a") reference to another class or object, rather than inheriting its behavior. In composition, objects are made up of other objects, establishing a "part-of" relationship.

Benefits of composition:
------------------------
- Promotes code reuse by assembling complex types from simpler ones.
- Increases flexibility: You can change components at runtime or substitute different objects, leading to more adaptable code.
- Looser coupling: Components (objects) can evolve independently, without the tight inheritance hierarchy.

How is composition different from inheritance?
----------------------------------------------
- Inheritance establishes an "is-a" relationship between classes. (e.g., Dog inherits from Animal: Dog is-an Animal)
- Composition establishes a "has-a" relationship. (e.g., Car has-an Engine)
- Inheritance means the subclass gets behavior from its parent class, while composition means a class can use (compose) behavior from other classes by having their instances as attributes.

Benefits of composition over inheritance:
-----------------------------------------
- Avoids deep and complex class hierarchies.
- More flexibility: You can swap out or modify components (objects) without altering the containing class.
- Favors code reuse through delegation rather than inheritance. This makes the code easier to understand, maintain, and extend.

How is composition used here?
-----------------------------
In this code example:
- The `Vehicle` class uses **composition** by having an `Engine` object as its attribute (`self.engine`).
- Instead of inheriting from `Engine`, `Vehicle` simply *has* an `Engine` (it receives one in its constructor and stores it).
- This setup means we can give any type of `Engine` to our `Vehicle`, making it flexible and decoupled. For example, we can swap the engine type without changing the `Vehicle` or `Engine` class.

This is an example of *composition* in Python OOP!
'''
