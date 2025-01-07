import json


def read_secrets(filename=".././secrets.json"):
    """Reads secrets from a JSON file.

    Args:
        filename: The name of the JSON file containing the secrets.
                  Defaults to 'secrets.json'.

    Returns:
        A dictionary containing the secrets loaded from the file.
        Returns an empty dictionary if the file cannot be read.
    """
    try:
        with open(filename, "r") as f:
            return json.load(f)

    except FileNotFoundError:
        print(f"Warning: Secrets file '{filename}' not found.")
        return {}


# Example usage:
if __name__ == "__main__":
    secrets = read_secrets()[0]
    api_key = secrets.get("key")
    database_password = secrets.get("database_password")
    print(api_key, database_password)

    # Use the secrets as needed
