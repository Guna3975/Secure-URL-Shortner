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
├── app/                # Backend (FastAPI application)
│   ├── core/           # Security, hashing, JWT, config
│   ├── database/       # DB connection, models, queries
│   ├── routes/         # API endpoints
│   ├── services/       # Business logic layer
│   ├── middleware/     # Logging & rate limiting
│   └── main.py         # FastAPI entry point
│
├── frontend/           # Static UI pages
├── sql/                # DB schema & migrations
├── redis/              # Redis configuration
├── tests/              # Unit tests
└── run.py              # App runner
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
psql -U postgres -f sql/schema.sql
psql -U postgres -f sql/seed.sql
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