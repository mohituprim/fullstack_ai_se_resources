## Adapter Design Pattern

**Intent**: Allow objects with incompatible interfaces to work together by **wrapping** one object with an adapter that exposes the expected interface.

- **When to use**:  
  - You want to integrate a third-party or legacy class whose interface doesn’t match your system.  
  - You want to reuse existing code without modifying it.

**Class example (Python)**:

```python
class EuropeanSocket:
    def supply_220v(self) -> None:
        print("Supplying 220V")


class USDevice:
    def plug_110v(self) -> None:
        print("Running on 110V")


class EuropeanToUSAdapter:
    """
    Adapter that makes a European socket compatible with a US device.
    """

    def __init__(self, socket: EuropeanSocket) -> None:
        self._socket = socket

    def plug_110v(self) -> None:
        # Internally uses 220V but presents a 110V method
        self._socket.supply_220v()
        print("Converting 220V to 110V for the US device")
```

**Usage example**:

```python
if __name__ == "__main__":
    european_socket = EuropeanSocket()
    adapter = EuropeanToUSAdapter(european_socket)

    us_device = USDevice()

    # Instead of plugging directly into a US socket,
    # we plug the device into the adapter.
    adapter.plug_110v()  # internally uses 220V, exposes plug_110v
    us_device.plug_110v()
```

---

## Bridge Design Pattern

**Intent**: Decouple an abstraction from its implementation so that the two can vary independently.

- **When to use**:  
  - You have a class explosion due to many combinations of **abstractions × implementations**.  
  - You want to switch implementations at runtime without changing the abstraction.

**Class example (Python)**:

```python
from abc import ABC, abstractmethod


class DrawingAPI(ABC):
    @abstractmethod
    def draw_circle(self, x: float, y: float, radius: float) -> None:
        pass


class DrawingAPI1(DrawingAPI):
    def draw_circle(self, x: float, y: float, radius: float) -> None:
        print(f"API1.circle at ({x}, {y}) with radius {radius}")


class DrawingAPI2(DrawingAPI):
    def draw_circle(self, x: float, y: float, radius: float) -> None:
        print(f"API2.circle at ({x}, {y}) with radius {radius}")


class Shape(ABC):
    def __init__(self, drawing_api: DrawingAPI) -> None:
        self._drawing_api = drawing_api

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def resize_by_percentage(self, pct: float) -> None:
        pass


class CircleShape(Shape):
    def __init__(self, x: float, y: float, radius: float, drawing_api: DrawingAPI):
        super().__init__(drawing_api)
        self._x = x
        self._y = y
        self._radius = radius

    def draw(self) -> None:
        self._drawing_api.draw_circle(self._x, self._y, self._radius)

    def resize_by_percentage(self, pct: float) -> None:
        self._radius *= (1 + pct / 100.0)
```

**Usage example**:

```python
if __name__ == "__main__":
    circle1 = CircleShape(1, 2, 3, DrawingAPI1())
    circle2 = CircleShape(5, 7, 11, DrawingAPI2())

    circle1.resize_by_percentage(10)
    circle2.resize_by_percentage(-20)

    circle1.draw()  # uses DrawingAPI1
    circle2.draw()  # uses DrawingAPI2
```

---

## Composite Design Pattern

**Intent**: Compose objects into tree structures to represent **part–whole hierarchies**, letting clients treat individual objects and compositions **uniformly**.

- **When to use**:  
  - You have hierarchical structures (e.g., file system, UI components).  
  - Clients should work with single objects and groups in the same way.

**Class example (Python)**:

```python
from abc import ABC, abstractmethod
from typing import List


class FileSystemItem(ABC):
    @abstractmethod
    def get_size(self) -> int:
        pass


class File(FileSystemItem):
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self._size = size

    def get_size(self) -> int:
        return self._size


class Directory(FileSystemItem):
    def __init__(self, name: str) -> None:
        self.name = name
        self._children: List[FileSystemItem] = []

    def add(self, item: FileSystemItem) -> None:
        self._children.append(item)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self._children)
```

**Usage example**:

```python
if __name__ == "__main__":
    root = Directory("root")
    src = Directory("src")
    assets = Directory("assets")

    root.add(src)
    root.add(assets)
    src.add(File("main.py", 1200))
    src.add(File("utils.py", 800))
    assets.add(File("logo.png", 5000))

    print(root.get_size())  # 1200 + 800 + 5000 = 7000
```

---

## Decorator Design Pattern

**Intent**: Attach **additional responsibilities** to an object dynamically, without modifying its class. Decorators provide a flexible alternative to subclassing for extending behavior.

- **When to use**:  
  - You want to add cross-cutting concerns (logging, caching, auth) to objects.  
  - You want to combine multiple behaviors flexibly at runtime.

**Class example (Python)**:

```python
from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass


class EmailNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"Sending EMAIL with message: {message}")


class NotifierDecorator(Notifier):
    def __init__(self, wrappee: Notifier) -> None:
        self._wrappee = wrappee

    def send(self, message: str) -> None:
        self._wrappee.send(message)


class SMSNotifier(NotifierDecorator):
    def send(self, message: str) -> None:
        super().send(message)
        print(f"Sending SMS with message: {message}")


class SlackNotifier(NotifierDecorator):
    def send(self, message: str) -> None:
        super().send(message)
        print(f"Posting to SLACK: {message}")
```

**Usage example**:

```python
if __name__ == "__main__":
    # Base notifier: email only
    email_notifier = EmailNotifier()

    # Decorated notifier: email + SMS
    email_sms_notifier = SMSNotifier(email_notifier)

    # Decorated notifier: email + SMS + Slack
    full_notifier = SlackNotifier(email_sms_notifier)

    full_notifier.send("System going down for maintenance")
```

---

## Facade Design Pattern

**Intent**: Provide a **simple, unified interface** to a complex subsystem.

- **When to use**:  
  - Subsystems are complex or have many interdependent classes.  
  - You want to provide a simpler API for common use cases.

**Class example (Python)**:

```python
class CPU:
    def freeze(self) -> None:
        print("Freezing CPU")

    def jump(self, position: int) -> None:
        print(f"Jumping to position {position}")

    def execute(self) -> None:
        print("Executing instructions")


class Memory:
    def load(self, position: int, data: bytes) -> None:
        print(f"Loading data into memory at position {position}")


class HardDrive:
    def read(self, lba: int, size: int) -> bytes:
        print(f"Reading {size} bytes from sector {lba}")
        return b"\x00" * size


class ComputerFacade:
    def __init__(self) -> None:
        self._cpu = CPU()
        self._memory = Memory()
        self._hard_drive = HardDrive()

    def start(self) -> None:
        self._cpu.freeze()
        data = self._hard_drive.read(0, 1024)
        self._memory.load(0, data)
        self._cpu.jump(0)
        self._cpu.execute()
```

**Usage example**:

```python
if __name__ == "__main__":
    computer = ComputerFacade()
    computer.start()  # simple interface hiding the subsystem complexity
```

---

## Flyweight Design Pattern

**Intent**: Minimize memory use by sharing as much data as possible with similar objects; separate **intrinsic (shared)** state from **extrinsic (context-specific)** state.

- **When to use**:  
  - You have a huge number of similar objects (e.g., characters in a text editor, tiles in a game).  
  - Most object state can be shared.

**Class example (Python)**:

```python
from typing import Dict


class TreeType:
    """
    Intrinsic state: shared between many trees (texture, color, etc.).
    """

    def __init__(self, name: str, color: str, texture: str) -> None:
        self.name = name
        self.color = color
        self.texture = texture

    def draw(self, x: int, y: int) -> None:
        print(f"Drawing {self.name} tree at ({x}, {y}) with color {self.color}")


class TreeFactory:
    _tree_types: Dict[str, TreeType] = {}

    @classmethod
    def get_tree_type(cls, name: str, color: str, texture: str) -> TreeType:
        key = (name, color, texture)
        if key not in cls._tree_types:
            cls._tree_types[key] = TreeType(name, color, texture)
        return cls._tree_types[key]


class Tree:
    """
    Extrinsic state: position (x, y) is stored per-object.
    Intrinsic state: TreeType is shared.
    """

    def __init__(self, x: int, y: int, tree_type: TreeType) -> None:
        self.x = x
        self.y = y
        self.type = tree_type

    def draw(self) -> None:
        self.type.draw(self.x, self.y)
```

**Usage example**:

```python
if __name__ == "__main__":
    trees = []
    for i in range(0, 1000, 10):
        tree_type = TreeFactory.get_tree_type("Oak", "Green", "Rough")
        trees.append(Tree(i, i // 2, tree_type))

    print(f"Number of TreeType objects created: {len(TreeFactory._tree_types)}")
    for tree in trees[:3]:
        tree.draw()
```

---

## Proxy Design Pattern

**Intent**: Provide a **surrogate** or placeholder for another object to control access to it.

- **When to use**:  
  - You need lazy initialization, access control, logging, caching, or smart references around a real object.  
  - The real object is remote, heavy, or needs protection.

**Class example (Python)**:

```python
from abc import ABC, abstractmethod


class Image(ABC):
    @abstractmethod
    def display(self) -> None:
        pass


class RealImage(Image):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        print(f"Loading image from disk: {self.filename}")

    def display(self) -> None:
        print(f"Displaying image: {self.filename}")


class ImageProxy(Image):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._real_image: RealImage | None = None

    def display(self) -> None:
        if self._real_image is None:
            # Lazy initialization: load on first use
            self._real_image = RealImage(self.filename)
        self._real_image.display()
```

**Usage example**:

```python
if __name__ == "__main__":
    image = ImageProxy("large_photo.png")

    # Image is loaded only when display() is first called
    image.display()
    image.display()  # second call reuses the already loaded RealImage
```

---

**Summary**

- **Adapter**: Make incompatible interfaces work together.  
- **Bridge**: Separate abstraction from implementation so both can vary independently.  
- **Composite**: Treat individual objects and composites uniformly using tree structures.  
- **Decorator**: Add responsibilities to objects dynamically without changing their class.  
- **Facade**: Provide a simplified interface over a complex subsystem.  
- **Flyweight**: Share intrinsic state to support large numbers of fine-grained objects efficiently.  
- **Proxy**: Control access to another object (lazy loading, access control, logging, etc.).
