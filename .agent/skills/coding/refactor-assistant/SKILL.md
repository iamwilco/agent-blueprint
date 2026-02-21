# Skill: Refactor Assistant
**Domain:** coding
**Version:** 1.1
**Eval Score:** 0.79

## Description
Perform safe, incremental refactoring: extract functions, rename symbols, reduce complexity, eliminate duplication — all while preserving behavior. Every refactor step must be individually testable.

## Usage
1. Identify the refactor target (high cyclomatic complexity, duplicated code, long function, unclear naming).
2. Confirm test coverage exists for the target. If not, write characterization tests first.
3. Apply one refactoring pattern at a time (see catalog below).
4. Run tests after each step — never batch multiple refactors before testing.
5. Commit each step separately with `refactor(<scope>): <description>`.

## Refactoring Catalog
| Pattern | When to Apply | Risk |
|---|---|---|
| Extract Function | Function >20 lines or does >1 thing | Low |
| Rename Symbol | Name doesn't convey intent | Low |
| Inline Variable | Temporary variable used once, adds no clarity | Low |
| Replace Magic Number | Literal values without context | Low |
| Extract Class/Module | Class has >2 responsibilities | Medium |
| Replace Conditional with Polymorphism | Switch/if chain on type | Medium |
| Introduce Parameter Object | Function takes >4 related params | Medium |

## Code Snippet
```python
# BEFORE: Long function with mixed concerns
def process_order(order):
    # validate
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Negative total")
    # calculate
    tax = order.total * 0.08
    shipping = 5.99 if order.total < 50 else 0
    final = order.total + tax + shipping
    # persist
    db.save(order)
    return final

# AFTER: Extracted functions, single responsibility
def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Negative total")

def calculate_total(subtotal: float) -> float:
    tax = subtotal * 0.08
    shipping = 5.99 if subtotal < 50 else 0
    return subtotal + tax + shipping

def process_order(order):
    validate_order(order)
    final = calculate_total(order.total)
    db.save(order)
    return final
```

## Eval Method
- **Metric:** Cyclomatic complexity delta (before vs after) + test pass rate stays 100%.
- **Tools:** `radon cc src/ -a` for complexity; `pytest` for regression.
- **Threshold:** Average complexity decreases by ≥1 grade (e.g., B→A) with zero test failures.
