from enum import Enum


class Category(str, Enum):
    FOOD = "food"
    RENT = "rent"
    UTILITIES = "utilities"
    ENTERTAINMENT = "entertainment"
    TRANSPORTATION = "transportation"
    SHOPPING = "shopping"
    SUBSCRIPTION = "subscription"
    INCOME = "income"
    TRANSFER = "transfer"
    UNCATEGORIZED = "uncategorized"


# Keyword-based merchant → category mapping for deterministic categorization.
# Keys are lowercased substrings matched against raw_description.
CATEGORY_KEYWORDS: dict[str, Category] = {
    # Food / Takeout
    "uber eats": Category.FOOD,
    "doordash": Category.FOOD,
    "grubhub": Category.FOOD,
    "mcdonald": Category.FOOD,
    "chipotle": Category.FOOD,
    "starbucks": Category.FOOD,
    "chick-fil-a": Category.FOOD,
    "panera": Category.FOOD,
    "subway": Category.FOOD,
    "taco bell": Category.FOOD,
    "wendy": Category.FOOD,
    "pizza": Category.FOOD,
    # Rent
    "landlord": Category.RENT,
    "rent": Category.RENT,
    "zelle to landlord": Category.RENT,
    # Utilities
    "duke energy": Category.UTILITIES,
    "spectrum": Category.UTILITIES,
    "comcast": Category.UTILITIES,
    "water utility": Category.UTILITIES,
    "electric": Category.UTILITIES,
    "internet": Category.UTILITIES,
    # Subscriptions
    "spotify": Category.SUBSCRIPTION,
    "netflix": Category.SUBSCRIPTION,
    "hulu": Category.SUBSCRIPTION,
    "nytimes": Category.SUBSCRIPTION,
    "gym": Category.SUBSCRIPTION,
    "gold's gym": Category.SUBSCRIPTION,
    "apple.com/bill": Category.SUBSCRIPTION,
    # Entertainment
    "amc theatre": Category.ENTERTAINMENT,
    "cinema": Category.ENTERTAINMENT,
    "steam": Category.ENTERTAINMENT,
    # Transportation
    "uber trip": Category.TRANSPORTATION,
    "lyft": Category.TRANSPORTATION,
    "shell oil": Category.TRANSPORTATION,
    "chevron": Category.TRANSPORTATION,
    "exxon": Category.TRANSPORTATION,
    "metro transit": Category.TRANSPORTATION,
    "parking": Category.TRANSPORTATION,
    # Shopping
    "amazon": Category.SHOPPING,
    "amzn": Category.SHOPPING,
    "target": Category.SHOPPING,
    "walmart": Category.SHOPPING,
    "best buy": Category.SHOPPING,
    "costco": Category.SHOPPING,
    # Income
    "payroll": Category.INCOME,
    "direct dep": Category.INCOME,
    "dir dep": Category.INCOME,
    # Transfers
    "venmo": Category.TRANSFER,
    "zelle": Category.TRANSFER,
    "cashapp": Category.TRANSFER,
    "atm withdrawal": Category.TRANSFER,
}
