# Collaboration: Effective Python Best Practices

## 1. Know Where to Find Community-Built Modules

### Explanation
Python’s strength comes from its huge ecosystem of third-party packages. Most community-built modules are published on:
- **PyPI (Python Package Index)** – main package repository
- GitHub / GitLab – source code, issues, documentation

### Use Cases
- Reusing battle-tested solutions instead of reinventing the wheel
- Finding libraries for web frameworks, data science, testing, etc.

### Examples

```bash
# Search PyPI from terminal
pip search requests

# Install a package
pip install requests

# Show info
pip show requests
```

Common categories:
- Web: `fastapi`, `django`, `flask`
- HTTP: `requests`, `httpx`
- Data: `numpy`, `pandas`, `sqlalchemy`
- Testing: `pytest`, `hypothesis`

### Tips
- Always check:
  - Downloads / popularity
  - Maintenance (recent releases, open issues)
  - License

---

## 2. Use Virtual Environments for Isolated and Reproducible Dependencies

### Explanation
Virtual environments (`venv`, `virtualenv`, `conda`) let each project have its **own set of packages**. This avoids:
- Version conflicts between projects
- Polluting global Python installation

### Use Cases
- Any non-trivial project
- Different projects needing different versions of the same library

### Examples

```bash
# Create venv
python3 -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install dependencies in this env
pip install fastapi uvicorn

# Freeze requirements
pip freeze > requirements.txt
```

### Guidelines
- Use **one venv per project**
- Track dependencies in `requirements.txt` or `pyproject.toml`
- Document activation steps in `README.md`

---

## 3. Write Docstrings for Every Function, Class, and Module

### Explanation
Docstrings are **string literals** immediately after a definition that describe:
- What the function/class/module does
- Its parameters and return values
- Any side effects or exceptions

They power:
- `help()` in Python
- IDE tooltips
- Documentation generators (e.g., Sphinx, pdoc)

### Use Cases
- Public APIs (functions/classes used by others)
- Complex internal utilities that need explanation

### Examples

```python
def add(a: int, b: int) -> int:
    """Add two integers.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Sum of a and b.
    """
    return a + b

class User:
    """Represents a user account in the system."""

    def __init__(self, username: str, email: str):
        """Create a new user.

        Args:
            username: Unique login name.
            email: Contact email address.
        """
        self.username = username
        self.email = email
```

Module docstring:

```python
"""User management module.

Provides functions and classes to create, authenticate, and manage users.
"""
```

### Guidelines
- Document **what** and **why**, not every trivial detail of how
- Keep docstrings up to date with code changes

---

## 4. Use Packages to Organize Modules and Provide Stable APIs

### Explanation
A **package** is a directory with an `__init__.py` file. Packages let you:
- Group related modules
- Provide a clean public API (what you export)
- Hide internal implementation details

### Use Cases
- Organizing medium/large projects
- Publishing libraries on PyPI

### Examples

```text
myapp/
    __init__.py
    models.py
    api/
        __init__.py
        users.py
        auth.py
```

In `myapp/api/__init__.py`:

```python
from .users import create_user, get_user
from .auth import login

__all__ = ["create_user", "get_user", "login"]
```

Consumers can import:

```python
from myapp.api import create_user, login
```

### Guidelines
- Expose a **small, stable API surface** via package `__init__.py`
- Treat modules not exported in `__all__` as internal

---

## 5. Consider Module-Scoped Code to Configure Deployment Environments

### Explanation
Module-level code runs **once on import**. It can be used (carefully) to:
- Configure logging
- Read environment variables
- Register plugins

But avoid heavy work at import time (slow startup, side effects).

### Use Cases
- Setting default logging format
- Configuring feature flags from environment

### Examples

```python
# config.py
import os

DEBUG = os.getenv("MYAPP_DEBUG", "0") == "1"
DATABASE_URL = os.getenv("MYAPP_DB_URL", "sqlite:///:memory:")
```

Logging config:

```python
# myapp/__init__.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
```

### Guidelines
- Keep module-level work **lightweight and side-effect-free** when possible
- For more complex initialization, provide explicit `init_app()` functions

---

## 6. Define a Root Exception to Insulate Callers from APIs

### Explanation
Libraries should define a **root exception class** (e.g., `MyLibraryError`) that all library-specific errors inherit from. This lets callers:
- Catch all library errors with a single `except`
- Distinguish library errors from system or other exceptions

### Use Cases
- Public libraries and SDKs
- Clear error boundaries between layers

### Examples

```python
class MyAppError(Exception):
    """Base exception for all MyApp errors."""

class ConfigError(MyAppError):
    """Configuration-related errors."""

class DatabaseError(MyAppError):
    """Database-related errors."""

def load_config(path):
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")
```

Callers:

```python
try:
    run_app()
except MyAppError as e:
    log_error(f"Application error: {e}")
    sys.exit(1)
```

### Benefits
- Easier error handling for consumers of your library
- Clear separation of **your** errors vs. everything else

---

## 7. Know How to Break Circular Dependencies

### Explanation
Circular imports happen when module A imports B and B imports A. This can cause:
- Import errors
- Partially initialized modules

Fix them by:
- Moving shared code to a third module
- Using **local imports** inside functions
- Refactoring to reduce coupling

### Examples

```python
# ❌ BAD: circular
# a.py
from b import func_b

def func_a():
    func_b()

# b.py
from a import func_a

def func_b():
    func_a()
```

### Fix 1: Extract shared functionality

```python
# common.py
def helper():
    ...

# a.py
from common import helper

# b.py
from common import helper
```

### Fix 2: Local imports (when truly necessary)

```python
# b.py
def func_b():
    from a import func_a  # imported only when needed
    func_a()
```

### Guidelines
- Prefer refactoring over local imports when possible
- Design modules with **clear directional dependencies**

---

## 8. Consider warnings to Refactor and Migrate Usage

### Explanation
The `warnings` module lets you emit **runtime warnings** without breaking code. Useful for:
- Deprecating functions or parameters
- Notifying users of behavior changes

### Use Cases
- Marking old APIs as deprecated
- Guiding users to new APIs during a transition period

### Examples

```python
import warnings

def old_function():
    warnings.warn(
        "old_function is deprecated, use new_function instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return new_function()
```

In tests, you can enforce no unexpected warnings:

```python
import warnings

with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    old_function()
    assert any(issubclass(wi.category, DeprecationWarning) for wi in w)
```

### Guidelines
- Use **specific warning classes** (`DeprecationWarning`, `UserWarning`, etc.)
- Include clear migration guidance in the message

---

## 9. Consider Static Analysis via typing to Obviate Bugs

### Explanation
Type hints (`typing`) plus static type checkers (`mypy`, `pyright`, etc.) catch many bugs **before runtime**:
- Wrong argument/return types
- Misuse of `None`
- Incorrect attribute access

### Use Cases
- Medium/large codebases
- Public APIs
- Critical logic where type safety helps

### Examples

```python
from typing import List

def average(values: List[float]) -> float:
    return sum(values) / len(values)
```

If you accidentally call `average("not a list")`, a type checker will complain.

Running mypy:

```bash
mypy your_project/
```

### Guidelines
- Add type hints gradually (you don’t have to annotate everything at once)
- Run a type checker in CI to prevent type regressions

---

## 10. Prefer Open Source Projects for Bundling Python Programs over zipimport and zipapp

### Explanation
Python supports packaging apps as **zip files** (`zipapp`, `zipimport`), but:
- They’re relatively low-level
- Missing conveniences for dependencies, reproducible builds, etc.

Instead, prefer existing open-source tools:
- `pipx`, `pip-tools`, `poetry`, `hatch`, `pdm`
- Docker images for deployment
- PyInstaller, Nuitka, etc. for standalone binaries

### Examples

```bash
# Using pipx to install a Python CLI globally in an isolated env
pipx install your-cli-package
```

Packaging with `poetry` (example):

```toml
# pyproject.toml
[tool.poetry]
name = "myapp"
version = "0.1.0"
description = "My awesome app"

[tool.poetry.dependencies]
python = "^3.11"
requests = "^2.31.0"
```

Then:

```bash
poetry build
poetry publish
```

### Guidelines
- Use modern packaging tools rather than rolling your own bundling
- Keep deployment scripts and configuration in version control

---

## Summary

These ten principles help you collaborate effectively on Python projects and libraries:

1. **Know the ecosystem** – Find and evaluate community packages on PyPI  
2. **Virtual environments** – Isolate and pin dependencies per project  
3. **Docstrings** – Document behavior for humans and tools  
4. **Packages** – Organize code and expose stable public APIs  
5. **Module-scoped configuration** – Light, explicit initialization at import time  
6. **Root exception types** – Give callers a single, clear error boundary  
7. **Breaking circular dependencies** – Design modules with clear directions  
8. **warnings module** – Deprecate and migrate APIs without breaking users  
9. **Static typing** – Catch whole classes of bugs before runtime  
10. **Modern packaging tools** – Rely on established solutions for distribution and deployment  

Following these practices makes your Python code **easier for others to use, extend, and maintain** over time.
