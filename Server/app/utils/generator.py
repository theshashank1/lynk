import random
import uuid


def generate_unique_id(length: int = 4) -> str:
    """
    Generate a unique ID of specified length by selecting a random sequence
    from a hyphen-less UUID.
    """
    # Generate UUID and remove hyphens to ensure consistent length
    uuid_str = str(uuid.uuid4()).replace("-", "")

    # Validate requested length
    if not 1 <= length <= len(uuid_str):
        raise ValueError(f"Length must be between 1 and {len(uuid_str)}")

    # Determine the random starting index for the sequence
    max_start = len(uuid_str) - length
    start = random.randint(0, max_start)

    # Extract and return the uppercase random sequence
    return uuid_str[start : start + length]


def generate_username(email: str, unique_id_length: int = 4) -> str:
    """
    Generate a username in the format: email_prefix_[unique_id]

    Args:
        email (str): User's email address
        unique_id_length (int): Length of the unique ID (default: 4)

    Returns:
        str: Username in format email_prefix_[unique_id]
    """
    # Extract the prefix of the email (before the @ symbol)
    email_prefix = email.split("@")[0]

    # Sanitize the email prefix to ensure it's a valid username component
    email_prefix = email_prefix.replace(".", "_").replace("-", "_")

    # Generate unique ID
    unique_id = generate_unique_id(unique_id_length).upper()

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
