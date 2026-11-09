# Test Cases Suite: Click & Collect (Phase 1)
*Derived from `00-test-plan.md` in-scope surfaces.*

## Reference In-Scope Surfaces
1. Web Inventory Check & Reservation
2. Store Pickup Slot Selection
3. Pickup Confirmation & Notification
4. Store Associate Scan-to-Verify

---

## Seed Test Cases (Written by Hand)
1. **Seed 1 (Inventory):** Customer reserves an item online with sufficient stock in the Milan flagship store; stock is successfully decremented in real-time.
2. **Seed 2 (Slot):** Customer selects a valid pickup slot during store operating hours and completes checkout.
3. **Seed 3 (Notification):** When store staff marks an order as packed, an automated email/SMS containing the QR verification code is dispatched to the customer.
4. **Seed 4 (Associate Scan):** Store associate scans the customer's QR code at the POS upon arrival, successfully transitioning the order status to `Picked Up`.
5. **Seed 5 (Negative Inventory):** Customer attempts to reserve an item whose physical stock dropped to zero during checkout due to a concurrent in-store purchase.

---

## Expanded Risk-Driven Test Suite (15 Test Cases)

| ID | Title / Scenario | Type | Surface Exercised | Priority | Expected Outcome |
|---|---|---|---|---|---|
| TC-INV-01 | Standard reservation in Milan flagship | Happy-Path | Web Inventory & Reservation | P1 | Stock decremented by 1, hold secured for 24h. |
| TC-INV-02 | Cross-region inventory lookup (Rome vs Milan) | Edge-Case | Web Inventory & Reservation | P2 | Correct local store stock displayed based on IP/postal code. |
| TC-INV-03 | Concurrent checkout race condition for last item | Negative | Web Inventory & Reservation | P1 | Second user blocked at checkout with out-of-stock notice. |
| TC-INV-04 | Reservation attempt on discontinued SKU | Negative | Web Inventory & Reservation | P3 | Checkout rejects SKU with appropriate error message. |
| TC-SLT-01 | Standard pickup slot selection during business hours | Happy-Path | Store Pickup Slot Selection | P1 | Slot successfully reserved and linked to order. |
| TC-SLT-02 | Slot selection outside store operating hours (Sunday night) | Edge-Case | Store Pickup Slot Selection | P2 | System prompts user to select next available business hours slot. |
| TC-SLT-03 | Selecting a fully booked pickup slot via API race | Negative | Store Pickup Slot Selection | P2 | API returns slot-unavailable error, forces re-selection. |
| TC-NOT-01 | QR code notification sent upon `Ready for Pickup` status | Happy-Path | Pickup Confirmation & Notification | P1 | Email and SMS dispatched within 60 seconds with valid QR link. |
| TC-NOT-02 | Notification retry after transient webhook failure | Edge-Case | Pickup Confirmation & Notification | P3 | Message queued and successfully delivered after second attempt. |
| TC-NOT-03 | Notification trigger with malformed customer phone number | Negative | Pickup Confirmation & Notification | P3 | SMS fails gracefully, email sent successfully, error logged. |
| TC-SCN-01 | Successful QR scan at store POS by associate | Happy-Path | Store Associate Scan-to-Verify | P1 | Order status updates instantly from `Ready` to `Picked Up`. |
| TC-SCN-02 | Scanning an expired QR code (>7 days past due) | Edge-Case | Store Associate Scan-to-Verify | P2 | POS terminal displays expiration warning, prompts manual manager override. |
| TC-SCN-03 | Scanning a QR code belonging to a cancelled order | Negative | Store Associate Scan-to-Verify | P1 | POS rejects scan, displays "Order Cancelled" alert. |
| TC-SCN-04 | Scanning an already picked-up order (duplicate scan) | Negative | Store Associate Scan-to-Verify | P2 | POS warns "Order already fulfilled", prevents double pickup. |
| TC-INV-05 | Zero inventory edge case during partial multi-item pickup | Negative | Web Inventory & Reservation | P2 | System handles partial fulfillment cleanly without crashing inventory sync. |