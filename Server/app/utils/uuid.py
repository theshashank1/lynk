import random
from datetime import datetime

import pytz


def generate_unique_id(length: int = 4) -> str:
    """
    Generate a unique ID of specified length using uppercase letters and numbers
    """
    # Define the character set (excluding similar looking characters)
    chars = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
    return "".join(random.choices(chars, k=length))


# Assign the function call to a module-level variable
DEFAULT_TIMESTAMP = datetime(2025, 1, 13, 18, 45, 6, tzinfo=pytz.UTC)


def generate_username(email: str, timestamp: datetime = DEFAULT_TIMESTAMP) -> str:
    """
    Generate a username in the format: email_prefix_[unique_id]

    Args:
        email (str): User's email address
        timestamp (datetime): Timestamp for ID generation (default: DEFAULT_TIMESTAMP)

    Returns:
        str: Username in format email_prefix_[unique_id]
    """
    # Extract the prefix of the email (before the @ symbol)
    email_prefix = email.split("@")[0]

    # Generate unique ID
    unique_id = generate_unique_id()

    # Combine email prefix and unique ID
    return f"{email_prefix}_{unique_id}"


if __name__ == "__main__":
    # Test data
    email = "theshashank1@example.com"

    # Generate username
    username = generate_username(email)
    print(f"Generated username: {username}")

    # Generate multiple examples to show uniqueness
    print("\nMultiple examples:")
    test_cases = [
        "theshashank1@example.com",
        "john.doe@example.com",
        "alice.smith@example.com",
        "bob@example.com",
    ]

    for test_email in test_cases:
        username = generate_username(test_email)
        print(f"Email: {test_email:<30} | Username: {username}")
