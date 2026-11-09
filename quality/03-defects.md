# Defect Log: Click & Collect (Phase 1 Execution)
*Executed against Meridian QA environment using Playwright AI browser agent, referencing `01-test-cases.md` and `02-test-data.json`.*

## Summary of Executed Priority Tests
1. **TC-INV-01** (Standard reservation in Milan flagship) — **PASS**
2. **TC-INV-03** (Concurrent checkout race condition for last item) — **FAIL (Defect #1)**
3. **TC-SLT-01** (Standard pickup slot selection during business hours) — **PASS**
4. **TC-SCN-03** (Scanning a QR code belonging to a cancelled order) — **FAIL (Defect #2)**

---

## Logged Defects

### Defect 1: Concurrent checkout allows over-reservation of last item (Phantom Stock Race Condition)
- **ID:** DEF-001
- **Severity:** P1 (Critical — Blocker for Italy pilot)
- **Priority:** P1 (Fix immediately before release)
- **Related Test Case:** TC-INV-03
- **Test Data Record:** `CUST_IT_99218` & `CUST_CONC_10` (simultaneous requests)
- **Steps to Reproduce:**
  1. Seed inventory of SKU `MER-SHIRT-01` to exactly `1` unit in Milan Flagship store.
  2. Launch two browser sessions simultaneously (User A and User B).
  3. Both users add the SKU to cart and proceed to checkout at the exact same millisecond.
  4. Both users click "Confirm Click & Collect Reservation".
- **Expected Result:** User A secures the reservation; User B is blocked at checkout with an "Out of stock" notification and cart update.
- **Actual Result:** Both users receive a "Reservation Confirmed" success screen. Stock in database decrements to `-1`.
- **AI-Surface Metadata:** Playwright MCP step trace confirmed zero millisecond database lock during inventory check phase. Prompt context: concurrent API load simulation.

---

### Defect 2: Store POS terminal accepts and validates cancelled order QR codes
- **ID:** DEF-002
- **Severity:** P2 (High — Operational impact on store associates)
- **Priority:** P1 (Fix before store associate training)
- **Related Test Case:** TC-SCN-03
- **Test Data Record:** `CUST_DE_EDGE_02` (Order `ORD-2026-9902` marked as `CANCELLED`)
- **Steps to Reproduce:**
  1. Log into Store Associate POS terminal interface.
  2. Scan the QR code associated with an order that was cancelled by customer 2 hours prior.
  3. Observe terminal behavior.
- **Expected Result:** POS rejects the scan immediately, displaying an alert: *"Error: Order Cancelled by Customer"*, preventing fulfillment.
- **Actual Result:** POS terminal displays order details and allows the associate to click "Complete Pickup", resulting in an orphaned inventory mismatch.
- **AI-Surface Metadata:** Playwright MCP agent scan simulation. Root cause identified as stale cache in POS local state lookup service.

---

## Unverified / Flaky Observations (Logs & Stories)
- **OBS-01 (Transient Notification Delay):** During load testing of `TC-NOT-01`, 1 out of 50 confirmation SMS notifications took 92 seconds to dispatch (above the 60s threshold). Marked as flaky due to sandbox SMS gateway throttling; monitored for production telemetry.