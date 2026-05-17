"""
Create an admin user for the EdgeSafe dashboard.
Run this once any time you need to add another admin
Usage:
    python create_admin.py
The script is idempotent: if the username already exists it skips
creation. Passwords are bcrypt-hashed before being stored.
"""

import getpass
import sys

from backend.auth.auth_crud import create_user, get_user_by_username
from backend.auth.security import hash_password

MIN_PASSWORD_LENGTH = 8


def main() -> int:
    username = input("Username: ").strip()
    if not username:
        print("ERROR: Username cannot be empty.", file=sys.stderr)
        return 1

    if get_user_by_username(username):
        print(f"User '{username}' already exists, skipping.")
        return 0

    password = getpass.getpass("Password: ")
    if len(password) < MIN_PASSWORD_LENGTH:
        print(
            f"ERROR: Password must be at least {MIN_PASSWORD_LENGTH} characters.",
            file=sys.stderr,
        )
        return 1

    confirm = getpass.getpass("Confirm password: ")
    if password != confirm:
        print("ERROR: Passwords do not match.", file=sys.stderr)
        return 1

    create_user(username, hash_password(password))
    print(f"Admin user '{username}' created successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
