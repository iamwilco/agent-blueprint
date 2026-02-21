# Skill: Performance Tuning
**Domain:** optimization
**Version:** 1.0
**Eval Score:** —

## Description
Identify and resolve performance bottlenecks: slow queries, N+1 problems, excessive memory allocation, unoptimized algorithms, missing caches. Always measure before and after — no speculative optimization.

## Usage
1. **Measure first** — Profile the slow path. Get a baseline metric (latency, throughput, memory).
2. **Identify the bottleneck** — Use profiling tools to find the hot spot.
3. **Apply the smallest fix** — Optimize the bottleneck, not everything.
4. **Measure again** — Confirm improvement with the same benchmark.
5. **Document** — Log the before/after in the task outcome.

## Profiling Toolkit

### Python: cProfile + snakeviz
```bash
python -m cProfile -o profile.out app.py
snakeviz profile.out  # Visual flame graph in browser
```

### Python: line_profiler for hot functions
```python
# Add @profile decorator to suspect functions, then:
# kernprof -l -v script.py
@profile
def process_orders(orders: list[Order]) -> list[Result]:
    results = []
    for order in orders:
        result = validate_and_process(order)  # <-- hot line?
        results.append(result)
    return results
```

### SQL: EXPLAIN ANALYZE
```sql
EXPLAIN ANALYZE
SELECT u.id, u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2025-01-01'
GROUP BY u.id, u.name
ORDER BY order_count DESC
LIMIT 20;

-- Look for: Seq Scan (missing index), Nested Loop (N+1), Sort (large dataset)
```

## Common Bottleneck Patterns

### N+1 Query
```python
# BAD: N+1 — one query per user
users = db.query("SELECT * FROM users LIMIT 100")
for user in users:
    orders = db.query("SELECT * FROM orders WHERE user_id = %s", [user.id])

# GOOD: Eager load in one query
users_with_orders = db.query("""
    SELECT u.*, json_agg(o.*) as orders
    FROM users u
    LEFT JOIN orders o ON o.user_id = u.id
    GROUP BY u.id
    LIMIT 100
""")
```

### Missing index
```sql
-- Before: Seq Scan on 10M rows (2.3s)
-- Fix: Add index on the filtered column
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created_at ON orders(created_at);
-- After: Index Scan (4ms)
```

### Unbounded memory allocation
```python
# BAD: Loads entire table into memory
all_rows = db.query("SELECT * FROM events")  # 10M rows → OOM

# GOOD: Stream with cursor/batches
def stream_events(batch_size: int = 1000):
    offset = 0
    while True:
        batch = db.query(
            "SELECT * FROM events ORDER BY id LIMIT %s OFFSET %s",
            [batch_size, offset]
        )
        if not batch:
            break
        yield from batch
        offset += batch_size
```

### Missing cache layer
```python
import functools
import hashlib
import json
import redis

cache = redis.Redis()

def cached(ttl_seconds: int = 300):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{hashlib.md5(json.dumps([args, kwargs], default=str).encode()).hexdigest()}"
            cached_result = cache.get(key)
            if cached_result:
                return json.loads(cached_result)
            result = func(*args, **kwargs)
            cache.setex(key, ttl_seconds, json.dumps(result, default=str))
            return result
        return wrapper
    return decorator

@cached(ttl_seconds=600)
def get_dashboard_stats(org_id: str) -> dict:
    # Expensive aggregation query
    return db.query("SELECT ... complex aggregation ...", [org_id])
```

### Algorithm complexity
```python
# BAD: O(n²) — nested loop for deduplication
def dedupe_slow(items: list) -> list:
    result = []
    for item in items:
        if item not in result:  # O(n) lookup each time
            result.append(item)
    return result

# GOOD: O(n) — set-based
def dedupe_fast(items: list) -> list:
    seen = set()
    result = []
    for item in items:
        if item not in seen:  # O(1) lookup
            seen.add(item)
            result.append(item)
    return result
```

## Performance Checklist
- [ ] **Baseline measured** — latency, throughput, or memory usage recorded before changes.
- [ ] **Profiler used** — not guessing, actual data on where time is spent.
- [ ] **Bottleneck identified** — single hot spot, not scattered micro-optimizations.
- [ ] **Fix applied** — smallest change that addresses the bottleneck.
- [ ] **After measured** — same benchmark, quantified improvement (e.g., "p99 from 800ms → 45ms").
- [ ] **No regressions** — all tests still pass, no new bugs introduced.
- [ ] **Documented** — before/after metrics in task outcome and reflection log.

## Eval Method
- **Metric:** Measurable speedup on a benchmark task.
- **Test:** Given a slow code sample with a known bottleneck, does the agent identify the correct bottleneck, apply an appropriate fix, and achieve measurable improvement?
- **Threshold:** ≥ 2x speedup on the benchmark, with all tests still passing.
