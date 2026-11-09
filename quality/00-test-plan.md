---
case: Meridian Retail Group — Click & Collect
feature: Omnichannel Click & Collect Cross-Channel Flow (Phase 1)
date: 2026-11-09
author: Maksym Hodik
---

# Test Strategy & Plan: Click & Collect (Phase 1)

## 1. In-Scope Surfaces
- **Web Inventory Check & Reservation:** Real-time stock visibility and cart reservation holding across web and mobile browsers.
- **Store Pickup Slot Selection:** Checkout slot booking mechanism and slot availability sync.
- **Pickup Confirmation & Notification:** Order state transition from `Ready for Pickup` to `Picked Up` via SMS/Email trigger.
- **Store Associate Scan-to-Verify:** Mobile/POS terminal scanning of customer QR confirmation codes upon arrival.

## 2. Out-of-Scope (Explicit Exclusions)
- **SAP ECC Inventory Ground-Truth Correctness:** The underlying ERP supply chain accuracy is owned by the Finance/Supply Chain team and covered by their independent nightly reconciliations.
- **Third-Party Payment Gateway Internal Processing:** We test API integration request/response handling, but not internal credit card processing infrastructure (handled by Stripe/Adyen).

## 3. Top-3 Risks (Identified via AI & Risk Analysis)
1. **Phantom Stock Cancellation Spike (Business Impact: High):**
   - *Failure:* Inventory shows available online, but physical shelf stock is zero due to store sync lag.
   - *User Impact:* Customer arrives at the store, but order cannot be fulfilled, causing frustration.
   - *Mitigation/Test Focus:* Test real-time inventory decrement during checkout and concurrent orders.
2. **Notification Delay on Ready-for-Pickup (User Impact: Medium):**
   - *Failure:* SMS/Email notification is delayed by >30 minutes after store packing.
   - *User Impact:* Customers show up before store staff finishes picking, or arrive too late.
   - *Mitigation/Test Focus:* Validate webhook response times and notification queue processing under peak load.
3. **QR Scan-to-Verify Failure at POS (Operational Impact: High):**
   - *Failure:* Store associate scanner fails to resolve customer QR code during pickup.
   - *User Impact:* Long queues at the pickup counter and manual order lookup required.
   - *Mitigation/Test Focus:* Test edge cases with malformed or expired QR tokens.

## 4. Entry Criteria
- Phase 1 build successfully deployed to the QA integration environment.
- SAP sandbox seeded with realistic inventory deltas and active store location profiles.
- Automated test data harness initialized with test user accounts.

## 5. Exit Criteria
- **Test Pass Rate:** $\ge 95\%$ on all critical Click & Collect user paths.
- **Defect Status:** Zero Critical or High unresolved defects; all Medium/Low defects documented with workarounds.
- **Phantom-Stock Rate:** Zero unhandled phantom-stock cancellation errors in the priority-1 test suite.
- **Sign-off:** Formal approval from QA Lead and Product Owner.