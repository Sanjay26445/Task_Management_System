# Entity-Relationship Diagram

## Database Schema

```
┌─────────────────────────┐
│        Users            │
├─────────────────────────┤
│ PK  id                  │
│     name                │
│ UQ  email               │
│     password (hashed)   │
│     is_active           │
│     is_staff            │
│     created_at          │
└─────────────────────────┘
           │
           │ 1:N
           │
           ▼
┌─────────────────────────┐
│        Tasks            │
├─────────────────────────┤
│ PK  id                  │
│ FK  user_id             │
│     title               │
│     description         │
│     priority            │
│     status              │
│     due_date            │
│     created_at          │
│     updated_at          │
└─────────────────────────┘
           │
           │ 1:N
           │
           ▼
┌─────────────────────────┐
│     TaskHistory         │
├─────────────────────────┤
│ PK  id                  │
│ FK  task_id             │
│     action_type         │
│     previous_state      │
│     timestamp           │
└─────────────────────────┘


┌─────────────────────────┐
│        Users            │
└─────────────────────────┘
           │
           │ 1:N
           │
           ▼
┌─────────────────────────┐
│       Feedback          │
├─────────────────────────┤
│ PK  id                  │
│ FK  user_id             │
│ FK  task_id (nullable)  │
│     comment             │
│     rating (1-5)        │
│     created_at          │
└─────────────────────────┘
           ▲
           │
           │ N:1 (nullable)
           │
┌─────────────────────────┐
│        Tasks            │
└─────────────────────────┘
```

## Relationships

### Users → Tasks (One-to-Many)
- One user can have many tasks
- Each task belongs to exactly one user
- Foreign Key: `tasks.user_id` references `users.id`
- On Delete: CASCADE (when user is deleted, all their tasks are deleted)

### Tasks → TaskHistory (One-to-Many)
- One task can have many history records
- Each history record belongs to exactly one task
- Foreign Key: `taskhistory.task_id` references `tasks.id`
- On Delete: CASCADE (when task is deleted, all history is deleted)
- Purpose: Track all modifications to a task (create, update, complete, delete)

### Users → Feedback (One-to-Many)
- One user can provide many feedback entries
- Each feedback belongs to exactly one user
- Foreign Key: `feedback.user_id` references `users.id`
- On Delete: CASCADE

### Tasks → Feedback (One-to-Many)
- One task can have many feedback entries
- Feedback can be associated with a task
- Foreign Key: `feedback.task_id` references `tasks.id` (nullable)
- On Delete: CASCADE

## Field Details

### Users
- `id`: Auto-incrementing primary key
- `name`: User's full name (VARCHAR 255)
- `email`: Unique email address (VARCHAR 255, UNIQUE)
- `password`: Bcrypt hashed password (VARCHAR 255)
- `is_active`: Boolean flag for account status
- `is_staff`: Boolean flag for admin access
- `created_at`: Timestamp of account creation

### Tasks
- `id`: Auto-incrementing primary key
- `user_id`: Foreign key to Users
- `title`: Task title (VARCHAR 255)
- `description`: Task description (TEXT)
- `priority`: Enum ('Low', 'Medium', 'High')
- `status`: Enum ('Pending', 'Completed', 'Archived')
- `due_date`: Due date (DATE, nullable)
- `created_at`: Timestamp of task creation
- `updated_at`: Timestamp of last update (auto-updated)

### TaskHistory
- `id`: Auto-incrementing primary key
- `task_id`: Foreign key to Tasks
- `action_type`: Enum ('created', 'updated', 'completed', 'deleted')
- `previous_state`: JSON field storing previous task state
- `timestamp`: Timestamp of the action

### Feedback
- `id`: Auto-incrementing primary key
- `user_id`: Foreign key to Users
- `task_id`: Foreign key to Tasks (nullable)
- `comment`: Feedback text (TEXT)
- `rating`: Integer rating 1-5 (with validators)
- `created_at`: Timestamp of feedback creation

## Indexes

### Performance Optimization Indexes

1. **tasks.user_id** - B-tree index
   - Purpose: Fast filtering of tasks by user
   - Used in: All task list queries

2. **tasks.status** - B-tree index
   - Purpose: Fast filtering by task status
   - Used in: Status-based queries, analytics

3. **tasks.priority** - B-tree index
   - Purpose: Fast filtering by priority
   - Used in: Priority-based queries, analytics

4. **tasks.due_date** - B-tree index
   - Purpose: Fast date-based queries
   - Used in: Overdue task detection, date filtering

5. **taskhistory.task_id** - B-tree index
   - Purpose: Fast history lookup for a task
   - Used in: Task history retrieval

6. **feedback.user_id** - B-tree index
   - Purpose: Fast feedback lookup by user
   - Used in: User feedback queries

7. **Composite Index: (user_id, status)** on tasks
   - Purpose: Optimize common query pattern
   - Used in: User's tasks filtered by status

8. **Composite Index: (user_id, priority)** on tasks
   - Purpose: Optimize common query pattern
   - Used in: User's tasks filtered by priority

## Normalization

The database follows **Third Normal Form (3NF)**:

1. **First Normal Form (1NF)**: All attributes contain atomic values
   - No repeating groups
   - Each field contains single value

2. **Second Normal Form (2NF)**: No partial dependencies
   - All non-key attributes fully depend on primary key
   - No composite keys with partial dependencies

3. **Third Normal Form (3NF)**: No transitive dependencies
   - No non-key attribute depends on another non-key attribute
   - All attributes depend only on the primary key

## Data Integrity

### Constraints
- Primary Keys: Ensure unique identification
- Foreign Keys: Maintain referential integrity
- Unique Constraints: Email uniqueness in Users
- Check Constraints: Rating between 1-5 in Feedback
- NOT NULL: Required fields enforced at database level

### Cascading Deletes
- User deletion → Cascades to Tasks, Feedback
- Task deletion → Cascades to TaskHistory, Feedback
- Ensures no orphaned records

## Query Patterns

### Common Queries Optimized by Indexes

1. Get user's pending tasks:
   ```sql
   SELECT * FROM tasks WHERE user_id = ? AND status = 'Pending'
   ```
   Uses: Composite index (user_id, status)

2. Get overdue tasks:
   ```sql
   SELECT * FROM tasks WHERE due_date < CURRENT_DATE AND status = 'Pending'
   ```
   Uses: Index on due_date and status

3. Get task history:
   ```sql
   SELECT * FROM taskhistory WHERE task_id = ? ORDER BY timestamp DESC
   ```
   Uses: Index on task_id

4. Analytics queries benefit from status and priority indexes:
   ```sql
   SELECT COUNT(*) FROM tasks WHERE user_id = ? AND status = 'Completed'
   ```
   Uses: Composite index (user_id, status)

## Summary

This ER diagram represents a well-normalized, efficient database schema for the Task Management System with:

- 4 main entities (Users, Tasks, TaskHistory, Feedback)
- Clear relationships with proper foreign keys
- Strategic indexing for performance
- Data integrity through constraints
- Audit trail via TaskHistory
- Third Normal Form (3NF) compliance
- Optimized for common query patterns

The schema supports all application features including authentication, task management, history tracking, feedback, and analytics while maintaining data integrity and performance.
