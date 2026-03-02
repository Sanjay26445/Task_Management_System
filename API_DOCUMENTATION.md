# API Documentation

Base URL: `http://localhost:8000/api`

## Authentication Endpoints

### Register User
```
POST /auth/register/
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "securepassword"
}
```

**Response (201):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Login
```
POST /auth/login/
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response (200):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token
```
POST /auth/token/refresh/
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## Task Endpoints

All task endpoints require authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### List Tasks
```
GET /tasks/
```

**Query Parameters:**
- `status` (optional): Filter by status (Pending, Completed, Archived)
- `priority` (optional): Filter by priority (Low, Medium, High)
- `due_date` (optional): Filter by due date (YYYY-MM-DD)
- `page` (optional): Page number for pagination

**Response (200):**
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/tasks/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Complete project",
      "description": "Finish the task management system",
      "priority": "High",
      "status": "Pending",
      "due_date": "2024-12-31",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Create Task
```
POST /tasks/
```

**Request Body:**
```json
{
  "title": "New Task",
  "description": "Task description",
  "priority": "Medium",
  "due_date": "2024-12-31"
}
```

**Response (201):**
```json
{
  "id": 2,
  "title": "New Task",
  "description": "Task description",
  "priority": "Medium",
  "status": "Pending",
  "due_date": "2024-12-31",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Get Task Detail
```
GET /tasks/{id}/
```

**Response (200):**
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the task management system",
  "priority": "High",
  "status": "Pending",
  "due_date": "2024-12-31",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Update Task
```
PUT /tasks/{id}/
```

**Request Body:**
```json
{
  "title": "Updated Task",
  "description": "Updated description",
  "priority": "High",
  "status": "Completed",
  "due_date": "2024-12-31"
}
```

**Response (200):**
```json
{
  "id": 1,
  "title": "Updated Task",
  "description": "Updated description",
  "priority": "High",
  "status": "Completed",
  "due_date": "2024-12-31",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```

### Delete Task
```
DELETE /tasks/{id}/
```

**Response (204):** No content

### Complete Task
```
POST /tasks/{id}/complete/
```

**Response (200):**
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the task management system",
  "priority": "High",
  "status": "Completed",
  "due_date": "2024-12-31",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```

### Archive Task
```
POST /tasks/{id}/archive/
```

**Response (200):**
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the task management system",
  "priority": "High",
  "status": "Archived",
  "due_date": "2024-12-31",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```

## Analytics Endpoint

### Get Analytics
```
GET /analytics/
```

**Response (200):**
```json
{
  "total_tasks": 10,
  "completed_tasks": 5,
  "completion_percentage": 50.0,
  "tasks_per_day": [
    {
      "date": "2024-01-01",
      "count": 3
    },
    {
      "date": "2024-01-02",
      "count": 2
    }
  ],
  "most_productive_day": {
    "date": "2024-01-01",
    "count": 3
  },
  "average_completion_time_hours": 24.5,
  "priority_distribution": {
    "Low": 2,
    "Medium": 5,
    "High": 3
  },
  "productivity_score": 15.75
}
```

## Feedback Endpoints

### List Feedback
```
GET /feedback/
```

**Response (200):**
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "task": 1,
      "comment": "Great task!",
      "rating": 5,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Create Feedback
```
POST /feedback/
```

**Request Body:**
```json
{
  "task": 1,
  "comment": "This task was helpful",
  "rating": 4
}
```

**Response (201):**
```json
{
  "id": 2,
  "task": 1,
  "comment": "This task was helpful",
  "rating": 4,
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
  "error": "Task not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Interactive Documentation

For interactive API documentation with the ability to test endpoints:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
