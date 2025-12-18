## Chain of Responsibility Design Pattern

**Intent**: Pass a request along a chain of handlers; each handler decides whether to process the request or pass it to the next handler.

- **When to use**:  
  - You want to decouple senders from receivers.  
  - Multiple handlers may or may not handle a request.  
  - You want flexible ordering and composition of processing steps.

**Class example (Python)**:

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


class Handler(ABC):
    def __init__(self) -> None:
        self._next: Optional[Handler] = None

    def set_next(self, handler: Handler) -> Handler:
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, request: str) -> None:
        if self._next:
            self._next.handle(request)


class AuthHandler(Handler):
    def handle(self, request: str) -> None:
        if "auth" in request:
            print("AuthHandler: authenticated request")
            if self._next:
                self._next.handle(request)
        else:
            print("AuthHandler: rejected request (no auth)")


class LoggingHandler(Handler):
    def handle(self, request: str) -> None:
        print(f"LoggingHandler: logging request = {request}")
        if self._next:
            self._next.handle(request)


class BusinessHandler(Handler):
    def handle(self, request: str) -> None:
        print(f"BusinessHandler: processing business logic for {request}")
```

**Usage example**:

```python
if __name__ == "__main__":
    auth = AuthHandler()
    logger = LoggingHandler()
    business = BusinessHandler()

    auth.set_next(logger).set_next(business)

    print("=== Valid request ===")
    auth.handle("auth: get /orders")

    print("=== Invalid request ===")
    auth.handle("get /orders")
```

---

## Command Design Pattern

**Intent**: Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undo/redo.

- **When to use**:  
  - You want to decouple invokers from receivers.  
  - You need undo/redo, queues, or macro commands.

**Class example (Python)**:

```python
from abc import ABC, abstractmethod
from typing import List


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


class Light:
    def __init__(self) -> None:
        self.is_on = False

    def on(self) -> None:
        self.is_on = True
        print("Light is ON")

    def off(self) -> None:
        self.is_on = False
        print("Light is OFF")


class LightOnCommand(Command):
    def __init__(self, light: Light) -> None:
        self.light = light

    def execute(self) -> None:
        self.light.on()

    def undo(self) -> None:
        self.light.off()


class LightOffCommand(Command):
    def __init__(self, light: Light) -> None:
        self.light = light

    def execute(self) -> None:
        self.light.off()

    def undo(self) -> None:
        self.light.on()


class RemoteControl:
    def __init__(self) -> None:
        self._history: List[Command] = []

    def submit(self, command: Command) -> None:
        command.execute()
        self._history.append(command)

    def undo_last(self) -> None:
        if self._history:
            cmd = self._history.pop()
            cmd.undo()
```

**Usage example**:

```python
if __name__ == "__main__":
    light = Light()
    remote = RemoteControl()

    remote.submit(LightOnCommand(light))
    remote.submit(LightOffCommand(light))
    remote.undo_last()  # turns light back ON
```

---

## Interpreter Design Pattern

**Intent**: Define a representation for a grammar and an interpreter to evaluate sentences in that language.

- **When to use**:  
  - You have a simple language or DSL embedded in your system.  
  - The grammar is simple and unlikely to change frequently.

**Class example (Python)** (simple boolean expression interpreter):

```python
from abc import ABC, abstractmethod
from typing import Dict


class Expression(ABC):
    @abstractmethod
    def interpret(self, context: Dict[str, bool]) -> bool:
        pass


class Variable(Expression):
    def __init__(self, name: str) -> None:
        self.name = name

    def interpret(self, context: Dict[str, bool]) -> bool:
        return context[self.name]


class And(Expression):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def interpret(self, context: Dict[str, bool]) -> bool:
        return self.left.interpret(context) and self.right.interpret(context)


class Or(Expression):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def interpret(self, context: Dict[str, bool]) -> bool:
        return self.left.interpret(context) or self.right.interpret(context)
```

**Usage example**:

```python
if __name__ == "__main__":
    # Expression: (A AND B) OR A
    a = Variable("A")
    b = Variable("B")
    expr = Or(And(a, b), a)

    context = {"A": True, "B": False}
    print(expr.interpret(context))  # True
```

---

## Mediator Design Pattern

**Intent**: Define an object that **encapsulates how a set of objects interact**, promoting loose coupling by preventing objects from referring to each other explicitly.

- **When to use**:  
  - Many objects communicate in complex ways.  
  - You want to centralize and simplify communication logic.

**Class example (Python)**:

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class ChatMediator(ABC):
    @abstractmethod
    def send_message(self, message: str, sender: "User") -> None:
        pass


class ChatRoom(ChatMediator):
    def __init__(self) -> None:
        self._users: List[User] = []

    def register(self, user: "User") -> None:
        self._users.append(user)

    def send_message(self, message: str, sender: "User") -> None:
        for user in self._users:
            if user is not sender:
                user.receive(message, sender)


class User:
    def __init__(self, name: str, mediator: ChatMediator) -> None:
        self.name = name
        self.mediator = mediator
        mediator.register(self)

    def send(self, message: str) -> None:
        print(f"{self.name} sends: {message}")
        self.mediator.send_message(message, self)

    def receive(self, message: str, sender: "User") -> None:
        print(f"{self.name} receives from {sender.name}: {message}")
```

**Usage example**:

```python
if __name__ == "__main__":
    room = ChatRoom()
    alice = User("Alice", room)
    bob = User("Bob", room)

    alice.send("Hello Bob!")
    bob.send("Hi Alice!")
```

---

## Memento Design Pattern

**Intent**: Capture and externalize an object’s internal state so it can be restored later, without violating encapsulation.

- **When to use**:  
  - You need undo/rollback functionality.  
  - You want to save/restore state snapshots.

**Class example (Python)**:

```python
from typing import List


class EditorMemento:
    def __init__(self, text: str) -> None:
        self._text = text

    @property
    def text(self) -> str:
        return self._text


class TextEditor:
    def __init__(self) -> None:
        self._text = ""

    def type(self, words: str) -> None:
        self._text += words

    def get_text(self) -> str:
        return self._text

    def save(self) -> EditorMemento:
        return EditorMemento(self._text)

    def restore(self, memento: EditorMemento) -> None:
        self._text = memento.text


class History:
    def __init__(self) -> None:
        self._states: List[EditorMemento] = []

    def push(self, memento: EditorMemento) -> None:
        self._states.append(memento)

    def pop(self) -> EditorMemento:
        return self._states.pop()
```

**Usage example**:

```python
if __name__ == "__main__":
    editor = TextEditor()
    history = History()

    editor.type("Hello")
    history.push(editor.save())

    editor.type(" World")
    history.push(editor.save())

    print(editor.get_text())  # Hello World

    editor.restore(history.pop())
    print(editor.get_text())  # Hello World

    editor.restore(history.pop())
    print(editor.get_text())  # Hello
```

---

## Observer Design Pattern

**Intent**: Define a one-to-many dependency so that when one object (subject) changes state, all its dependents (observers) are notified and updated automatically.

- **When to use**:  
  - Event-driven systems, GUIs, reactive systems.  
  - You want to decouple emitters from listeners.

**Class example (Python)**:

```python
from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    @abstractmethod
    def update(self, temperature: float) -> None:
        pass


class WeatherStation:
    def __init__(self) -> None:
        self._observers: List[Observer] = []
        self._temperature = 0.0

    def add_observer(self, observer: Observer) -> None:
        self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def set_temperature(self, temperature: float) -> None:
        self._temperature = temperature
        self._notify()

    def _notify(self) -> None:
        for obs in self._observers:
            obs.update(self._temperature)


class PhoneDisplay(Observer):
    def update(self, temperature: float) -> None:
        print(f"PhoneDisplay: temperature is now {temperature}°C")


class LEDDisplay(Observer):
    def update(self, temperature: float) -> None:
        print(f"LEDDisplay: temperature is now {temperature}°C")
```

**Usage example**:

```python
if __name__ == "__main__":
    station = WeatherStation()
    phone = PhoneDisplay()
    led = LEDDisplay()

    station.add_observer(phone)
    station.add_observer(led)

    station.set_temperature(25.0)
    station.set_temperature(30.5)
```

---

## State Design Pattern

**Intent**: Allow an object to change its behavior when its internal state changes, as if the object changed its class.

- **When to use**:  
  - An object’s behavior depends on its state and must change at runtime.  
  - You want to avoid large `if/elif` state machines.

**Class example (Python)**:

```python
from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def handle(self, context: "Context") -> None:
        pass


class Context:
    def __init__(self, state: State) -> None:
        self._state = state

    def set_state(self, state: State) -> None:
        print(f"Context: transition to {state.__class__.__name__}")
        self._state = state

    def request(self) -> None:
        self._state.handle(self)


class ConcreteStateA(State):
    def handle(self, context: Context) -> None:
        print("State A handling request; switching to State B")
        context.set_state(ConcreteStateB())


class ConcreteStateB(State):
    def handle(self, context: Context) -> None:
        print("State B handling request; switching to State A")
        context.set_state(ConcreteStateA())
```

**Usage example**:

```python
if __name__ == "__main__":
    context = Context(ConcreteStateA())
    context.request()
    context.request()
    context.request()
```

---

## Strategy Design Pattern

**Intent**: Define a family of algorithms, encapsulate each one, and make them interchangeable.

- **When to use**:  
  - You want to switch algorithms at runtime.  
  - You want to avoid hardcoding complex conditional logic to choose behavior.

**Class example (Python)**:

```python
from abc import ABC, abstractmethod
from typing import List


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass


class AscendingSort(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        return sorted(data)


class DescendingSort(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        return sorted(data, reverse=True)


class SortContext:
    def __init__(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def execute(self, data: List[int]) -> List[int]:
        return self._strategy.sort(data)
```

**Usage example**:

```python
if __name__ == "__main__":
    data = [5, 2, 9, 1]
    context = SortContext(AscendingSort())
    print(context.execute(data))  # [1, 2, 5, 9]

    context.set_strategy(DescendingSort())
    print(context.execute(data))  # [9, 5, 2, 1]
```

---

## Template Method Design Pattern

**Intent**: Define the **skeleton of an algorithm** in a method, deferring some steps to subclasses without changing the overall structure.

- **When to use**:  
  - Multiple implementations share the same algorithm structure.  
  - You want to enforce the order of steps, but let subclasses customize details.

**Class example (Python)**:

```python
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    def process(self) -> None:
        self.load_data()
        self.transform_data()
        self.save_data()

    @abstractmethod
    def load_data(self) -> None:
        pass

    @abstractmethod
    def transform_data(self) -> None:
        pass

    @abstractmethod
    def save_data(self) -> None:
        pass


class CSVDataProcessor(DataProcessor):
    def load_data(self) -> None:
        print("Loading data from CSV file")

    def transform_data(self) -> None:
        print("Cleaning and transforming CSV data")

    def save_data(self) -> None:
        print("Saving processed data to database")
```

**Usage example**:

```python
if __name__ == "__main__":
    processor = CSVDataProcessor()
    processor.process()
```

---

## Visitor Design Pattern

**Intent**: Represent an operation to be performed on elements of an object structure, allowing you to define new operations **without changing the element classes**.

- **When to use**:  
  - You have a stable object structure but need to add new operations often.  
  - You want to separate algorithms from the objects on which they operate.

**Class example (Python)**:

```python
from abc import ABC, abstractmethod
from typing import List


class Visitor(ABC):
    @abstractmethod
    def visit_file(self, element: "FileElement") -> None:
        pass

    @abstractmethod
    def visit_folder(self, element: "FolderElement") -> None:
        pass


class Element(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass


class FileElement(Element):
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_file(self)


class FolderElement(Element):
    def __init__(self, name: str) -> None:
        self.name = name
        self.children: List[Element] = []

    def add(self, element: Element) -> None:
        self.children.append(element)

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_folder(self)
        for child in self.children:
            child.accept(visitor)


class SizeCalculatorVisitor(Visitor):
    def __init__(self) -> None:
        self.total_size = 0

    def visit_file(self, element: FileElement) -> None:
        self.total_size += element.size

    def visit_folder(self, element: FolderElement) -> None:
        # Optional: handle folder-specific logic
        pass
```

**Usage example**:

```python
if __name__ == "__main__":
    root = FolderElement("root")
    root.add(FileElement("a.txt", 100))
    root.add(FileElement("b.txt", 200))

    sub = FolderElement("sub")
    sub.add(FileElement("c.txt", 300))
    root.add(sub)

    visitor = SizeCalculatorVisitor()
    root.accept(visitor)
    print(visitor.total_size)  # 600
```

---

**Summary**

- **Chain of Responsibility**: Pass requests along a chain of handlers.  
- **Command**: Encapsulate requests as objects (undo, queues, macros).  
- **Interpreter**: Evaluate sentences in a simple language/grammar.  
- **Mediator**: Centralize communication between objects.  
- **Memento**: Save and restore object state without breaking encapsulation.  
- **Observer**: Notify many dependents automatically when a subject changes.  
- **State**: Change behavior when internal state changes.  
- **Strategy**: Swap algorithms at runtime via a common interface.  
- **Template Method**: Define algorithm skeleton; subclasses fill in steps.  
- **Visitor**: Add new operations to object structures without modifying them.
