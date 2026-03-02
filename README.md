 # Candidate Batch Processing System
A production-oriented backend system for ingesting, validating, and asynchronously processing candidate records in controlled batches with retry logic, reporting capabilities, and role-based access control.
Architected to reflect real-world external API integrations with resilience, observability, and concurrency safety.

## Problem Statement

Organizations often need to:
- Collect candidate data via APIs
- Validate and persist structured records
- Send records to external systems in scheduled batches
- Retry failed submissions
- Track processing attempts
- Generate operational and analytical reports
This system provides a scalable and fault-tolerant solution for that workflow.

## Architecture Overview
```bash
Client → Django REST API → PostgreSQL
                               ↓
                         Background Worker (Celery Worker (Redis Broker))
                               ↓
                        External Batch API
```
### Core Design Principles
- Clean separation of concerns
- Background task processing
- Idempotent batch execution
- Concurrency-safe record selection
- Structured error handling
- Role-based authorization
- Extensible reporting layer

## Tech Stack
| Layer            | Technology               |
| ---------------- | ------------------------ |
| Language         | Python                   |
| Framework        | Django                   |
| API Layer        | Django REST Framework    |
| Database         | PostgreSQL               |
| Auth             | JWT                      |
| Background Jobs  | Celery + Redis |
| Containerization | Docker (Planned)         |

### why Celery?
- Mature ecosystem
- Robust retry mechanisms
- Supports periodic tasks
- Scales with worker processes
- Integrates well with Django

## API Standards
- RESTful API design
- Consistent JSON response format
- Structured error responses
- Pagination support (planned for list endpoints)
- Token-based authentication using Authorization header

## Authentication & Authorization
### Authentication
- JWT-based authentication for API access
- Short-lived access tokens
- Optional refresh token mechanism
- Bearer token required for protected endpoints
```bash
Authorization: Bearer <token>
```

### Role-Based Access Control (RBAC)
Two roles are implemented:
#### ADMIN
- Full system access
- Create candidates
- Trigger batch runs
- Access reports
#### REVIEWER
- Read-only access
- Can view search and reporting endpoints
- Cannot mutate candidate or batch state
Custom user model supports role enforcement at permission level.

## Candidate Ingestion
```markdown
POST /candidates
Creates a new candidate after strict validation.
```

### Server-Side Validations
| Field       | Rule                           |
| ----------- | ------------------------------ |
| name        | Required, non-empty            |
| email       | Valid email format             |
| phoneNumber | International format supported |
| link        | Valid URL (optional)           |
| dob         | Valid date (optional)          |
### Duplicate Prevention
- Email uniqueness enforced
- Conflict response returned if duplicate detected

## Data Model
### users
- email (unique)
- password
- role (ADMIN / REVIEWER)

### candidates
- UUID primary key
- name
- email
- phone_number
- link
- dob
- status (PENDING, SUCCESS, FAILED)
- created_at

### batch_runs
Tracks each scheduled batch execution.

### candidate_attempts
Tracks each processing attempt per candidate.

## Batch Processing Strategy (Upcoming Phase)
Designed for:
- Execution every 2 hours
- Max 10 records per batch
- Retry failed records
- Skip successful records
- Prevent double-processing using:
- - Row-level locking
- - Atomic update strategy
- - Pick markers
Resilience goals:
- Safe restarts
- Retry on transient failures
- Idempotent execution

## Reporting Capabilities (Upcoming Phase)
Planned analytics endpoints include:
- Success/failure metrics
- Success rate calculation
- Retry distribution histogram
- Average attempts to success
- Top email domains by success rate
- Stuck candidate detection
Optimized using database aggregation queries.

## Concurrency & Safety
- Transactional operations
- Atomic record updates
- UUID-based identifiers
- Structured error responses
```markdown
Clear HTTP status codes:
- 400 validation
- 401 unauthenticated
- 403 unauthorized
- 404 not found
- 409 conflict
```


## Project Structure
```bash
project/
│
├── users/          # Authentication & RBAC
├── candidates/     # Candidate management
├── batch/          # Batch processing logic (planned)
├── reports/        # Reporting layer (planned)
├── core/           # Shared utilities
│
├── manage.py
└── requirements.txt
```
## Running Locally
1. Clone the repository
```bash
git clone <repo-url>
cd <project>
```
2. Setup environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Configure Environment Variables
create a .env file with:
```bash
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/dbname
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0
REDIS_URL=redis://localhost:6379/0
```
4. Run Migrations
```bash
python manage.py migrate
``` 
5. Create Superuser
```bash
python manage.py createsuperuser
```
6. Start Development Server
```bash
python manage.py runserver
```
## Engineering Decisions
- Custom user model implemented early to avoid migration complexity later.
- UUID used for candidate ID for safe external API exposure.
- Status field introduced from day one to support async lifecycle transitions.
- Validation handled at serializer level for API consistency.
- System structured to scale into service-based architecture if needed.

## Roadmap

- Celery + Redis integration for background processing
- Periodic batch scheduler
- Retry mechanism with attempt tracking
- Advanced search API
- Reporting endpoints
- Containerization with Docker
- Production deployment
- Test coverage expansion
- Observability integration (logging + metrics)

## Why This Project Matters
This project demonstrates:
- API design principles
- Clean architecture
- Authentication & RBAC implementation
- Concurrency-aware design
- External system integration strategy
- Scalable batch processing patterns

