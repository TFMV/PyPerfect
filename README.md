# PyPerfect Bookmarks API

A multi-tenant bookmark aggregator API built with FastAPI, featuring authentication, database migrations, and SQL queries.

## Features

- FastAPI framework with automatic OpenAPI documentation
- Multi-tenant architecture with organization-based access control
- Database migrations with dbmate
- SQL queries with PugSQL
- Authentication (mock implementation, ready for PropelAuth integration)
- Nanoid for generating short, unique IDs

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up the directories and database:

   ```bash
   # Create necessary directories
   python setup_dirs.py
   
   # Set up the database (if using dbmate)
   dbmate up
   ```

3. Run the server using the run script:

   ```bash
   python run.py
   ```

   Alternatively, you can use uvicorn directly:

   ```bash
   uvicorn app.app:app --reload
   ```

4. Access the API documentation at <http://localhost:8000/docs>

## Database Configuration

The application uses SQLite by default. The connection string format for SQLite is:

```bash
sqlite:///path/to/database.sqlite3
```

Note the three forward slashes - this is important for SQLAlchemy to correctly parse the URL:

- `sqlite:///` - protocol and separator
- `path/to/database.sqlite3` - absolute path to the database file

You can change the database connection in the `.env` file.

## Project Structure

```txt
PyPerfect/
├── app/
│   └── app.py           # Main FastAPI application
├── db/
│   ├── queries/         # SQL queries for PugSQL
│   │   ├── get_link.sql
│   │   ├── save_bookmark.sql
│   │   └── ...
│   └── migrations/      # Database migrations for dbmate
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
├── run.py               # Script to run the application
└── setup_dirs.py        # Script to set up directories
```

## API Endpoints

- `GET /health` - Health check endpoint
- `GET /{org_id}/{bookmark_id}` - Get a bookmark by ID
- `POST /{org_id}/bookmark` - Create a new bookmark
- `DELETE /{org_id}/bookmark/{bookmark_id}` - Delete a bookmark
- `GET /{org_id}/bookmarks` - List all bookmarks in an organization

## Production Setup

For production, you'll need to:

1. Replace the mock authentication with PropelAuth
2. Configure proper database credentials
3. Set up proper CORS settings
4. Deploy to your preferred hosting platform

## License

MIT
