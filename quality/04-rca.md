# Root-Cause Analysis (RCA) & Guard Test: Defect DEF-001

## 1. Defect Summary
- **ID:** DEF-001
- **Title:** Concurrent checkout allows over-reservation of last item (Phantom Stock Race Condition)
- **Severity:** P1 (Critical — Blocker for Italy pilot)
- **Observed Behavior:** When two users simultaneously submit reservations for the last remaining unit of an item, both succeed, and inventory decrements to `-1`.

---

## 2. Root-Cause Hypotheses Tracing
- **Hypothesis A (UI Validation Lag):** The frontend is not disabling the checkout button quickly enough upon click. *(Ruled out: API logs show both requests hit the backend controller simultaneously within the same millisecond window).*
- **Hypothesis B (Database Missing Lock):** The inventory reservation query executes a non-atomic `SELECT` followed by an `UPDATE` without a pessimistic row-level lock or optimistic locking version check. *(Confirmed: Database transaction logs show no isolation barrier or serializable transaction boundary around inventory decrement).*
- **Hypothesis C (Cache Invalidation):** Redis cache is returning stale inventory counts to application instances. *(Ruled out: Cache TTL is disabled for checkout write paths, direct DB hit was used).*

---

## 3. Precise Root-Cause Statement
> *The condition that made this bug possible was the lack of database-level atomic locking or optimistic concurrency control on the inventory decrement transaction, allowing concurrent API requests to read the same positive stock level and pass validation simultaneously.*

---

## 4. Guard Test
- **Test ID:** TC-GUARD-01
- **Title:** Atomic inventory decrement concurrency guard test under high contention
- **Type:** Guard Test / Regression
- **Surface Exercised:** Web Inventory & Reservation (API concurrency level)
- **Priority:** P1
- **Preconditions:** SKU `MER-SHIRT-01` inventory balance is seeded to exactly `1` in database.
- **Steps:**
  1. Trigger two simultaneous HTTP POST requests to `/api/v1/checkout/reserve` containing identical SKU payloads using an automated test harness.
  2. Execute requests concurrently within a 10ms window.
  3. Inspect HTTP response codes and database state post-execution.
- **Expected Outcome:** Exactly one request receives HTTP 200 OK (Reservation Confirmed); the second request receives HTTP 409 Conflict (Out of Stock / Inventory Locked). Database stock equals `0`, and inventory count never drops below zero.

---

## 5. Recommended Fix
Implement database-level pessimistic locking (`SELECT ... FOR UPDATE`) or an optimistic concurrency token on the inventory table during checkout reservation to ensure that stock decrements are processed serially per SKU.