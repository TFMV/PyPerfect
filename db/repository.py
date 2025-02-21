import ibis
from pydantic import BaseModel
from typing import List, Optional
from .session import db_session
from .models import User

class UserRepository:
    """Handles database interactions for the User entity."""

    def __init__(self):
        self.conn = db_session.get_connection()

    def create_user(self, user: User) -> None:
        """Insert a new user into the database."""
        self.conn.raw_sql(
            "INSERT INTO users (id, username, email, full_name, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (user.id, user.username, user.email, user.full_name, user.created_at, user.updated_at)
        )

    def get_user(self, user_id: int) -> User | None:
        """Fetch a user by ID."""
        result = self.conn.raw_sql(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        ).fetchdf()
        if result.empty:
            return None
        return User(**result.iloc[0].to_dict())

    def list_users(self) -> list[User]:
        """Retrieve all users."""
        result = self.conn.raw_sql(
            "SELECT * FROM users"
        ).fetchdf()
        return [User(**row.to_dict()) for _, row in result.iterrows()]

    def delete_user(self, user_id: int) -> None:
        """Delete a user by ID."""
        self.conn.raw_sql(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )

# Example usage
if __name__ == "__main__":
    repo = UserRepository()
    new_user = User(id=1, username="johndoe", email="johndoe@example.com", full_name="John Doe")
    repo.create_user(new_user)
    print(repo.list_users())
