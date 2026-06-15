"""
Curriculum batch 2 — Python, Django, Flask.
Run: python manage.py generate_curriculum_2
"""
from django.core.management.base import BaseCommand
from academy.models import LearningPath, Lesson


def upsert(path, order, title, objective, content, exercise, quiz_q, project, notes, mins):
    qs = Lesson.objects.filter(learning_path=path, order=order)
    if qs.count() > 1:
        keep = qs.first().pk
        qs.exclude(pk=keep).delete()
        qs = Lesson.objects.filter(pk=keep)
    lesson = qs.first()
    if lesson:
        lesson.title = title; lesson.objective = objective
        lesson.content = content; lesson.exercise_prompt = exercise
        lesson.quiz_question = quiz_q; lesson.project_prompt = project
        lesson.notes = notes; lesson.estimated_minutes = mins
        lesson.save()
        return False
    Lesson.objects.create(
        learning_path=path, order=order, title=title, objective=objective,
        content=content, exercise_prompt=exercise, quiz_question=quiz_q,
        project_prompt=project, notes=notes, estimated_minutes=mins
    )
    return True


PYTHON_LESSONS = [
    (1, "Python Introduction — Syntax, Variables & Data Types",
     "Write and run Python programs, use variables, and understand Python's core data types.",
     '''## What is Python?

Python is a high-level, interpreted, dynamically-typed programming language created by Guido van Rossum in 1991. It is the world's most popular language for data science, AI/ML, web development, automation, and scripting.

**Why Python?**
- Simple, readable syntax — almost like English
- Huge standard library and ecosystem (300,000+ packages on PyPI)
- Runs on all platforms
- Dominant in AI/ML, data science, and automation

## Installation & Setup

```bash
# Download from python.org or:
# Windows: winget install Python.Python.3
# macOS:   brew install python@3

python --version    # verify
python3 --version   # on macOS/Linux

# Virtual environment — ALWAYS use for projects
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\\Scripts\\activate.bat    # Windows

# Install packages
pip install requests django pandas numpy

# Run a script
python app.py

# Interactive REPL
python
```

## First Python program

```python
# hello.py
print("Hello, CodeSavannah!")
print("Welcome to Python programming.")

# Python uses indentation (4 spaces) — no curly braces
# Comments start with #

# Multiple values
print("Name:", "Grace", "Age:", 17)

# f-strings (Python 3.6+) — the modern way to format strings
name = "Grace"
age  = 17
print(f"Name: {name}, Age: {age}")
print(f"In 5 years: {age + 5}")
```

## Variables and dynamic typing

```python
# No type declarations needed
name     = "Grace Adhiambo"   # str
age      = 17                  # int
gpa      = 3.9                 # float
is_active = True               # bool
score     = None               # NoneType

# Type changes at runtime
x = 42         # int
x = "hello"    # now str — valid in Python
x = [1, 2, 3]  # now list

# Check type
print(type(name))   # <class 'str'>
print(type(42))     # <class 'int'>

# Multiple assignment
a, b, c = 1, 2, 3
first, *rest = [10, 20, 30, 40]  # unpacking
print(first, rest)  # 10 [20, 30, 40]

# Constants — convention: UPPER_SNAKE_CASE
MAX_STUDENTS  = 100
DATABASE_URL  = "postgresql://localhost/academy"
```

## Numeric types and operators

```python
# int — unlimited precision
big = 1_000_000_000_000   # underscores for readability
print(big * big)

# float
pi = 3.14159265358979
import math
print(math.pi)         # 3.141592653589793
print(math.sqrt(144))  # 12.0
print(math.ceil(3.2))  # 4
print(math.floor(3.9)) # 3

# Arithmetic
print(10 + 3)   # 13
print(10 - 3)   # 7
print(10 * 3)   # 30
print(10 / 3)   # 3.3333... (float division)
print(10 // 3)  # 3   (integer division)
print(10 % 3)   # 1   (modulo / remainder)
print(2 ** 10)  # 1024 (exponentiation)

# divmod — quotient and remainder together
q, r = divmod(17, 5)  # q=3, r=2

# Comparison
print(10 == 10)  # True
print(10 != 5)   # True
print(10 > 5)    # True
print(10 >= 10)  # True

# Augmented assignment
x = 10
x += 5   # x = 15
x -= 3   # x = 12
x *= 2   # x = 24
x //= 5  # x = 4
x **= 3  # x = 64
```

## Strings — deep dive

```python
name = "Grace Adhiambo"

# Indexing — Python is 0-based
print(name[0])    # 'G'
print(name[-1])   # 'o'  (negative = from end)

# Slicing [start:stop:step]
print(name[0:5])   # "Grace"
print(name[6:])    # "Adhiambo"
print(name[:5])    # "Grace"
print(name[::2])   # every 2nd character
print(name[::-1])  # reversed: "obmaihhdA ecarG"

# Common string methods
s = "  Hello, World!  "
print(s.strip())          # "Hello, World!"
print(s.lstrip())         # "Hello, World!  "
print(s.rstrip())         # "  Hello, World!"
print(s.upper())          # "  HELLO, WORLD!  "
print(s.lower())          # "  hello, world!  "
print(s.title())          # "  Hello, World!  "
print(s.replace("World", "Python"))  # replace
print(s.find("World"))    # index of first match
print(s.count("l"))       # count occurrences
print(s.startswith(" "))  # True
print(s.endswith("!  "))  # True
print(s.split(", "))      # ["  Hello", "World!  "]
print("*".join(["a", "b", "c"]))  # "a*b*c"

# Multi-line strings — use parentheses for readability
bio = (
    "I am Grace, a Form 3 student at Nairobi Academy.\n"
    "I love coding and want to become a software engineer.\n"
)

# String formatting
name, gpa = "Grace", 3.9
# f-string (recommended)
msg = f"Student: {name}, GPA: {gpa:.2f}"

# .format() — older style
msg = "Student: {}, GPA: {:.2f}".format(name, gpa)

# % formatting — legacy
msg = "Student: %s, GPA: %.2f" % (name, gpa)
```

## Booleans and None

```python
# Truthy and Falsy values
# Falsy: False, 0, 0.0, "", [], {}, set(), None
# Truthy: everything else

print(bool(0))      # False
print(bool(""))     # False
print(bool([]))     # False
print(bool(None))   # False
print(bool(42))     # True
print(bool("hi"))   # True
print(bool([1]))    # True

# None — absence of value
result = None
if result is None:
    print("No result yet")
if result is not None:
    print("Got:", result)
```
''',
     "Write a Python script that: asks the user's name and age with input(), calculates their birth year, prints a formatted report using f-strings, and demonstrates 5 string methods on their name.",
     "In Python, what operator performs integer (floor) division?",
     "Build a Python currency converter: supports KES, USD, EUR, GBP, UGX. Accept amount and from/to currency from input, validate the currency codes, and display the result with proper formatting.",
     "Python uses indentation (4 spaces) to define code blocks — NOT curly braces. Mixing tabs and spaces causes IndentationError. Configure your editor to convert tabs to 4 spaces automatically.",
     40),

    (2, "Python Data Structures — Lists, Tuples, Sets & Dicts",
     "Master Python's four built-in data structures and know when to use each.",
     '''## Lists — ordered, mutable sequences

```python
# Create
fruits  = ["mango", "avocado", "pineapple"]
scores  = [85, 92, 78, 96, 70]
mixed   = [1, "hello", True, 3.14, None]
nested  = [[1, 2], [3, 4], [5, 6]]
empty   = []

# Access
print(fruits[0])    # "mango"
print(fruits[-1])   # "pineapple"
print(fruits[1:3])  # ["avocado", "pineapple"]

# Modify
fruits[0] = "banana"        # replace
fruits.append("papaya")     # add to end
fruits.insert(1, "orange")  # insert at index
fruits.extend(["guava", "passion"])  # add multiple
fruits.remove("avocado")    # remove first match
popped = fruits.pop()       # remove and return last
popped = fruits.pop(0)      # remove and return by index
del fruits[1]               # delete by index
fruits.clear()              # empty list

# Search & info
fruits = ["mango", "avocado", "pineapple"]
print("mango" in fruits)    # True
print(fruits.index("avocado")) # 1
print(fruits.count("mango"))   # 1
print(len(fruits))             # 3

# Sorting
scores = [85, 92, 78, 96, 70]
scores.sort()                     # in-place ascending
scores.sort(reverse=True)         # in-place descending
sorted_copy = sorted(scores)      # returns new list
scores.reverse()                  # reverse in-place

# Sort objects by attribute
students = [{"name": "Brian", "gpa": 2.8}, {"name": "Grace", "gpa": 3.9}]
students.sort(key=lambda s: s["gpa"], reverse=True)

# List comprehensions — Pythonic and fast
squares    = [x**2 for x in range(1, 11)]
evens      = [x for x in range(100) if x % 2 == 0]
names_up   = [name.upper() for name in ["grace", "brian", "amara"]]
flat       = [item for row in nested for item in row]

# zip — iterate two lists in parallel
names  = ["Grace", "Brian", "Amara"]
grades = ["A", "B", "A"]
for name, grade in zip(names, grades):
    print(f"{name}: {grade}")

pairs = list(zip(names, grades))  # [("Grace","A"), ("Brian","B"),...]

# enumerate — index + value
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")
```

## Tuples — ordered, immutable

```python
# Immutable — cannot change after creation
point    = (3, 7)
student  = ("Grace", 17, 3.9, "Form 3")
rgb      = (255, 128, 0)
single   = (42,)      # trailing comma required for single element
empty    = ()

# Access same as list
print(point[0])       # 3
x, y = point          # unpacking

# Why use tuples?
# - Faster than lists
# - Hashable — can be dict keys, in sets
# - Communicate "this should not change"
# - Return multiple values from functions

def min_max(numbers):
    return min(numbers), max(numbers)  # returns tuple

lo, hi = min_max([3, 1, 4, 1, 5, 9])
print(lo, hi)  # 1 9

# Named tuple — tuples with field names
from collections import namedtuple
Student = namedtuple("Student", ["name", "age", "gpa"])
grace = Student(name="Grace", age=17, gpa=3.9)
print(grace.name)  # "Grace"
print(grace[2])    # 3.9
```

## Sets — unordered, unique elements

```python
# No duplicates
skills = {"Python", "JavaScript", "CSS", "Python"}  # "Python" only once
print(skills)  # order not guaranteed

# Create
empty_set = set()   # NOT {} — that's an empty dict
from_list = set([1, 2, 2, 3, 3, 4])  # {1, 2, 3, 4}

# Modify
skills.add("Java")
skills.discard("CSS")  # no error if missing
skills.remove("CSS")   # KeyError if missing

# Set operations
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

print(a | b)   # union      {1,2,3,4,5,6,7,8}
print(a & b)   # intersection {4,5}
print(a - b)   # difference  {1,2,3}
print(a ^ b)   # symmetric difference {1,2,3,6,7,8}
print(a <= b)  # issubset?   False
print(b >= a)  # issuperset? False

# Use cases
registered  = {"Grace", "Brian", "Kofi"}
paid        = {"Grace", "Amara", "Brian"}
both        = registered & paid   # paid AND registered
only_reg    = registered - paid   # registered but not paid
```

## Dictionaries — key-value stores

```python
# Create
student = {
    "id":    1,
    "name":  "Grace Adhiambo",
    "grade": "Form 3",
    "gpa":   3.9,
    "courses": ["Python", "Web Dev"]
}

# Access
print(student["name"])                     # "Grace Adhiambo"
print(student.get("email", "No email"))    # default if missing

# Modify
student["email"] = "grace@example.com"    # add/update
student.update({"gpa": 4.0, "grade": "Form 4"})
del student["email"]
removed = student.pop("courses", None)    # remove and return

# Check
print("name" in student)                  # True (check key)
print("Grace" in student.values())        # True (check value)

# Iterate
for key in student:
    print(key)

for key, value in student.items():
    print(f"{key}: {value}")

for value in student.values():
    print(value)

# Dict comprehensions
squares = {x: x**2 for x in range(1, 6)}
# {1:1, 2:4, 3:9, 4:16, 5:25}

# Nested dict
courses_db = {
    "python": {"title": "Python", "level": "beginner", "price": 12000},
    "django": {"title": "Django", "level": "intermediate", "price": 18000},
}
print(courses_db["django"]["title"])

# defaultdict — no KeyError for missing keys
from collections import defaultdict
word_count = defaultdict(int)
for word in "the quick brown fox jumps over the lazy dog".split():
    word_count[word] += 1
print(dict(word_count))

# Counter — count occurrences
from collections import Counter
grades = ["A", "B", "A", "C", "A", "B", "A"]
counts = Counter(grades)
print(counts)            # Counter({'A': 4, 'B': 2, 'C': 1})
print(counts.most_common(2))  # [('A', 4), ('B', 2)]
```
''',
     "Build a Python word frequency counter: read a paragraph, split into words, count each word using a dictionary, sort by frequency, and print the top 10 most common words.",
     "Which Python data structure is unordered, contains only unique elements, and supports set operations like union and intersection?",
     "Build a student grade tracker: dictionary-based storage, add/update/delete students, calculate class average, find top 3 students, find students below average, and export to CSV. All implemented with list and dict comprehensions.",
     "Use dict.get(key, default) instead of dict[key] when the key might not exist — it never raises KeyError and lets you supply a default value cleanly.",
     50),

    (3, "Python Functions — Closures, Decorators & Functional Programming",
     "Write advanced Python functions including closures, decorators, generators, and lambda expressions.",
     '''## Function basics

```python
def greet(name, greeting="Hello"):
    \"\"\"Greet a person. Returns the greeting string.\"\"\"
    return f"{greeting}, {name}!"

print(greet("Grace"))               # "Hello, Grace!"
print(greet("Brian", "Habari"))     # "Habari, Brian!"
print(greet(greeting="Jambo", name="Amara"))  # keyword arg
```

## *args and **kwargs

```python
def total(*args):
    return sum(args)

print(total(1, 2, 3))        # 6
print(total(1, 2, 3, 4, 5))  # 15

def show_info(**kwargs):
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

show_info(name="Grace", gpa=3.9, grade="Form 3")

# Combine all types
def config(host, port=8000, *services, debug=False, **settings):
    print(host, port, services, debug, settings)

config("localhost", 8080, "redis", "celery", debug=True, workers=4)
```

## First-class functions

```python
# Functions are objects — can be assigned, passed, returned

def apply(func, value):
    return func(value)

def double(x): return x * 2
def square(x): return x ** 2

print(apply(double, 5))  # 10
print(apply(square, 5))  # 25

# Store in data structures
operations = [double, square, abs, len]
for op in operations:
    print(op.__name__, ":", op(8))
```

## Lambda functions

```python
# Small anonymous functions
double = lambda x: x * 2
add    = lambda x, y: x + y
grade  = lambda gpa: "A" if gpa >= 3.7 else "B" if gpa >= 3.0 else "C"

# Most useful in sorting and filtering
students = [
    {"name": "Grace", "gpa": 3.9},
    {"name": "Brian", "gpa": 2.8},
    {"name": "Amara", "gpa": 3.5},
]
students.sort(key=lambda s: s["gpa"], reverse=True)

scores = [85, 42, 91, 37, 78, 55]
passing = list(filter(lambda s: s >= 50, scores))
doubled = list(map(lambda s: s * 2, scores))
```

## Closures

```python
# A closure "remembers" variables from its enclosing scope

def make_counter(start=0):
    count = start

    def increment(step=1):
        nonlocal count
        count += step
        return count

    def reset():
        nonlocal count
        count = start

    def get():
        return count

    return increment, reset, get

inc, reset, get = make_counter(10)
print(inc())    # 11
print(inc(5))   # 16
print(get())    # 16
reset()
print(get())    # 10

# Practical closure — rate limiter
def make_logger(prefix):
    def log(message):
        import datetime
        print(f"[{datetime.datetime.now():%H:%M:%S}] [{prefix}] {message}")
    return log

info  = make_logger("INFO")
error = make_logger("ERROR")
info("Server started")
error("Database connection failed")
```

## Decorators

```python
import functools, time

# A decorator wraps a function to add behaviour
def timer(func):
    @functools.wraps(func)       # preserve original function metadata
    def wrapper(*args, **kwargs):
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        end    = time.perf_counter()
        print(f"{func.__name__!r} took {end-start:.4f}s")
        return result
    return wrapper

@timer
def slow_calculation(n):
    return sum(range(n))

slow_calculation(10_000_000)  # 'slow_calculation' took 0.3421s

# Decorator with arguments
def repeat(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Grace")  # prints 3 times

# login_required decorator (Django-style)
def login_required(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")
        return func(request, *args, **kwargs)
    return wrapper
```

## Generators — lazy iteration

```python
# Generator function — yields values one at a time
def fibonacci(limit):
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b

for n in fibonacci(100):
    print(n)

# Generator saves memory — creates values on demand
def read_large_file(path):
    with open(path) as f:
        for line in f:
            yield line.rstrip()

for line in read_large_file("students.csv"):
    process(line)

# Generator expression — like list comprehension but lazy
squares_gen = (x**2 for x in range(1_000_000))  # no memory allocated yet
print(next(squares_gen))   # 0
print(next(squares_gen))   # 1
print(sum(squares_gen))    # iterate and sum — memory-efficient
```
''',
     "Write a Python decorator called @retry(n, delay) that retries a function up to n times with delay seconds between attempts if it raises an exception. Test it with a function that randomly fails.",
     "In Python, what keyword is used in a generator function to yield a value without exiting the function?",
     "Build a Python task queue system: tasks stored as functions in a list, @timed decorator measuring execution time, @retry decorator for unreliable tasks, @log decorator writing to a file, and a generator that yields tasks one at a time.",
     "Use functools.wraps(func) inside every decorator wrapper — without it, the wrapped function loses its __name__ and __doc__, breaking debugging and introspection tools.",
     55),

    (4, "Python OOP — Classes, Inheritance & Magic Methods",
     "Model real-world systems in Python using classes, inheritance, and Python's special methods.",
     '''## Classes and Objects

```python
class Student:
    # Class variable — shared by all instances
    school    = "CodeSavannah Academy"
    _count    = 0      # private by convention

    def __init__(self, name: str, grade: str, gpa: float):
        # Instance variables
        self.name   = name
        self.grade  = grade
        self._gpa   = gpa           # _ convention: "private"
        self.__id   = Student._count + 1  # __ name-mangled
        Student._count += 1

    # Property — controlled access
    @property
    def gpa(self):
        return self._gpa

    @gpa.setter
    def gpa(self, value):
        if not (0.0 <= value <= 4.0):
            raise ValueError(f"GPA {value} is out of range 0.0–4.0")
        self._gpa = round(value, 2)

    @property
    def letter_grade(self):
        if self._gpa >= 3.7: return "A"
        if self._gpa >= 3.0: return "B"
        if self._gpa >= 2.0: return "C"
        if self._gpa >= 1.0: return "D"
        return "F"

    # Class method — factory pattern
    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["name"], data["grade"], data["gpa"])

    @classmethod
    def total_students(cls):
        return cls._count

    # Static method — utility (no self or cls)
    @staticmethod
    def is_valid_gpa(gpa: float) -> bool:
        return 0.0 <= gpa <= 4.0

    # Magic (dunder) methods
    def __str__(self):
        return f"{self.name} ({self.grade}, GPA {self._gpa:.2f})"

    def __repr__(self):
        return f"Student(name={self.name!r}, grade={self.grade!r}, gpa={self._gpa})"

    def __eq__(self, other):
        return isinstance(other, Student) and self.__id == other.__id

    def __lt__(self, other):
        return self._gpa < other._gpa

    def __len__(self):
        return len(self.name)

    def __hash__(self):
        return hash(self.__id)
```

## Inheritance and MRO

```python
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age  = age

    def greet(self):
        return f"Hi, I'm {self.name}"

class Student(Person):
    def __init__(self, name, age, grade, gpa):
        super().__init__(name, age)   # call parent __init__
        self.grade = grade
        self.gpa   = gpa

    def greet(self):
        base = super().greet()        # call parent method
        return f"{base}, studying at {self.grade}"

class WorkingStudent(Student):
    def __init__(self, name, age, grade, gpa, employer):
        super().__init__(name, age, grade, gpa)
        self.employer = employer

    def greet(self):
        return f"{super().greet()}, working at {self.employer}"

# Multiple inheritance
class Athlete:
    def compete(self): return f"{self.name} competes"

class SportyStudent(Student, Athlete):
    pass  # inherits from both

grace = SportyStudent("Grace", 17, "Form 3", 3.9)
grace.compete()   # works — from Athlete
grace.greet()     # works — from Student (MRO left-to-right)

print(SportyStudent.__mro__)  # method resolution order
```

## Abstract base classes

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    def __init__(self, color: str = "black"):
        self.color = color

    @abstractmethod
    def area(self) -> float: pass

    @abstractmethod
    def perimeter(self) -> float: pass

    def describe(self):
        return (f"{self.color} {type(self).__name__}: "
                f"area={self.area():.2f}, perimeter={self.perimeter():.2f}")

class Circle(Shape):
    import math as _math
    def __init__(self, radius: float, color="black"):
        super().__init__(color)
        self.radius = radius

    def area(self):      return 3.14159 * self.radius ** 2
    def perimeter(self): return 2 * 3.14159 * self.radius

class Rectangle(Shape):
    def __init__(self, w, h, color="black"):
        super().__init__(color)
        self.w, self.h = w, h

    def area(self):      return self.w * self.h
    def perimeter(self): return 2 * (self.w + self.h)

shapes = [Circle(5, "red"), Rectangle(4, 6, "blue"), Circle(3)]
for s in shapes:
    print(s.describe())

# Shape() raises TypeError: Can't instantiate abstract class
```

## Dataclasses (Python 3.7+)

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Course:
    id:       int
    title:    str
    level:    str = "beginner"
    price:    float = 0.0
    students: List[str] = field(default_factory=list)

    def enroll(self, name: str):
        if name not in self.students:
            self.students.append(name)

python_course = Course(1, "Python Programming", price=12000.0)
python_course.enroll("Grace")
print(python_course)  # auto __repr__
# Course(id=1, title='Python Programming', level='beginner', price=12000.0, students=['Grace'])
```
''',
     "Build a Python OOP system for a school library: abstract class LibraryItem with @abstractmethod checkout() and return_item(); Book and Magazine subclasses; Library class with search, list, and stats; use @property for price with validation.",
     "In Python, what decorator creates a read-only attribute that computes its value on access?",
     "Build a fully OOP E-commerce system: abstract Product class; PhysicalProduct and DigitalProduct subclasses; ShoppingCart with magic methods (__len__, __iter__, __add__); Order with status transitions; all code tested with assertions.",
     "Use @dataclass for simple data-holding classes — it auto-generates __init__, __repr__, and __eq__, removing boilerplate. Add frozen=True for immutable dataclasses.",
     55),

    (5, "Python File I/O, APIs & Data Processing",
     "Read/write files, call REST APIs, and process data with CSV and JSON.",
     '''## File I/O

```python
# Writing a file
with open("students.txt", "w", encoding="utf-8") as f:
    f.write("Grace Adhiambo, Form 3, 3.9\\n")
    f.write("Brian Ochieng, Form 2, 2.8\\n")
    # File is automatically closed — always use `with`

# Reading entire file
with open("students.txt", "r", encoding="utf-8") as f:
    content = f.read()   # entire file as string

# Reading line by line
with open("students.txt") as f:
    for line in f:            # memory-efficient for large files
        print(line.rstrip())

# Reading all lines into a list
with open("students.txt") as f:
    lines = f.readlines()

# Appending to a file
with open("log.txt", "a") as f:
    f.write("New log entry\\n")
```

## CSV files

```python
import csv

# Write CSV
students = [
    ["name", "grade", "gpa"],
    ["Grace", "Form 3", "3.9"],
    ["Brian", "Form 2", "2.8"],
]
with open("students.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(students)

# Read CSV
with open("students.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)  # read as list of dicts
    for row in reader:
        print(f"{row['name']}: GPA {row['gpa']}")

# Process CSV data
with open("students.csv") as f:
    reader = csv.DictReader(f)
    students = list(reader)

gpas    = [float(s["gpa"]) for s in students]
average = sum(gpas) / len(gpas)
top3    = sorted(students, key=lambda s: float(s["gpa"]), reverse=True)[:3]
```

## JSON files

```python
import json

# Python dict to JSON file
data = {
    "school": "CodeSavannah Academy",
    "courses": [
        {"id": 1, "title": "Python", "price": 12000},
        {"id": 2, "title": "Web Dev", "price": 15000},
    ]
}
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# JSON file to Python dict
with open("data.json") as f:
    loaded = json.load(f)
print(loaded["school"])
print(loaded["courses"][0]["title"])

# JSON string conversions
json_str   = json.dumps(data, indent=2)     # dict → string
back_again = json.loads(json_str)           # string → dict
```

## pathlib — modern file path handling

```python
from pathlib import Path

# Path operations
base      = Path("data")
csv_file  = base / "students.csv"  # works on all OSes
json_file = base / "config.json"

# Check
print(csv_file.exists())     # True/False
print(csv_file.is_file())
print(base.is_dir())

# File metadata
print(csv_file.stat().st_size)    # bytes
print(csv_file.suffix)            # ".csv"
print(csv_file.stem)              # "students"
print(csv_file.name)              # "students.csv"
print(csv_file.parent)            # Path("data")

# Create directories
Path("output/reports").mkdir(parents=True, exist_ok=True)

# Find files by pattern
for f in Path("data").glob("*.csv"):
    print(f)
```

## HTTP requests with requests library

```python
import requests

# GET request
response = requests.get("https://api.example.com/courses/")
print(response.status_code)  # 200
data = response.json()        # parse JSON response

# GET with parameters
params = {"level": "beginner", "page": 1}
r = requests.get("https://api.example.com/courses/", params=params)

# POST request
payload = {"name": "Grace", "email": "grace@example.com", "course": "python"}
r = requests.post("https://api.example.com/enrol/",
                  json=payload,
                  headers={"Authorization": "Bearer TOKEN"})
r.raise_for_status()   # raises exception for 4xx/5xx
print(r.json())

# Session — reuse connections, cookies
session = requests.Session()
session.headers.update({"Authorization": "Bearer TOKEN"})
r1 = session.get("/api/profile/")
r2 = session.get("/api/courses/")
```

## Error handling for files and APIs

```python
import requests
from pathlib import Path

def safe_read_json(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with p.open(encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {path}: {e}") from e

def fetch_courses(api_url: str, timeout: int = 10) -> list:
    try:
        r = requests.get(api_url, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except requests.Timeout:
        print("Request timed out — try again later")
        return []
    except requests.HTTPError as e:
        print(f"HTTP error {e.response.status_code}: {e.response.text[:200]}")
        return []
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return []
```
''',
     "Write a Python script that reads a CSV of 10 students, calculates average GPA, writes a JSON summary report, and prints the top 3 students formatted as a table.",
     "Which Python context manager keyword ensures a file is automatically closed after use?",
     "Build a Python data pipeline: read student enrolment CSV, call a mock API to get course details, merge the data, filter students at risk (GPA < 2.0), and write a JSON report and a formatted text report.",
     "Always open files with encoding='utf-8' explicitly — the default depends on the OS locale and can cause UnicodeDecodeError when moving code between machines.",
     50),

    (6, "Python Error Handling, Testing & Best Practices",
     "Write robust, tested Python code using exceptions, unittest, and professional patterns.",
     '''## Exception handling

```python
# Basic
try:
    result = int(input("Enter a number: "))
    print(100 / result)
except ValueError:
    print("That's not a valid integer")
except ZeroDivisionError:
    print("Cannot divide by zero")
except (TypeError, AttributeError) as e:
    print(f"Type error: {e}")
except Exception as e:
    print(f"Unexpected error: {type(e).__name__}: {e}")
else:
    print("Success!")     # runs only if no exception
finally:
    print("Done")         # always runs

# Custom exceptions
class CourseFullError(Exception):
    def __init__(self, course_name: str, capacity: int):
        super().__init__(f"{course_name!r} is full ({capacity} students)")
        self.course_name = course_name
        self.capacity    = capacity

class InvalidGPAError(ValueError):
    pass

def enrol(student, course):
    if course.is_full():
        raise CourseFullError(course.title, course.capacity)
    if not Student.is_valid_gpa(student.gpa):
        raise InvalidGPAError(f"Invalid GPA: {student.gpa}")

try:
    enrol(grace, python_course)
except CourseFullError as e:
    print(f"Enrolment failed: {e} | course={e.course_name}")
```

## Context managers

```python
# Using contextlib
from contextlib import contextmanager

@contextmanager
def database_transaction(db):
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise

with database_transaction(db) as conn:
    conn.execute("INSERT INTO students ...")

# Class-based context manager
class Timer:
    import time as _time

    def __enter__(self):
        self.start = self._time.perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed = self._time.perf_counter() - self.start
        print(f"Elapsed: {self.elapsed:.4f}s")
        return False  # don't suppress exceptions

with Timer() as t:
    result = sum(range(10_000_000))
```

## Unit testing with unittest

```python
import unittest

class Student:
    def __init__(self, name, gpa):
        if not name:           raise ValueError("Name required")
        if not 0 <= gpa <= 4:  raise ValueError("GPA must be 0-4")
        self.name = name
        self.gpa  = gpa

    def letter_grade(self):
        return "A" if self.gpa >= 3.7 else "B" if self.gpa >= 3.0 else "C"


class TestStudent(unittest.TestCase):

    def setUp(self):
        # Runs before each test
        self.grace = Student("Grace", 3.9)
        self.brian = Student("Brian", 2.8)

    def test_name_stored(self):
        self.assertEqual(self.grace.name, "Grace")

    def test_letter_grade_A(self):
        self.assertEqual(self.grace.letter_grade(), "A")

    def test_letter_grade_C(self):
        self.assertEqual(self.brian.letter_grade(), "C")

    def test_empty_name_raises(self):
        with self.assertRaises(ValueError):
            Student("", 3.5)

    def test_invalid_gpa_raises(self):
        with self.assertRaises(ValueError):
            Student("Valid", 5.0)

    def test_zero_gpa_valid(self):
        s = Student("Someone", 0.0)
        self.assertEqual(s.letter_grade(), "C")

    def tearDown(self):
        # Runs after each test
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

## pytest (industry standard)

```python
# pip install pytest pytest-cov
# Run: pytest tests/ -v
# Run with coverage: pytest --cov=academy tests/

import pytest

@pytest.fixture
def sample_student():
    return Student("Grace", 3.9)

@pytest.fixture
def sample_courses():
    return [
        Course(1, "Python", 12000),
        Course(2, "Web Dev", 15000),
    ]

def test_student_letter_grade(sample_student):
    assert sample_student.letter_grade() == "A"

@pytest.mark.parametrize("gpa,expected", [
    (4.0, "A"), (3.5, "B"), (2.5, "C"), (1.5, "D"), (0.5, "F"),
])
def test_letter_grades(gpa, expected):
    s = Student("Test", gpa)
    assert s.letter_grade() == expected

def test_invalid_gpa():
    with pytest.raises(ValueError, match="GPA must be 0-4"):
        Student("Valid", 5.0)
```

## Python best practices

```python
# 1. Use type hints (Python 3.9+)
def add_student(name: str, gpa: float) -> "Student":
    return Student(name, gpa)

# 2. Use walrus operator := (Python 3.8+)
if (n := len(students)) > 10:
    print(f"Too many students: {n}")

# 3. Use structural pattern matching (Python 3.10+)
match command:
    case "quit":              exit(0)
    case "list":              list_students()
    case "add" if has_perm:   add_student()
    case _:                   print("Unknown command")

# 4. Avoid bare except
# Bad:
try:
    risky()
except:        # catches EVERYTHING including SystemExit, KeyboardInterrupt
    pass

# Good:
try:
    risky()
except Exception as e:
    logger.error(f"Error: {e}")
```
''',
     "Write a test suite for a BankAccount class: test deposit, withdraw, transfer; test overdraft raises InsufficientFundsError; test negative amounts raise ValueError; achieve 100% code coverage.",
     "In Python testing, what decorator tests a function with multiple sets of input/output parameters?",
     "Build a fully tested Python library management system: 6 unit tests per class, custom exceptions, context manager for file operations, type hints throughout, and a CI-ready pytest configuration with coverage reporting.",
     "Write tests first (TDD) for critical business logic — it forces you to think about edge cases before writing code, not after finding bugs in production.",
     55),
]

DJANGO_LESSONS = [
    (1, "Django Introduction — MVT Pattern & Project Setup",
     "Set up a Django project and understand the Model-View-Template architecture.",
     '''## What is Django?

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It follows the Model-View-Template (MVT) architectural pattern and the DRY (Don't Repeat Yourself) principle.

**The Django philosophy:**
- *Batteries included* — admin, auth, ORM, forms, security all built in
- *Convention over configuration* — sensible defaults, less boilerplate
- *Security first* — CSRF, XSS, SQL injection protection by default

## Installation & Project Setup

```bash
# Create virtual environment (always!)
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\\Scripts\\activate     # Windows

# Install Django
pip install django

# Create a new project
django-admin startproject codesavannah .
# The trailing . puts manage.py in the current directory

# Project structure:
# codesavannah/          <- project config package
#     __init__.py
#     settings.py        <- all configuration
#     urls.py            <- root URL dispatcher
#     wsgi.py            <- WSGI server entry point
#     asgi.py            <- ASGI server (async)
# manage.py              <- command-line utility

# Start development server
python manage.py runserver
# Visit http://127.0.0.1:8000
```

## Django apps

```bash
# A Django project is made of apps
python manage.py startapp academy

# academy/
#     __init__.py
#     admin.py       <- register models for admin site
#     apps.py        <- app configuration
#     models.py      <- database models
#     views.py       <- request handlers
#     urls.py        <- URL patterns (create this)
#     tests.py       <- tests
#     migrations/    <- database schema versions

# Register the app in settings.py
INSTALLED_APPS = [
    ...
    'academy',      # add this
]
```

## MVT — Model, View, Template

```
HTTP Request
    ↓
URL Dispatcher (urls.py)
    ↓
View (views.py) — receives request, talks to model
    ↓
Model (models.py) — queries database
    ↓
View builds context dict
    ↓
Template (templates/) — renders HTML
    ↓
HTTP Response
```

## Your first view

```python
# academy/views.py
from django.shortcuts import render
from django.http import HttpResponse

# Function-Based View (FBV)
def home(request):
    context = {
        "title":   "CodeSavannah Academy",
        "tagline": "Learn. Build. Succeed.",
        "courses": ["Python", "Web Dev", "Cybersecurity"],
    }
    return render(request, "academy/home.html", context)

def about(request):
    return render(request, "academy/about.html")
```

## URL routing

```python
# academy/urls.py (create this file)
from django.urls import path
from . import views

urlpatterns = [
    path("",       views.home,  name="home"),
    path("about/", views.about, name="about"),
]

# codesavannah/urls.py — root URL conf
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/",   admin.site.urls),
    path("",         include("academy.urls")),
]
```

## Templates

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}CodeSavannah{% endblock %}</title>
</head>
<body>
<nav>
    <a href="{% url 'home' %}">Home</a>
    <a href="{% url 'about' %}">About</a>
</nav>

<main>{% block content %}{% endblock %}</main>

<footer>&copy; 2025 CodeSavannah</footer>
</body>
</html>
```

```html
<!-- templates/academy/home.html -->
{% extends "base.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<h1>{{ title }}</h1>
<p>{{ tagline }}</p>

<h2>Our Courses</h2>
<ul>
    {% for course in courses %}
        <li>{{ course }}</li>
    {% empty %}
        <li>No courses available yet.</li>
    {% endfor %}
</ul>
{% endblock %}
```

## Settings configuration

```python
# settings.py key settings

DEBUG = True  # MUST be False in production

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Database (default: SQLite, swap for PostgreSQL in production)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Templates
TEMPLATES = [{
    "DIRS": [BASE_DIR / "templates"],  # add this
    ...
}]

# Static files
STATIC_URL  = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # add this

# Time zone
TIME_ZONE = "Africa/Nairobi"
USE_TZ    = True
```
''',
     "Set up a new Django project called 'schoolsite', create an 'academics' app, write views for home and courses pages, configure URL routing, and create templates with template inheritance (base.html).",
     "In Django's MVT pattern, what component handles the HTTP request and decides which data to fetch and which template to render?",
     "Build a Django website for CodeSavannah Academy: home page with hero section, courses list page, individual course detail page, about page, and contact page with a form. All pages use template inheritance.",
     "Always keep DEBUG=False and ALLOWED_HOSTS properly set in production. Leaving DEBUG=True exposes your full stack trace and settings to the public internet.",
     50),

    (2, "Django Models & Database — ORM Mastery",
     "Define database models, run migrations, and query data using Django's ORM.",
     '''## Defining Models

```python
# academy/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Course(models.Model):
    LEVEL_CHOICES = [
        ("beginner",     "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced",     "Advanced"),
    ]

    title       = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=200, unique=True)
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="courses")
    description = models.TextField()
    level       = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="beginner")
    price       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    thumbnail   = models.ImageField(upload_to="course_thumbs/", blank=True)
    is_published = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)  # set once, on create
    updated_at  = models.DateTimeField(auto_now=True)      # updated on every save

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Enrolment(models.Model):
    STATUS = [("active", "Active"), ("completed", "Completed"), ("dropped", "Dropped")]

    student  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrolments")
    course   = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrolments")
    status   = models.CharField(max_length=20, choices=STATUS, default="active")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress = models.PositiveSmallIntegerField(default=0)  # 0–100

    class Meta:
        unique_together = [["student", "course"]]  # prevent duplicate enrolments

    def __str__(self):
        return f"{self.student.username} → {self.course.title}"
```

## Migrations

```bash
# Create migration files from model changes
python manage.py makemigrations

# Apply migrations to the database
python manage.py migrate

# Show migration status
python manage.py showmigrations

# SQL preview
python manage.py sqlmigrate academy 0001

# Undo a migration
python manage.py migrate academy 0001
```

## Django ORM — querying

```python
# Django shell
python manage.py shell

from academy.models import Course, Category, Enrolment

# CREATE
python_cat = Category.objects.create(name="Programming", slug="programming")
course = Course.objects.create(
    title="Python Programming",
    slug="python-programming",
    category=python_cat,
    description="Learn Python from scratch",
    level="beginner",
    price=12000,
    is_published=True,
)

# READ — QuerySets are lazy (no DB hit until evaluated)
Course.objects.all()                          # all courses
Course.objects.filter(level="beginner")       # filter
Course.objects.filter(price__lt=15000)        # less than
Course.objects.filter(title__icontains="py")  # case-insensitive contains
Course.objects.filter(category__name="Programming")  # related model
Course.objects.exclude(is_published=False)    # exclude
Course.objects.get(slug="python-programming") # single object (raises if not found)
Course.objects.first()                        # first (or None)
Course.objects.last()
Course.objects.count()                        # COUNT query

# Ordering
Course.objects.order_by("price")              # ascending
Course.objects.order_by("-price")             # descending
Course.objects.order_by("level", "-price")   # multiple

# Slicing (LIMIT/OFFSET)
Course.objects.all()[:5]        # first 5
Course.objects.all()[5:10]      # offset 5, limit 5

# Select related — avoid N+1 queries
courses = Course.objects.select_related("category").filter(is_published=True)
for c in courses:
    print(c.category.name)  # no extra query per course

# Prefetch related — for many-to-many and reverse FK
courses = Course.objects.prefetch_related("enrolments__student").all()

# UPDATE
Course.objects.filter(level="beginner").update(price=10000)
course.price = 12000
course.save()          # save all fields
course.save(update_fields=["price"])  # save one field only

# DELETE
Course.objects.filter(is_published=False).delete()
course.delete()

# Aggregation
from django.db.models import Avg, Count, Max, Min, Sum

Course.objects.aggregate(Avg("price"))  # {"price__avg": 13500.0}
Course.objects.aggregate(Count("id"), Avg("price"), Max("price"))

# Annotation — add aggregate data to each object
from django.db.models import Count
courses = Course.objects.annotate(num_enrolments=Count("enrolments"))
for c in courses:
    print(f"{c.title}: {c.num_enrolments} students")

# Q objects — complex queries (OR, NOT)
from django.db.models import Q
Course.objects.filter(Q(level="beginner") | Q(price__lt=10000))
Course.objects.filter(Q(is_published=True) & ~Q(level="advanced"))
```
''',
     "Build Django models for a blog: Category, Post (with ForeignKey to Category and ManyToManyField to Tag), Comment (with ForeignKey to Post). Run migrations, then use the shell to create 3 posts, add tags, and query: posts by category, recent posts, post with most comments.",
     "Which Django ORM method adds aggregate data (like count) as a computed field to each object in a QuerySet?",
     "Build a Django app with models for Student, Course, and Enrolment. Write ORM queries for: (1) top 5 most enrolled courses, (2) students with 3+ active enrolments, (3) completion rate per course, (4) students who enrolled this month.",
     "Use select_related() for ForeignKey/OneToOne fields and prefetch_related() for ManyToMany/reverse FK to prevent N+1 query problems. The Django Debug Toolbar is invaluable for spotting these.",
     55),

    (3, "Django Views, Forms & Authentication",
     "Handle form submission, user registration, login, and access control.",
     '''## Class-Based Views

```python
# academy/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Course

class CourseListView(ListView):
    model               = Course
    template_name       = "academy/course_list.html"
    context_object_name = "courses"
    paginate_by         = 12

    def get_queryset(self):
        qs = Course.objects.filter(is_published=True).select_related("category")
        level = self.request.GET.get("level")
        if level:
            qs = qs.filter(level=level)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["levels"] = Course.objects.values_list("level", flat=True).distinct()
        return ctx

class CourseDetailView(DetailView):
    model               = Course
    template_name       = "academy/course_detail.html"
    context_object_name = "course"

class CourseCreateView(LoginRequiredMixin, CreateView):
    model         = Course
    fields        = ["title", "description", "level", "price", "category"]
    template_name = "academy/course_form.html"
    success_url   = reverse_lazy("course-list")

    def form_valid(self, form):
        # Hook into form submission — set author etc.
        return super().form_valid(form)
```

## Django Forms

```python
# academy/forms.py
from django import forms
from .models import Course, Enrolment

class EnrolmentForm(forms.ModelForm):
    class Meta:
        model  = Enrolment
        fields = ["course"]
        widgets = {
            "course": forms.Select(attrs={"class": "form-select"})
        }

class ContactForm(forms.Form):
    name    = forms.CharField(max_length=100)
    email   = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}))

    def clean_message(self):
        msg = self.cleaned_data["message"]
        if len(msg) < 20:
            raise forms.ValidationError("Message must be at least 20 characters.")
        return msg

    def send_email(self):
        from django.core.mail import send_mail
        send_mail(
            self.cleaned_data["subject"],
            self.cleaned_data["message"],
            self.cleaned_data["email"],
            ["support@codesavannah.ac"],
        )
```

```python
# Form handling in a view
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_email()
            messages.success(request, "Message sent! We'll reply within 24 hours.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "academy/contact.html", {"form": form})
```

## User Authentication

```python
# Registration view
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout

def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after register
            messages.success(request, "Account created! Welcome.")
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "auth/register.html", {"form": form})

# Login/Logout — use Django's built-ins in urls.py
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/",  auth_views.LoginView.as_view(template_name="auth/login.html"),  name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", views.register, name="register"),
]

# settings.py
LOGIN_URL          = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"
```

## Access control

```python
# Decorators for FBVs
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def dashboard(request):
    enrolments = request.user.enrolments.select_related("course").all()
    return render(request, "academy/dashboard.html", {"enrolments": enrolments})

@permission_required("academy.add_course", raise_exception=True)
def create_course(request):
    pass

# Mixins for CBVs
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class DashboardView(LoginRequiredMixin, ListView):
    login_url = "/login/"  # override default

class AdminCourseView(PermissionRequiredMixin, CreateView):
    permission_required = "academy.add_course"
```

## Django messages framework

```python
# In views
from django.contrib import messages
messages.debug(request, "Debug info")
messages.info(request, "FYI")
messages.success(request, "Course created successfully!")
messages.warning(request, "Your subscription expires in 3 days.")
messages.error(request, "Payment failed. Please try again.")

# In templates — base.html
{% if messages %}
<ul class="messages">
    {% for message in messages %}
    <li class="{{ message.tags }}">{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}
```
''',
     "Build a Django app with user registration and login, a protected dashboard showing the logged-in user's enrolments, and a contact form with validation that sends an email on submission.",
     "Which Django decorator restricts a view to authenticated users only and redirects to the login page otherwise?",
     "Build a full Django authentication system: custom user model with email as username, registration with email verification, password reset via email, profile page with photo upload, and role-based access (student vs trainer).",
     "Use Django's built-in auth views (LoginView, LogoutView, PasswordResetView) rather than writing your own — they handle security edge cases that are easy to miss in custom implementations.",
     60),

    (4, "Django REST Framework & APIs",
     "Build production-quality REST APIs with Django REST Framework.",
     '''## Django REST Framework Setup

```bash
pip install djangorestframework djangorestframework-simplejwt django-cors-headers

# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # FIRST
    ...
]
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
```

## Serializers

```python
# academy/serializers.py
from rest_framework import serializers
from .models import Course, Enrolment
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ["id", "name", "slug"]

class CourseSerializer(serializers.ModelSerializer):
    category         = CategorySerializer(read_only=True)
    category_id      = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    enrolment_count  = serializers.IntegerField(source="enrolments.count", read_only=True)

    class Meta:
        model  = Course
        fields = ["id", "title", "slug", "category", "category_id",
                  "description", "level", "price", "is_published",
                  "enrolment_count", "created_at"]
        read_only_fields = ["id", "slug", "created_at"]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

class EnrolmentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    course  = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.filter(is_published=True),
        source="course", write_only=True
    )

    class Meta:
        model  = Enrolment
        fields = ["id", "student", "course", "course_id", "status", "progress", "enrolled_at"]
        read_only_fields = ["id", "student", "enrolled_at"]
```

## API Views — ViewSets

```python
# academy/api_views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

class CourseViewSet(viewsets.ModelViewSet):
    queryset         = Course.objects.filter(is_published=True).select_related("category")
    serializer_class = CourseSerializer
    lookup_field     = "slug"

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = super().get_queryset()
        level = self.request.query_params.get("level")
        search = self.request.query_params.get("search")
        if level:  qs = qs.filter(level=level)
        if search: qs = qs.filter(title__icontains=search)
        return qs

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def enrol(self, request, slug=None):
        course = self.get_object()
        enrolment, created = Enrolment.objects.get_or_create(
            student=request.user, course=course
        )
        if not created:
            return Response({"detail": "Already enrolled."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(EnrolmentSerializer(enrolment).data, status=status.HTTP_201_CREATED)
```

## URL routing with Router

```python
# academy/urls.py
from rest_framework.routers import DefaultRouter
from .api_views import CourseViewSet, EnrolmentViewSet

router = DefaultRouter()
router.register("courses",    CourseViewSet,    basename="course")
router.register("enrolments", EnrolmentViewSet, basename="enrolment")

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/token/",         TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(),    name="token_refresh"),
]
# Auto-generates:
# GET/POST /api/v1/courses/
# GET/PUT/PATCH/DELETE /api/v1/courses/{slug}/
# POST /api/v1/courses/{slug}/enrol/
```
''',
     "Build a Django REST API for a todo list: CRUD endpoints for Todo items, filter by status and priority, JWT authentication, and write tests using APITestCase.",
     "In Django REST Framework, what class automatically generates CRUD URL patterns for a ModelViewSet?",
     "Build a complete REST API for CodeSavannah Academy: courses, enrolments, user profile, and progress tracking endpoints. Include JWT auth, rate limiting, API versioning, and comprehensive tests.",
     "Use select_related() in ViewSet.get_queryset() to avoid N+1 queries. Every extra DB round-trip in an API adds latency — even 10ms per query becomes 1 second for 100 nested objects.",
     65),
]

FLASK_LESSONS = [
    (1, "Flask Introduction — Routes, Templates & Forms",
     "Build web applications with Flask, understanding its minimalist approach vs Django.",
     '''## What is Flask?

Flask is a micro web framework for Python — it gives you the core tools (routing, templating, request handling) without opinions about database, ORM, or project structure. You choose and integrate what you need.

**Flask vs Django:**
| Feature | Flask | Django |
|---------|-------|--------|
| Size | Micro-framework | Full-stack framework |
| ORM | Choose your own | Built-in |
| Admin | Build yourself | Auto-generated |
| Learning curve | Lower | Higher |
| Flexibility | Very high | Opinionated |
| Best for | APIs, microservices, small apps | Large, full-featured apps |

## Setup

```bash
pip install flask flask-sqlalchemy flask-wtf python-dotenv

# Project structure
flask-app/
    app/
        __init__.py
        models.py
        routes.py
        forms.py
        templates/
        static/
    config.py
    run.py
```

## Application factory pattern

```python
# app/__init__.py
from flask import Flask
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from .routes import main
    app.register_blueprint(main)

    return app

# run.py
from app import create_app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

## Routes and views

```python
# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash

main = Blueprint("main", __name__)

@main.route("/")
def home():
    courses = [
        {"title": "Python", "level": "beginner"},
        {"title": "Web Dev", "level": "beginner"},
    ]
    return render_template("home.html", courses=courses, title="CodeSavannah")

@main.route("/course/<slug>")
def course_detail(slug):
    return render_template("course.html", slug=slug)

# Accept multiple methods
@main.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name  = request.form.get("name")
        email = request.form.get("email")
        msg   = request.form.get("message")
        # process...
        flash("Message sent!", "success")
        return redirect(url_for("main.contact"))
    return render_template("contact.html")

# URL with types
@main.route("/users/<int:user_id>")
def user_profile(user_id: int):
    return f"User {user_id}"

@main.route("/api/courses/")
def api_courses():
    from flask import jsonify
    data = [{"id": 1, "title": "Python"}, {"id": 2, "title": "Django"}]
    return jsonify(data)
```

## Jinja2 templates

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}CodeSavannah{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
    <div class="alert alert-{{ category }}">{{ message }}</div>
    {% endfor %}
{% endwith %}

{% block content %}{% endblock %}
</body>
</html>
```

```html
<!-- templates/home.html -->
{% extends "base.html" %}

{% block title %}Home — {{ super() }}{% endblock %}

{% block content %}
<h1>Welcome to {{ title }}</h1>

{% for course in courses %}
<div class="card">
    <h2>{{ course.title }}</h2>
    <span class="badge badge-{{ course.level }}">{{ course.level | title }}</span>
</div>
{% else %}
<p>No courses available.</p>
{% endfor %}

{{ "hello" | upper }}   {# Jinja2 filter #}
{{ price | round(2) }}
{{ text  | truncate(100) }}
{{ name  | default("Anonymous") }}
{% endblock %}
```

## Flask-WTF Forms

```python
# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SelectField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    name    = StringField("Name",    validators=[DataRequired(), Length(2, 100)])
    email   = EmailField("Email",    validators=[DataRequired(), Email()])
    subject = StringField("Subject", validators=[DataRequired(), Length(5, 200)])
    message = TextAreaField("Message", validators=[DataRequired(), Length(20, 2000)])
```

## Configuration

```python
# config.py
import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY          = os.getenv("SECRET_KEY", "dev-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED    = True
```
''',
     "Build a Flask app with: home route listing 5 courses (from a Python list), individual course route with a slug, a contact form with WTF validation, and a REST endpoint returning courses as JSON.",
     "In Flask, what decorator registers a function as the handler for a specific URL route?",
     "Build a Flask blog with: list all posts, view individual post, create/edit/delete post (admin only), comment submission form, and a JSON API endpoint for posts. Use Jinja2 template inheritance.",
     "Always set a strong SECRET_KEY for Flask — it's used to sign session cookies. A weak or exposed key lets attackers forge sessions and impersonate any user.",
     50),

    (2, "Flask + SQLAlchemy — Database Models & CRUD",
     "Persist data with Flask-SQLAlchemy and build full CRUD applications.",
     '''## Flask-SQLAlchemy Setup

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db      = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///academy.db"
    app.config["SECRET_KEY"] = "change-in-production"

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main
    app.register_blueprint(main)

    return app
```

```bash
# Migrations with Flask-Migrate
pip install flask-migrate

flask db init       # create migrations folder (once)
flask db migrate -m "Add Course model"
flask db upgrade
flask db downgrade
```

## Models

```python
# app/models.py
from . import db
from datetime import datetime, timezone

class Category(db.Model):
    __tablename__ = "categories"

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)

    courses = db.relationship("Course", backref="category", lazy="dynamic")

    def __repr__(self):
        return f"<Category {self.name}>"

class Course(db.Model):
    __tablename__ = "courses"

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    slug        = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    level       = db.Column(db.Enum("beginner","intermediate","advanced", name="level_enum"), default="beginner")
    price       = db.Column(db.Numeric(10, 2), default=0)
    is_published = db.Column(db.Boolean, default=False, index=True)
    created_at  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    enrolments  = db.relationship("Enrolment", backref="course", lazy="dynamic", cascade="all,delete")

    def to_dict(self):
        return {
            "id": self.id, "title": self.title, "slug": self.slug,
            "level": self.level, "price": float(self.price),
        }

# Association table — many-to-many
tags = db.Table("course_tags",
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id")),
    db.Column("tag_id",    db.Integer, db.ForeignKey("tags.id")),
)

class Tag(db.Model):
    __tablename__ = "tags"
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    courses = db.relationship("Course", secondary=tags, backref="tags")
```

## CRUD routes

```python
# Full CRUD
@main.route("/courses/")
def course_list():
    level  = request.args.get("level")
    search = request.args.get("q")
    query  = Course.query.filter_by(is_published=True)
    if level:  query = query.filter_by(level=level)
    if search: query = query.filter(Course.title.ilike(f"%{search}%"))
    courses = query.order_by(Course.created_at.desc()).paginate(per_page=12)
    return render_template("courses.html", courses=courses)

@main.route("/courses/create", methods=["GET", "POST"])
def course_create():
    form = CourseForm()
    if form.validate_on_submit():
        from slugify import slugify
        course = Course(
            title=form.title.data,
            slug=slugify(form.title.data),
            description=form.description.data,
            level=form.level.data,
            price=form.price.data,
        )
        db.session.add(course)
        db.session.commit()
        flash("Course created successfully!", "success")
        return redirect(url_for("main.course_list"))
    return render_template("course_form.html", form=form)

@main.route("/courses/<slug>/edit", methods=["GET", "POST"])
def course_edit(slug):
    course = Course.query.filter_by(slug=slug).first_or_404()
    form   = CourseForm(obj=course)
    if form.validate_on_submit():
        form.populate_obj(course)
        db.session.commit()
        flash("Course updated.", "success")
        return redirect(url_for("main.course_detail", slug=course.slug))
    return render_template("course_form.html", form=form, course=course)

@main.route("/courses/<slug>/delete", methods=["POST"])
def course_delete(slug):
    course = Course.query.filter_by(slug=slug).first_or_404()
    db.session.delete(course)
    db.session.commit()
    flash("Course deleted.", "warning")
    return redirect(url_for("main.course_list"))
```
''',
     "Build a Flask app with SQLAlchemy models for Task (title, description, status, due_date) and Category. Implement full CRUD: list, create, update, delete, filter by status and category.",
     "In Flask-SQLAlchemy, what method commits changes to the database within the current session?",
     "Build a Flask bookmark manager: User model with Flask-Login authentication, Bookmark model (url, title, tags, is_private), full CRUD, search by title/tag, and an import/export feature for JSON.",
     "Use db.session.add() followed by db.session.commit() for creates and updates. Never call commit() inside a loop — batch multiple operations in one transaction for performance.",
     55),
]


BATCH_2 = [
    ("python", "Python Programming", "programming", "beginner", "8 weeks",
     "Python 3, OOP, File I/O, APIs, Testing, Data Structures",
     "Master Python from variables to advanced patterns — the world's most versatile language.", PYTHON_LESSONS),

    ("django", "Django Web Framework", "web", "intermediate", "8 weeks",
     "Django, MVT, ORM, REST API, Authentication, PostgreSQL",
     "Build full-featured web applications with Django — Python's premier web framework.", DJANGO_LESSONS),

    ("flask", "Flask Microframework", "web", "intermediate", "6 weeks",
     "Flask, SQLAlchemy, Jinja2, REST APIs, Flask-Login",
     "Build lightweight, flexible web apps and APIs with Flask.", FLASK_LESSONS),
]


class Command(BaseCommand):
    help = "Generate curriculum batch 2: Python, Django, Flask"

    def handle(self, *args, **options):
        total_created = total_updated = 0

        for (slug, title, category, level, duration, skills, summary, lessons) in BATCH_2:
            path, p_created = LearningPath.objects.get_or_create(
                slug=slug,
                defaults=dict(title=title, category=category, level=level,
                              duration=duration, skill_stack=skills,
                              summary=summary, is_featured=True)
            )
            if not p_created:
                path.title = title; path.category = category; path.level = level
                path.duration = duration; path.skill_stack = skills
                path.summary = summary; path.is_featured = True
                path.save()

            for lesson_data in lessons:
                created = upsert(path, *lesson_data)
                if created: total_created += 1
                else:       total_updated += 1

            self.stdout.write(f'  {"+" if p_created else "~"} {title}: {len(lessons)} lessons')

        self.stdout.write(self.style.SUCCESS(
            f"\nBatch 2 done — {total_created} lessons created, {total_updated} updated."
        ))
