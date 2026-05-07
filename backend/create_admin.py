from auth.auth_crud import create_user, get_user_by_username
from auth.security import hash_password

USERNAME = "admin"
PASSWORD = "admin"  

if __name__ == "__main__":
    if get_user_by_username(USERNAME):
        print(f"User '{USERNAME}' already exists, skipping.")
    else:
        create_user(USERNAME, hash_password(PASSWORD))
        print(f"Admin user '{USERNAME}' created successfully.")