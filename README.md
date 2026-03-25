# Secure URL Shortener

## Description
    A WebApp to shorten a URL given by the User securely by checking whether that given link is safe or not (having malware).

## Team Members
- R. Gunaseelan
- M. Jayasri
- K. Jayasuriya

## Features
- URL shortening with unique hash generation
- Malicious / unsafe URL detection before shortening
- User authentication (JWT-based login & registration)
- Click analytics & usage statistics
- Redis-based rate limiting
- Admin dashboard for monitoring URLs & users
- Fast redirection service
- Automated backend tests

## Project Directory
``` 
secure-url-shortener
│
├── app/                     # Main backend application
│   |
│   ├── config.py            # Global configuration settings
│   |
│   ├── core/                # Core security and utility modules
│   │   ├── config.py        # Core configuration values
│   │   ├── exceptions.py    # Custom exception handling
│   │   ├── generator.py     # Short URL code generator
│   │   ├── hashing.py       # Password hashing utilities
│   │   └── jwt_handler.py   # JWT token generation & validation
│   |
│   ├── database/            # Database interaction layer
│   │   ├── connection.py    # Oracle DB connection using SQL*Plus
│   │   ├── models.py        # Data models
│   │   └── queries.py       # SQL queries used by services
│   |
│   ├── middleware/          # Request middleware components
│   │   ├── logging.py       # Request logging middleware
│   │   └── rate_limit.py    # API rate limiting using Redis
│   |
│   ├── routes/              # API endpoints
│   │   ├── admin_routes.py  # Admin management APIs
│   │   ├── auth_routes.py   # Login & registration endpoints
│   │   ├── redirect_routes.py # URL redirection endpoint
│   │   └── url_routes.py    # URL shortening APIs
│   |
│   ├── schemas/             # Request & response validation schemas
│   │   ├── admin_schema.py
│   │   ├── auth_schema.py
│   │   └── url_schema.py
│   |
│   ├── services/            # Business logic layer
│   │   ├── analytics_service.py   # Click tracking & statistics
│   │   ├── auth_service.py        # Authentication logic
│   │   ├── limiter_service.py     # Rate limit logic
│   │   ├── security_service.py    # URL safety checking
│   │   ├── url_service.py         # URL shortening & retrieval
│   │   └── validator_service.py   # URL validation utilities
│   |
│   ├── dependencies.py      # FastAPI dependency injection
│   └── main.py              # FastAPI application entry point
│  
├── frontend/                # Static frontend pages
│   ├── index.html
│   ├── start.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── features.html
│
├── redis/                   # Redis configuration for caching and rate limiting
│   └── redis_config.md
│
├── sql/                     # Database schema and migrations
│   ├── schema.sql           # Initial database schema
│   ├── seed.sql             # Sample data
│   └── migrations/          # Additional migration scripts
│       ├── 001_create_users_and_urls.sql
│       ├── click_table_log.sql
│       └── url_storing_table.sql
│
├── tests/                   # Unit and integration tests
│   ├── test_auth.py
│   ├── test_limits.py
│   └── test_urls.py
│
├── requirements.txt         # Python dependencies
├── run.py                   # Application runner script
└── README.md                # Project documentation
```
## Getting Started
1. Clone the repository
``` bash
git clone https://github.com/your-username/secure-url-shortener.git

cd secure-url-shortener
```

2. Create virtual environment
``` bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
3. Install dependencies
``` bash
pip install -r requirements.txt
```
4. Setup database
``` bash
sqlplus username/password

@sql/schema.sql
@sql/seed.sql
```
5. Start Redis
``` bash
redis-server
```
6. Run application
``` bash
python run.py
```
*App will start at:*

http://localhost:8000
## Tech Stack
### Backend
- FastAPI
- Python 3.13
- PostgreSQL / SQLite
- Redis
- JWT Authentication
### Frontend
- HTML / CSS
- Vanilla JS
### Security
- URL validation & malware check
- Hash-based short codes
- Rate limiting
- Auth tokens

## Security Workflow
1. User submits URL
2. System validates format
3. Malware / blacklist check
4. Unique hash generated
5. URL stored in database
6. Short link returned

## License
    This project is developed for academic purposes.
## Future Improvements
- Real-time threat intelligence API integration
- QR code generation
- Custom short aliases
- Expiring URLs
- Public analytics dashboard