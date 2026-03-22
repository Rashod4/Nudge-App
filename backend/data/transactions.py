"""
Mock transaction dataset for Nudge financial coaching demo.

47 realistic transactions spanning 3 weeks (2026-03-01 to 2026-03-21).
The data tells a story: escalating takeout spending, a possibly unused
subscription, and normal bills/income.
"""

TRANSACTIONS: list[dict] = [
    # === INCOME ===
    {"id": 1,  "date": "2026-03-06", "raw_description": "ACME CORP PAYROLL DIR DEP", "amount": 3200.00, "type": "credit"},
    {"id": 2,  "date": "2026-03-20", "raw_description": "ACME CORP PAYROLL DIR DEP", "amount": 3200.00, "type": "credit"},

    # === RENT ===
    {"id": 3,  "date": "2026-03-01", "raw_description": "ZELLE TO LANDLORD J.MARTINEZ", "amount": -1400.00, "type": "debit"},

    # === UTILITIES ===
    {"id": 4,  "date": "2026-03-03", "raw_description": "DUKE ENERGY AUTOPAY", "amount": -142.37, "type": "debit"},
    {"id": 5,  "date": "2026-03-05", "raw_description": "SPECTRUM INTERNET AUTOPAY", "amount": -79.99, "type": "debit"},

    # === SUBSCRIPTIONS ===
    {"id": 6,  "date": "2026-03-01", "raw_description": "SPOTIFY USA", "amount": -9.99, "type": "debit"},
    {"id": 7,  "date": "2026-03-01", "raw_description": "NETFLIX.COM", "amount": -15.49, "type": "debit"},
    {"id": 8,  "date": "2026-03-02", "raw_description": "GOLD'S GYM MONTHLY", "amount": -49.99, "type": "debit"},
    {"id": 9,  "date": "2026-03-02", "raw_description": "NYTIMES DIGITAL SUB", "amount": -12.99, "type": "debit"},

    # === WEEK 1 FOOD (Mar 1-7): 3 transactions ===
    {"id": 10, "date": "2026-03-02", "raw_description": "UBER EATS 8F7D2", "amount": -24.50, "type": "debit"},
    {"id": 11, "date": "2026-03-04", "raw_description": "MCDONALD'S #3892", "amount": -11.47, "type": "debit"},
    {"id": 12, "date": "2026-03-06", "raw_description": "CHIPOTLE ONLINE 4A91", "amount": -14.25, "type": "debit"},

    # === WEEK 2 FOOD (Mar 8-14): 5 transactions ===
    {"id": 13, "date": "2026-03-08", "raw_description": "DOORDASH*THAI PALACE", "amount": -32.80, "type": "debit"},
    {"id": 14, "date": "2026-03-09", "raw_description": "UBER EATS A3B91", "amount": -27.15, "type": "debit"},
    {"id": 15, "date": "2026-03-10", "raw_description": "MCDONALD'S #14923", "amount": -9.87, "type": "debit"},
    {"id": 16, "date": "2026-03-12", "raw_description": "STARBUCKS STORE 7821", "amount": -6.45, "type": "debit"},
    {"id": 17, "date": "2026-03-13", "raw_description": "CHICK-FIL-A #02918", "amount": -12.63, "type": "debit"},

    # === WEEK 3 FOOD (Mar 15-21): 7 transactions — escalation! ===
    {"id": 18, "date": "2026-03-15", "raw_description": "UBER EATS 2C4F8", "amount": -29.90, "type": "debit"},
    {"id": 19, "date": "2026-03-16", "raw_description": "DOORDASH*CHIPOTLE", "amount": -18.45, "type": "debit"},
    {"id": 20, "date": "2026-03-17", "raw_description": "GRUBHUB SUSHI PALACE", "amount": -41.20, "type": "debit"},
    {"id": 21, "date": "2026-03-18", "raw_description": "MCDONALD'S #3892", "amount": -13.28, "type": "debit"},
    {"id": 22, "date": "2026-03-19", "raw_description": "UBER EATS 9D1E3", "amount": -22.75, "type": "debit"},
    {"id": 23, "date": "2026-03-20", "raw_description": "DOORDASH*PANERA", "amount": -16.30, "type": "debit"},
    {"id": 24, "date": "2026-03-21", "raw_description": "STARBUCKS STORE 3102", "amount": -7.85, "type": "debit"},

    # === TRANSPORTATION ===
    {"id": 25, "date": "2026-03-03", "raw_description": "SHELL OIL 04728", "amount": -48.52, "type": "debit"},
    {"id": 26, "date": "2026-03-10", "raw_description": "UBER TRIP 3F29A", "amount": -18.40, "type": "debit"},
    {"id": 27, "date": "2026-03-14", "raw_description": "METRO TRANSIT PASS", "amount": -25.00, "type": "debit"},
    {"id": 28, "date": "2026-03-19", "raw_description": "SHELL OIL 04728", "amount": -52.10, "type": "debit"},

    # === SHOPPING ===
    {"id": 29, "date": "2026-03-04", "raw_description": "AMZN MKTPLACE 3A2K", "amount": -34.99, "type": "debit"},
    {"id": 30, "date": "2026-03-09", "raw_description": "TARGET 00012847", "amount": -67.23, "type": "debit"},
    {"id": 31, "date": "2026-03-15", "raw_description": "AMZN MKTPLACE 7F3B", "amount": -22.49, "type": "debit"},
    {"id": 32, "date": "2026-03-18", "raw_description": "BEST BUY #0947", "amount": -89.99, "type": "debit"},

    # === TRANSFERS / AMBIGUOUS ===
    {"id": 33, "date": "2026-03-02", "raw_description": "VENMO *PAYMENT RECEIVED", "amount": 50.00, "type": "credit"},
    {"id": 34, "date": "2026-03-07", "raw_description": "VENMO *PAYMENT SENT", "amount": -35.00, "type": "debit"},
    {"id": 35, "date": "2026-03-11", "raw_description": "ATM WITHDRAWAL #4421", "amount": -60.00, "type": "debit"},
    {"id": 36, "date": "2026-03-16", "raw_description": "VENMO *PAYMENT SENT", "amount": -25.00, "type": "debit"},
    {"id": 37, "date": "2026-03-19", "raw_description": "ATM WITHDRAWAL #5537", "amount": -40.00, "type": "debit"},

    # === ENTERTAINMENT ===
    {"id": 38, "date": "2026-03-07", "raw_description": "AMC THEATRE #1204", "amount": -16.50, "type": "debit"},
    {"id": 39, "date": "2026-03-14", "raw_description": "STEAM PURCHASE", "amount": -29.99, "type": "debit"},

    # === MORE SHOPPING / MISC ===
    {"id": 40, "date": "2026-03-05", "raw_description": "WALGREENS #9182", "amount": -18.43, "type": "debit"},
    {"id": 41, "date": "2026-03-08", "raw_description": "COSTCO WHSE #0482", "amount": -127.84, "type": "debit"},
    {"id": 42, "date": "2026-03-12", "raw_description": "TARGET 00012847", "amount": -43.17, "type": "debit"},
    {"id": 43, "date": "2026-03-17", "raw_description": "AMZN MKTPLACE 1K9Z", "amount": -15.99, "type": "debit"},

    # === ADDITIONAL TRANSACTIONS FOR REALISM ===
    {"id": 44, "date": "2026-03-06", "raw_description": "PARKING METER DT-3892", "amount": -4.00, "type": "debit"},
    {"id": 45, "date": "2026-03-11", "raw_description": "VENMO *PAYMENT RECEIVED", "amount": 30.00, "type": "credit"},
    {"id": 46, "date": "2026-03-13", "raw_description": "COSTCO GAS #0482", "amount": -38.71, "type": "debit"},
    {"id": 47, "date": "2026-03-20", "raw_description": "WALGREENS #9182", "amount": -12.56, "type": "debit"},
]
