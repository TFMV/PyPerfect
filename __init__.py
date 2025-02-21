"""PyPerfect package initialization.""" 

from .app import create_app
from .db import init_db

__all__ = ["create_app", "init_db"]

# Add this line to the end of the file
__version__ = "0.1.0"
