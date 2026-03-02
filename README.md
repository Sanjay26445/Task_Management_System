# Task Management System with Authentication and Analytics

A full-stack task management application with JWT authentication, historical tracking, and productivity analytics.

## Tech Stack

- **Backend**: Django + Django REST Framework
- **Frontend**: React + TypeScript + Tailwind CSS
- **Database**: PostgreSQL
- **Authentication**: JWT (access + refresh tokens)

## Features

- JWT-based authentication with access and refresh tokens
- Complete task CRUD operations
- Task history tracking for all modifications
- User feedback system
- Analytics dashboard with productivity metrics
- Responsive UI with Tailwind CSS

## Project Structure

```
task-management-system/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # Database models
│   │   ├── serializers/  # DRF serializers
│   │   ├── services/     # Business logic
│   │   ├── repositories/ # Data access layer
│   │   └── core/         # Config and utilities
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API service layer
│   │   ├── contexts/     # React contexts
│   │   └── utils/        # Utilities
│   └── package.json
└── docker-compose.yml
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Docker (optional)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=taskmanagement
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser (optional):
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```env
VITE_API_URL=http://localhost:8000/api
```

4. Run development server:
```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

### Docker Setup (Alternative)

```bash
docker-compose up --build
```

## JWT Authentication Flow

### Token Types

1. **Access Token**: Short-lived (15 minutes), used for API requests
2. **Refresh Token**: Long-lived (7 days), used to obtain new access tokens

### Authentication Flow

1. **Registration**: User registers with email, name, and password
   - Password is hashed using bcrypt
   - User record created in database

2. **Login**: User provides email and password
   - Credentials validated
   - Access token and refresh token generated
   - Tokens returned to client

3. **API Requests**: Client includes access token in Authorization header
   - Format: `Authorization: Bearer <access_token>`
   - Backend validates token on protected routes

4. **Token Refresh**: When access token expires
   - Client sends refresh token to `/api/auth/token/refresh/`
   - New access token returned
   - Refresh token remains valid

5. **Logout**: Client discards tokens

### Security Measures

- Passwords hashed with bcrypt (cost factor 12)
- JWT tokens signed with HS256 algorithm
- Refresh tokens stored securely
- CORS configured for frontend origin
- Protected routes require valid JWT

## Database Schema

### Users Table
- `id`: Primary key
- `name`: User's full name
- `email`: Unique email (used for login)
- `password`: Hashed password
- `created_at`: Timestamp

### Tasks Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `title`: Task title
- `description`: Task description
- `priority`: Enum (Low, Medium, High)
- `status`: Enum (Pending, Completed, Archived)
- `due_date`: Due date
- `created_at`: Timestamp
- `updated_at`: Timestamp

### TaskHistory Table
- `id`: Primary key
- `task_id`: Foreign key to Tasks
- `action_type`: Enum (created, updated, completed, deleted)
- `previous_state`: JSON field with previous task state
- `timestamp`: Timestamp

### Feedback Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `task_id`: Foreign key to Tasks (optional)
- `comment`: Feedback text
- `rating`: Integer (1-5)
- `created_at`: Timestamp

### Relationships
- One User has many Tasks (1:N)
- One Task has many TaskHistory records (1:N)
- One User has many Feedback records (1:N)
- One Task has many Feedback records (1:N, optional)

### Indexes
- `tasks.user_id` - for filtering user tasks
- `tasks.status` - for status filtering
- `tasks.priority` - for priority filtering
- `tasks.due_date` - for date-based queries
- `taskhistory.task_id` - for history lookups
- `feedback.user_id` - for user feedback queries

## Analytics Logic

### Metrics Calculated

1. **Total Tasks**: Count of all tasks for user
2. **Completed Tasks**: Count of tasks with status='Completed'
3. **Completion Percentage**: (Completed / Total) × 100
4. **Tasks Per Period**: Group by date and count
5. **Most Productive Day**: Day with most completions
6. **Average Completion Time**: Average time from created_at to completion
7. **Priority Distribution**: Count by priority level
8. **Productivity Score**: Custom formula (see below)

### Productivity Score Formula

```
Productivity Score = (
    (Completed Tasks × 10) +
    (High Priority Completed × 5) +
    (Medium Priority Completed × 3) +
    (On-Time Completions × 7) -
    (Overdue Tasks × 3)
) / Total Days Active
```

Factors:
- Rewards task completion
- Bonus for high-priority completions
- Bonus for meeting deadlines
- Penalty for overdue tasks
- Normalized by days active

## API Documentation

API documentation available at:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

### Key Endpoints

**Authentication**
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh access token

**Tasks**
- `GET /api/tasks/` - List tasks (with filters)
- `POST /api/tasks/` - Create task
- `GET /api/tasks/{id}/` - Get task detail
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `POST /api/tasks/{id}/complete/` - Mark as complete
- `POST /api/tasks/{id}/archive/` - Archive task

**Analytics**
- `GET /api/analytics/` - Get all analytics data

**Feedback**
- `POST /api/feedback/` - Submit feedback
- `GET /api/feedback/` - List user feedback

## Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

The application can be deployed using:
- Backend: Heroku, Railway, DigitalOcean
- Frontend: Vercel, Netlify
- Database: Managed PostgreSQL (AWS RDS, DigitalOcean)

## License

MIT
