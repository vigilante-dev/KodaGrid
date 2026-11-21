---
kind: learning_path
title: Python: Practical Programming
slug: python-foundations
category: programming
level: beginner
duration: 6 stages · self-paced
skill_stack: Python, functions, collections, files, testing
summary: Solve practical problems with readable Python, well-tested functions, and careful handling of files and input.
language: en
stages:
  - {order: 1, stage: Beginner, slug: beginner-python, estimated_minutes: 45}
  - {order: 2, stage: Intermediate, slug: intermediate-python, estimated_minutes: 50}
  - {order: 3, stage: Advanced, slug: advanced-python, estimated_minutes: 55}
  - {order: 4, stage: Projects, slug: python-projects, estimated_minutes: 70}
  - {order: 5, stage: Challenges, slug: python-challenges, estimated_minutes: 40}
  - {order: 6, stage: Final Assessment, slug: python-assessment, estimated_minutes: 50}
references:
  - https://docs.python.org/3/tutorial/
  - https://docs.python.org/3/library/
originality: Original CoderGrid instructional content; references identify authoritative documentation.
---

# Python · Practical Programming

Python emphasizes readable code and comes with a broad standard library. Use a current supported Python 3 release, and practise with short scripts in a local interpreter or offline editor.

## Beginner

**Objectives:** assign values, use built-in types, make decisions, repeat work, and define functions.

```python
harvest_kg = [12, 9, 15]
total = sum(harvest_kg)
def average(values):
    if not values:
        return 0
    return sum(values) / len(values)

print(f"Collected {total} kg; average {average(harvest_kg):.1f} kg.")
```

Indentation groups a block. The function parameter `values` receives an argument; `return` gives a result. A list keeps ordered values; `sum` and `len` are built-ins. An f-string inserts values into text.

**Try it:** calculate the total and average daily water use from fictional whole-litre values. What should an empty list return? Pick and document a sensible behaviour.

**Practice / answers:** What begins a function definition? `def`. What does `range(3)` produce when iterated? 0, 1, 2. Why use `==` rather than `=` in a condition? `==` compares; `=` assigns.

**Mistakes and habits:** indentation errors, off-by-one ranges, and assuming user input is numeric. Name values clearly, convert input explicitly, and handle empty collections.

## Intermediate

**Objectives:** choose dictionaries and sets, transform collections, and recover from expected input errors.

```python
stock = {"beans": 8, "maize": 13}
stock["beans"] -= 2
low_items = [name for name, count in stock.items() if count < 10]
try:
    requested = int(input("How many units? "))
except ValueError:
    print("Enter a whole number, such as 3.")
```

A dictionary maps keys to values. `.items()` yields key/value pairs. A list comprehension creates a new list from an iterable and optional condition. Catch a specific expected exception, not every possible failure.

**Exercise:** make a fictional book-loan tracker with a dictionary of titles and copies. Reject negative quantities and report missing titles clearly.

**Practice:** Which collection removes duplicates? A set. What does `dict.get(key, default)` do? Returns a stored value or the default. Why catch `ValueError` here? Conversion can fail for non-numeric text.

**Mini project:** build a market stock report that totals products by category and identifies items below a threshold. Keep calculations in functions and test edge cases.

**Habits:** use `with` for files, validate at boundaries, and keep functions focused. Avoid broad exception handling that hides programming errors.

## Advanced

**Objectives:** work with iterators, context managers, modules, and tests while managing side effects.

```python
from pathlib import Path
import json

def save_report(path: Path, report: dict) -> None:
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
```

`Path` represents file-system paths; JSON serialization supports basic data types. File writes can fail due to permissions, missing directories, or storage conditions, so production code should handle those expected failures. Keep imports at module scope and avoid executing costly work just by importing a module.

**Challenge:** refactor a script into a module with pure calculation functions, a `main()` entry point, and unit tests for empty data, malformed input, and normal results.

**Best practices:** use a virtual environment per project, pin dependencies thoughtfully, document setup, protect secrets, and don't deserialize untrusted pickle data. Add type hints where they clarify contracts; test behaviour, not implementation details.

**Quiz / answers:** What does `if __name__ == "__main__":` support? Running a module as a script without automatically running its CLI on import. What is an iterator? An object producing values one at a time. What does `with` commonly manage? Resource setup and cleanup.

## Projects

Create **Cooperative Savings Ledger (Practice)** for fictional members and amounts. Add deposits, calculate totals, show a summary, and export JSON or CSV. Do not use real financial details. Validate input, make a backup before replacing an export, and write tests for totals and invalid entries.

**Deliverables:** source, tests, sample fictional data, README, and a note about data privacy. **Review:** can calculations run without prompting? Are file errors understandable? Can another learner reproduce the environment?

## Challenges

1. Find an off-by-one error in a daily-report loop.
2. Count the frequency of words in a short Swahili or English sample while defining how punctuation is handled.
3. Stream a large text file line by line rather than reading all of it at once.
4. Add tests for zero, missing, and malformed values.

**Hint:** reduce the problem to a small example, then test the function with expected input/output pairs.

## Final Assessment

Write a tested program that summarizes fictional community library activity.

1. Which type maps title to copy count? A dictionary.
2. How do you handle a non-integer conversion? Catch `ValueError` around conversion.
3. Why use `with` for an opened file? It reliably closes the file.
4. What should an empty-data case do? An explicit, documented result.
5. Where should testable business logic live? In functions independent of interactive input/output.

**Rubric (20):** correct calculations 5; data structures and functions 4; input/file handling 4; tests and edge cases 4; setup notes and privacy 3.
