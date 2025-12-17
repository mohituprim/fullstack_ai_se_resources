# Testing and Debugging: Effective Python Best Practices

## 1. Verify Related Behaviors in TestCase Subclasses

### Explanation
`unittest.TestCase` lets you group related tests into **classes**. Each method that starts with `test_` is a separate test. Grouping related tests:
- Improves organization and readability
- Lets you share common setup/teardown
- Makes it easy to see all tests for a given feature

### Use Cases
- Testing a single class or module
- Grouping tests by feature or behavior
- Sharing fixtures (`setUp`, `tearDown`) between related tests

### Examples

```python
import unittest

def add(a, b):
    return a + b

class TestAdd(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)
\n    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -2), -3)

    def test_add_mixed_signs(self):
        self.assertEqual(add(-1, 2), 1)

if __name__ == "__main__":
    unittest.main()
```

You can create multiple `TestCase` subclasses for different parts of your code:

```python
class TestUserModel(unittest.TestCase):
    ...

class TestUserAPI(unittest.TestCase):
    ...
```

### Best Practices
- One `TestCase` per concept/feature/class
- Use descriptive test method names (`test_something_happens_when...`)

---

## 2. Prefer Integration Tests over Unit Tests

### Explanation
Unit tests focus on **small pieces** (single functions/classes) in isolation. Integration tests check that **pieces work together** correctly (e.g., API + DB + logic).  
Both are useful, but:
- Integration tests catch real-world failures
- Unit tests can be too tightly coupled to implementation details

### Use Cases
- Testing API endpoints end-to-end
- Testing workflows (e.g., user registration, login)
- Verifying interactions with databases, message queues, etc. (possibly in a test environment)

### Examples

```python
# Unit-level test (isolated)
def calculate_total(items):
    return sum(items)

class TestCalculateTotal(unittest.TestCase):
    def test_calculate_total(self):
        self.assertEqual(calculate_total([1, 2, 3]), 6)
```

Integration-style test with `requests` (example, not full app):

```python
import unittest
import requests

class TestUserRegistrationFlow(unittest.TestCase):
    BASE_URL = "http://localhost:8000"

    def test_register_and_login(self):
        # Register
        resp = requests.post(
            f"{self.BASE_URL}/register",
            json={"username": "alice", "password": "secret"},
        )
        self.assertEqual(resp.status_code, 201)

        # Login
        resp = requests.post(
            f"{self.BASE_URL}/login",
            json={"username": "alice", "password": "secret"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("token", resp.json())
```

### Guidelines
- Have **some unit tests** for core logic
- Emphasize **integration tests** for important user flows and external dependencies
- Avoid writing tests that are so tightly coupled to private implementation that any refactor breaks them

---

## 3. Isolate Tests From Each Other with setUp, tearDown, setUpModule, and tearDownModule

### Explanation
Each test should be **independent** and **repeatable**. `unittest` provides hooks:
- `setUp` / `tearDown`: run before/after **each test method**
- `setUpClass` / `tearDownClass`: run once per **TestCase class**
- `setUpModule` / `tearDownModule`: run once per **module**

Use them to:
- Create fresh state for each test
- Clean up resources (files, DB records, network sockets)

### Examples

```python
import unittest

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Run once for the whole class
        cls.db = connect_to_test_db()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def setUp(self):
        # Run before each test
        self.db.reset()  # ensure clean state

    def tearDown(self):
        # Run after each test
        self.db.cleanup_temp()

    def test_insert_user(self):
        self.db.insert_user("alice")
        self.assertTrue(self.db.user_exists("alice"))

    def test_insert_duplicate_user_raises(self):
        self.db.insert_user("bob")
        with self.assertRaises(ValueError):
            self.db.insert_user("bob")
```

Module-level setup:

```python
# test_example.py
def setUpModule():
    print("Module setup")

def tearDownModule():
    print("Module teardown")
```

### Best Practices
- Avoid tests that depend on the **order** of execution
- Use `setUp` to prepare known-good starting state
- Clean up external resources in `tearDown` / `tearDownClass` / `tearDownModule`

---

## 4. Use Mocks to Test Code with Complex Dependencies

### Explanation
Some code depends on:
- External services (APIs, databases)
- Time, random numbers, environment, etc.

Mocks let you **replace these dependencies** with controllable fakes during tests, so you can:
- Run tests offline
- Make tests deterministic and fast
- Simulate error conditions

Python provides `unittest.mock` for this.

### Use Cases
- Mocking HTTP requests
- Mocking time (`datetime.now`, `time.time`)
- Mocking file system or DB calls

### Examples

```python
from unittest import TestCase
from unittest.mock import patch, MagicMock
import requests

def get_user_name(user_id):
    resp = requests.get(f"https://api.example.com/users/{user_id}")
    resp.raise_for_status()
    return resp.json()["name"]

class TestGetUserName(TestCase):
    @patch("requests.get")
    def test_get_user_name(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"name": "Alice"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Act
        name = get_user_name(123)

        # Assert
        self.assertEqual(name, "Alice")
        mock_get.assert_called_once_with("https://api.example.com/users/123")
```

### Guidelines
- Mock only **external interactions** (APIs, time, DB) – not internal logic
- Use `patch` with the **correct import path** (where the function is looked up, not where it’s defined)

---

## 5. Encapsulate Dependencies to Facilitate Mocking and Testing

### Explanation
Code is easier to test when dependencies (APIs, DBs, config) are:
- Passed in as arguments
- Wrapped behind small interfaces

This is **dependency injection**: rather than calling global functions directly, you accept them as parameters or attributes.

### Use Cases
- Making code testable without heavy mocking
- Swapping real dependencies for fakes in tests

### Examples

```python
# ❌ HARD TO TEST: Direct calls to requests and globals
import requests

def fetch_data():
    resp = requests.get("https://api.example.com/data")
    resp.raise_for_status()
    return resp.json()

# ✅ BETTER: Inject dependency
def fetch_data(session):
    resp = session.get("https://api.example.com/data")
    resp.raise_for_status()
    return resp.json()
```

In tests:

```python
from unittest import TestCase
from unittest.mock import MagicMock

class TestFetchData(TestCase):
    def test_fetch_data(self):
        fake_session = MagicMock()
        fake_resp = MagicMock()
        fake_resp.json.return_value = {"value": 42}
        fake_resp.raise_for_status.return_value = None
        fake_session.get.return_value = fake_resp

        result = fetch_data(fake_session)
        self.assertEqual(result, {"value": 42})
        fake_session.get.assert_called_once()
```

### Guidelines
- Pass dependencies (sessions, clients, repositories) into functions or class constructors
- Avoid module-level singletons that are hard to replace in tests

---

## 6. Use assertAlmostEqual to Control Precision in Floating Point Tests

### Explanation
Floating-point arithmetic is inherently imprecise. Direct equality (`==`) often fails due to tiny rounding errors.  
`TestCase.assertAlmostEqual` lets you compare two numbers within a tolerance:
- `places`: number of decimal places
- or `delta`: absolute tolerance

### Use Cases
- Testing numeric algorithms
- Checking results of calculations involving floats

### Examples

```python
import unittest

def area_of_circle(radius):
    import math
    return math.pi * radius * radius

class TestAreaOfCircle(unittest.TestCase):
    def test_area(self):
        result = area_of_circle(1)
        # ❌ BAD: direct equality
        # self.assertEqual(result, 3.141592653589793)

        # ✅ GOOD: use assertAlmostEqual
        self.assertAlmostEqual(result, 3.14159, places=5)

    def test_area_delta(self):
        result = area_of_circle(2)
        expected = 12.566370614359172
        self.assertAlmostEqual(result, expected, delta=1e-9)

if __name__ == "__main__":
    unittest.main()
```

### Guidelines
- Use `assertAlmostEqual` (or `math.isclose`) for float comparisons
- Choose tolerances based on the domain (e.g., money vs physics)

---

## 7. Consider Interactive Debugging with pdb

### Explanation
`pdb` is Python’s **built-in debugger**. It lets you:
- Pause execution at a breakpoint
- Inspect variables
- Step through code line by line
- Evaluate expressions interactively

### Use Cases
- Investigating failing tests
- Understanding unfamiliar code paths
- Reproducing tricky bugs

### Examples

Insert a breakpoint:

```python
def buggy_function(x, y):
    result = x + y
    import pdb; pdb.set_trace()  # breakpoint
    return result * 2
```

Run the code, and when it hits `set_trace()`, you can:
- `n` – next line
- `s` – step into
- `c` – continue
- `p variable` – print variable
- `q` – quit

Using from command line:

```bash
python -m pdb your_script.py
```

Or start debugger on an exception:

```bash
python -m pdb -c continue your_script.py
```

### Tips
- Use breakpoints **temporarily**, don’t leave them in committed code
- In modern Python, you can also use `breakpoint()` (honors `PYTHONBREAKPOINT` env var)

---

## 8. Use tracemalloc to Understand Memory Usage and Leaks

### Explanation
`tracemalloc` is a built-in module for tracking memory allocations in Python:
- Shows where memory is being allocated
- Helps detect memory leaks
- Useful for analyzing large or long-running programs

### Use Cases
- Web services that grow in memory over time
- Scripts that process large datasets
- Debugging unexpected memory spikes

### Examples

```python
import tracemalloc

tracemalloc.start()

run_heavy_code()

current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024 / 1024:.2f} MB; Peak: {peak / 1024 / 1024:.2f} MB")

tracemalloc.stop()
```

Top memory allocation locations:

```python
import tracemalloc

tracemalloc.start()
\nrun_heavy_code()

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics("lineno")

print("[ Top 10 memory allocations ]")
for stat in top_stats[:10]:
    print(stat)
```

### Guidelines
- Use `tracemalloc` in development or staging to understand memory behavior
- Combine with profiling to optimize both time and memory

---

## Summary

These eight principles help you write **reliable, testable, and debuggable** Python code:

1. **TestCase subclasses** – Group related tests and share setup  
2. **Integration tests** – Focus on real workflows, not just isolated units  
3. **Isolated tests** – Use `setUp`/`tearDown` to avoid test interference  
4. **Mocks** – Replace external dependencies with controllable fakes  
5. **Encapsulated dependencies** – Design code for easy testing and mocking  
6. **assertAlmostEqual** – Compare floating-point results safely  
7. **pdb** – Step through code interactively to understand and fix bugs  
8. **tracemalloc** – Analyze memory usage and find leaks  

Combining these techniques will make your Python codebase **easier to maintain, safer to change, and faster to debug**.
