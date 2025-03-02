# app/app.py
import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import pugsql
from nanoid import generate
from typing import Optional
from pathlib import Path

# Initialize FastAPI app
app = FastAPI(title="PyPerfect Bookmarks API", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the base directory and construct paths
BASE_DIR = Path(__file__).resolve().parent.parent
QUERIES_DIR = BASE_DIR / "db" / "queries"

# Ensure the queries directory exists
os.makedirs(QUERIES_DIR, exist_ok=True)

# Load database queries
queries = pugsql.module(str(QUERIES_DIR))

# SQLite connection string must have 3 slashes for absolute path: sqlite:///path/to/db
db_path = BASE_DIR / "db" / "database.sqlite3"
os.makedirs(db_path.parent, exist_ok=True)
db_url = os.getenv("DATABASE_URL", f"sqlite:///{db_path}")
queries.connect(db_url)


# Mock auth for development (replace with PropelAuth in production)
class User:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def get_org(self, org_id: str):
        # Mock implementation - in production, use PropelAuth
        return UserOrgInfo(org_id)


class UserOrgInfo:
    def __init__(self, org_id: str):
        self.org_id = org_id

    def is_at_least_role(self, role: str) -> bool:
        # Mock implementation - in production, use PropelAuth
        return True


class MockAuth:
    def require_user(self):
        # Mock implementation - in production, use PropelAuth
        async def _require_user():
            return User("test-user-id")

        return _require_user


# Initialize auth (mock for development)
auth = MockAuth()


# Models
class Bookmark(BaseModel):
    link: HttpUrl


# Dependencies
# First create a dependency for the current user
current_user_dependency = Depends(auth.require_user)


def require_org_access(minimum_required_role: str | None = None):
    """Dependency factory to check organization access and roles."""

    async def _require_org_access(
        org_id: str, current_user: User = current_user_dependency
    ):
        user_info_in_org = current_user.get_org(org_id)
        if user_info_in_org is None:
            raise HTTPException(status_code=401, detail="Not a member of this org")

        if minimum_required_role is not None and not user_info_in_org.is_at_least_role(
            minimum_required_role
        ):
            raise HTTPException(status_code=403, detail="Insufficient role in org")

        return (current_user, user_info_in_org)

    return _require_org_access


# Routes
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "OK"}


@app.get("/{org_id}/{bookmark_id}")
async def redirect_to_bookmark(
    bookmark_id: str,
    org_id: str,
    user_and_org: tuple[User, UserOrgInfo] = Depends(require_org_access()),
):
    """Get a bookmark by ID within an organization."""
    link = queries.get_link(org_id=org_id, bookmark_id=bookmark_id)
    if link is None:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return {"link": link}


@app.post("/{org_id}/bookmark")
async def create_bookmark(
    bookmark: Bookmark,
    org_id: str,
    user_and_org: tuple[User, UserOrgInfo] = Depends(require_org_access()),
):
    """Create a new bookmark within an organization."""
    user, _ = user_and_org
    bookmark_id = generate()
    queries.save_bookmark(
        bookmark_id=bookmark_id,
        link=str(bookmark.link),
        org_id=org_id,
        user_id=user.user_id,
    )
    return {"bookmark_id": bookmark_id}


@app.delete("/{org_id}/bookmark/{bookmark_id}")
async def delete_bookmark(
    org_id: str,
    bookmark_id: str,
    user_and_org: tuple[User, UserOrgInfo] = Depends(require_org_access()),
):
    """Delete a bookmark by ID within an organization."""
    user, user_info_in_org = user_and_org

    affected_rows = 0
    if user_info_in_org.is_at_least_role("Admin"):
        # Admins can delete any bookmark in their org
        affected_rows = queries.delete_bookmark(org_id=org_id, bookmark_id=bookmark_id)
    else:
        # Regular users can only delete their own bookmarks
        affected_rows = queries.delete_my_bookmark(
            org_id=org_id, user_id=user.user_id, bookmark_id=bookmark_id
        )

    if affected_rows > 0:
        return {"status": "deleted"}
    else:
        raise HTTPException(status_code=404, detail="Bookmark not found")


@app.get("/{org_id}/bookmarks")
async def list_bookmarks(
    org_id: str, user_and_org: tuple[User, UserOrgInfo] = Depends(require_org_access())
):
    """List all bookmarks within an organization."""
    bookmarks = queries.list_bookmarks(org_id=org_id)
    return {"bookmarks": bookmarks}


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to PyPerfect Bookmarks API"}
