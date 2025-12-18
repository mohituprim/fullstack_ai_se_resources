## Factory Method Design Pattern

**Intent**: Define an interface for creating an object, but let subclasses decide which concrete class to instantiate.

- **When to use**:  
  - **You want** to encapsulate object creation logic.  
  - **You want** different products created depending on configuration or subclass.  
  - **You want** to avoid `if/elif` trees scattered around the code for object creation.

**Class example (Python)**:

```python
from abc import ABC, abstractmethod


class Transport(ABC):
    @abstractmethod
    def deliver(self) -> None:
        pass


class Truck(Transport):
    def deliver(self) -> None:
        print("Delivering by road in a truck")


class Ship(Transport):
    def deliver(self) -> None:
        print("Delivering by sea in a ship")


class Logistics(ABC):
    @abstractmethod
    def create_transport(self) -> Transport:
        """Factory Method."""
        pass

    def plan_delivery(self) -> None:
        # business logic that uses the product created by the factory method
        transport = self.create_transport()
        transport.deliver()


class RoadLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Truck()


class SeaLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Ship()
```

**Usage example**:

```python
def client_code(logistics: Logistics) -> None:
    logistics.plan_delivery()


if __name__ == "__main__":
    # Choose the concrete creator at runtime
    client_code(RoadLogistics())  # Delivering by road in a truck
    client_code(SeaLogistics())   # Delivering by sea in a ship
```

---

## Abstract Factory Method Design Pattern

**Intent**: Provide an interface for creating **families of related or dependent objects** without specifying their concrete classes.

- **When to use**:  
  - **You want** to support multiple product families (e.g., Windows UI vs. Mac UI).  
  - **You want** to ensure products from the same family are used together.  
  - **You want** to keep creation of these families centralized.

**Class example (Python)**:

```python
from abc import ABC, abstractmethod


class Button(ABC):
    @abstractmethod
    def render(self) -> None:
        pass


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> None:
        pass


class WinButton(Button):
    def render(self) -> None:
        print("Rendering Windows style button")


class WinCheckbox(Checkbox):
    def render(self) -> None:
        print("Rendering Windows style checkbox")


class MacButton(Button):
    def render(self) -> None:
        print("Rendering macOS style button")


class MacCheckbox(Checkbox):
    def render(self) -> None:
        print("Rendering macOS style checkbox")


class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass


class WinFactory(GUIFactory):
    def create_button(self) -> Button:
        return WinButton()

    def create_checkbox(self) -> Checkbox:
        return WinCheckbox()


class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()
```

**Usage example**:

```python
def render_ui(factory: GUIFactory) -> None:
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    button.render()
    checkbox.render()


if __name__ == "__main__":
    os_type = "windows"  # could come from config/env

    if os_type == "windows":
        factory = WinFactory()
    else:
        factory = MacFactory()

    render_ui(factory)
```

---

## Singleton Method Design Pattern

**Intent**: Ensure a class has **only one instance**, and provide a global access point to it.

- **When to use**:  
  - **You need** exactly one shared object (e.g., configuration, logger, connection pool).  
  - **You want** controlled global access.

**Class example (Python, simple eager singleton)**:

```python
class AppConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # one-time initialization
            cls._instance.debug = False
        return cls._instance


config1 = AppConfig()
config2 = AppConfig()

assert config1 is config2  # same instance
```

**Usage example**:

```python
def enable_debug() -> None:
    config = AppConfig()
    config.debug = True


def is_debug_enabled() -> bool:
    config = AppConfig()
    return config.debug


if __name__ == "__main__":
    enable_debug()
    print(is_debug_enabled())  # True, same shared instance
```

> Note: In multi-threaded or large systems, prefer dependency injection and explicit scopes over heavy use of singletons.

---

## Prototype Method Design Pattern

**Intent**: Create new objects by **cloning existing objects (prototypes)** instead of instantiating classes directly.

- **When to use**:  
  - **Object creation** is costly or complex.  
  - **You need** copies of objects with mostly similar state.  
  - **You want** to avoid subclass explosion when using configuration-heavy objects.

**Class example (Python)**:

```python
import copy


class Enemy:
    def __init__(self, health: int, speed: int, weapon: str) -> None:
        self.health = health
        self.speed = speed
        self.weapon = weapon

    def clone(self) -> "Enemy":
        # Shallow copy is often enough; use deepcopy for nested structures
        return copy.copy(self)

    def __repr__(self) -> str:
        return f"Enemy(health={self.health}, speed={self.speed}, weapon={self.weapon!r})"
```

**Usage example**:

```python
if __name__ == "__main__":
    base_orc = Enemy(health=100, speed=10, weapon="axe")

    # Create many similar enemies by cloning and tweaking
    fast_orc = base_orc.clone()
    fast_orc.speed = 20

    strong_orc = base_orc.clone()
    strong_orc.health = 150

    print(base_orc)   # Enemy(health=100, speed=10, weapon='axe')
    print(fast_orc)   # Enemy(health=100, speed=20, weapon='axe')
    print(strong_orc) # Enemy(health=150, speed=10, weapon='axe')
```

---

## Builder Method Design Pattern

**Intent**: Separate the **construction of a complex object** from its representation, so the same construction process can create different representations.

- **When to use**:  
  - **Objects** have many optional parameters or complicated assembly steps.  
  - **You want** readable, step-by-step object construction.  
  - **You want** different representations built via the same steps.

**Class example (Python)**:

```python
class House:
    def __init__(self) -> None:
        self.has_garden = False
        self.has_garage = False
        self.floors = 1

    def __repr__(self) -> str:
        return (
            f"House(floors={self.floors}, "
            f"garden={self.has_garden}, garage={self.has_garage})"
        )


class HouseBuilder:
    def __init__(self) -> None:
        self._house = House()

    def add_garden(self) -> "HouseBuilder":
        self._house.has_garden = True
        return self

    def add_garage(self) -> "HouseBuilder":
        self._house.has_garage = True
        return self

    def set_floors(self, floors: int) -> "HouseBuilder":
        self._house.floors = floors
        return self

    def build(self) -> House:
        return self._house
```

**Usage example**:

```python
if __name__ == "__main__":
    # Build a 2-floor luxury house with garden and garage
    luxury_house = (
        HouseBuilder()
        .set_floors(2)
        .add_garden()
        .add_garage()
        .build()
    )

    # Build a simple one-floor house
    simple_house = HouseBuilder().build()

    print(luxury_house)  # House(floors=2, garden=True, garage=True)
    print(simple_house)  # House(floors=1, garden=False, garage=False)
```

---

**Summary**

- **Factory Method**: Defer object creation to subclasses.  
- **Abstract Factory**: Create families of related objects.  
- **Singleton**: Single shared instance with global access.  
- **Prototype**: Clone existing objects instead of creating from scratch.  
- **Builder**: Step-by-step construction of complex objects.
