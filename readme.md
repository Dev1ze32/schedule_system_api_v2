# Faculty Schedule Management API

A RESTful API for managing faculty schedules, room assignments, and semester declarations built with Flask and MySQL.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Environment Configuration](#environment-configuration)
- [Running the API](#running-the-api)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

---

## Features

- **Authentication & Authorization**: JWT-based authentication with role-based access (Faculty & Admin)
- **Faculty Management**: Create, read, update, and delete faculty accounts
- **Semester Management**: Manage academic semesters with activation/deactivation
- **Schedule Declarations**: Faculty can declare their teaching schedules
- **Room Management**: Track and manage classroom assignments
- **Bulk Upload**: CSV/Excel file upload for batch schedule creation
- **Rate Limiting**: Built-in protection against API abuse
- **CORS Support**: Configured for cross-origin requests
- **Health Check**: Monitor API and database status

---

## Tech Stack

- **Framework**: Flask 2.x
- **Database**: MySQL 8.0
- **Containerization**: Docker & Docker Compose
- **Authentication**: JWT (JSON Web Tokens)
- **Security**: bcrypt for password hashing, CORS, rate limiting
- **File Processing**: Pandas for CSV/Excel parsing

---

## Prerequisites

Before running this application, ensure you have:

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Git**: For cloning the repository

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd faculty-schedule-api
```

### 2. Create Environment File

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration (see [Environment Configuration](#environment-configuration) below).

### 3. Build and Start Containers

```bash
#start up
sudo service docker start or sudo systemctl start docker
then in rpi sudo systemctl enable docker
# check if the docker is running
sudo systemctl status docker

#first init
sudo docker-compose up -d --build api

#if failed
docker compose down

# if you want to remove all
docker system prune

# if you want to rebuild and start 
docker compose up -d --build

# Build the Docker images
docker-compose build

# Start the services
docker-compose up -d
```

### 4. Verify Installation

Check if containers are running:

```bash
docker-compose ps
```

Check API health:

```bash
curl http://localhost:5000/api/health
```

---

## Environment Configuration

Create a `.env` file with the following variables:

```env
# Database Configuration
DB_HOST=mysql
DB_USER=root
DB_PASSWORD=your_secure_password_here
DB_NAME=faculty_db

# JWT Configuration
JWT_SECRET_KEY=your_very_secret_jwt_key_here_min_32_chars

# Application Configuration
DEBUG=False
API_TITLE=Faculty Schedule API
API_VERSION=1.0.0

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Rate Limiting
RATELIMIT_ENABLED=True
RATELIMIT_DEFAULT=100 per hour
RATELIMIT_STORAGE_URL=memory://

# File Upload
MAX_FILE_SIZE=10485760  # 10MB in bytes

# Security
FORCE_HTTPS=False  # Set to True in production
```

### Important Notes:

- **JWT_SECRET_KEY**: Should be a long, random string (minimum 32 characters)
- **DB_PASSWORD**: Use a strong password in production
- **DEBUG**: Must be `False` in production
- **FORCE_HTTPS**: Enable in production environments

---

## Running the API

### Start the Application

```bash
docker-compose up -d
```

### Stop the Application

```bash
docker-compose down
```

### View Logs

```bash
# All services
docker-compose logs -f

# API only
docker-compose logs -f api

# MySQL only
docker-compose logs -f mysql
```

### Restart Services

```bash
docker-compose restart
```

### Rebuild After Code Changes

```bash
docker-compose down
docker-compose build
docker-compose up -d
```

### Access MySQL Database

```bash
docker exec -it faculty_mysql mysql -u root -p
```

---

## API Documentation

Base URL: `http://localhost:5000/api`

### Authentication

All endpoints (except login and health check) require authentication via JWT token in the Authorization header.

---

## API Endpoints

### Health Check

#### Check API Status

```http
GET /api/health
```

**Response:**

```json
{
  "status": "healthy",
  "server": "Faculty Schedule API",
  "version": "1.0.0",
  "database": "connected",
  "environment": "production"
}
```

---

### Authentication Endpoints

#### Faculty Login

```http
POST /api/auth/login
```

**Request Body:**

```json
{
  "username": "faculty_user",
  "password": "password123"
}
```

**Response:**

```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "faculty": {
    "faculty_id": 1,
    "username": "faculty_user",
    "faculty_name": "John Doe",
    "email": "john@example.com",
    "department": "Computer Science"
  }
}
```

**Rate Limit:** 5 requests per minute

---

#### Admin Login

```http
POST /api/auth/admin/login
```

**Request Body:**

```json
{
  "username": "admin_user",
  "password": "admin_password"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "admin_id": 1,
    "admin_name": "Admin User",
    "email": "admin@example.com"
  }
}
```

**Rate Limit:** 5 requests per minute

---

### Semester Management

#### Get All Semesters

```http
GET /api/semesters
```

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response:**

```json
[
  {
    "semester_id": 1,
    "semester_name": "Fall 2024",
    "semester_code": "FALL2024",
    "academic_year": "2024-2025",
    "start_date": "2024-09-01",
    "end_date": "2024-12-15",
    "is_active": true
  }
]
```

---

#### Get Active Semester

```http
GET /api/semesters/active
```

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response:**

```json
{
  "semester_id": 1,
  "semester_name": "Fall 2024",
  "semester_code": "FALL2024",
  "academic_year": "2024-2025",
  "start_date": "2024-09-01",
  "end_date": "2024-12-15",
  "is_active": true
}
```

---

#### Get Semester by ID

```http
GET /api/semesters/{semester_id}
```

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response:**

```json
{
  "semester_id": 1,
  "semester_name": "Fall 2024",
  "semester_code": "FALL2024",
  "academic_year": "2024-2025",
  "start_date": "2024-09-01",
  "end_date": "2024-12-15",
  "is_active": true
}
```

---

#### Get Semester Statistics

```http
GET /api/semesters/{semester_id}/statistics
```

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response:**

```json
{
  "semester_id": 1,
  "total_declarations": 45,
  "total_faculty": 12,
  "rooms_used": 8
}
```

---

#### Create Semester (Admin Only)

```http
POST /api/semesters
```

**Headers:**

```
Authorization: Bearer <admin_jwt_token>
```

**Request Body:**

```json
{
  "semester_name": "Spring 2025",
  "semester_code": "SPRING2025",
  "academic_year": "2024-2025",
  "start_date": "2025-01-15",
  "end_date": "2025-05-30"
}
```

**Response:**

```json
{
  "message": "Semester created",
  "semester_id": 2
}
```

---

#### Activate Semester (Admin Only)

```http
POST /api/semesters/{semester_id}/activate
```

**Headers:**

```
Authorization: Bearer <admin_jwt_token>
```

**Response:**

```json
{
  "message": "Semester activated successfully",
  "affected_declarations": 23
}
```

---

#### Deactivate Semester (Admin Only)

```http
POST /api/semesters/{semester_id}/deactivate
```

**Headers:**

```
Authorization: Bearer <admin_jwt_token>
```

**Response:**

```json
{
  "message": "Semester deactivated successfully"
}
```

---

#### Update Semester (Admin Only)

```http
PUT /api/semesters/{semester_id}
```

**Headers:**

```
Authorization: Bearer <admin_jwt_token>
```

**Request Body:**

```json
{
  "semester_name": "Spring 2025 Updated",
  "end_date": "2025-06-15"
}
```

**Response:**

```json
{
  "message": "Semester updated successfully"
}
```

---

#### Delete Semester (Admin Only)

```http
DELETE /api/semesters/{semester_id}
```

**Headers:**

```
Authorization: Bearer <admin_jwt_token>
```

**Response:**

```json
{
  "message": "Semester deleted successfully"
}
```

---

### Declaration Management (Faculty Schedules)

#### Create Declaration

```http
POST /api/declarations
```

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Request Body:**

```json
{
  "room": "Room 101",
  "semester_id": 1,
  "subject_code": "CS101",
  "class_section": "A",
  "day": "Monday",
  "start_time": "08:00:00",
  "end_time": "10:00:00"
}
```

**Response:**

```json
{
  "message": "Declaration created",
  "declaration_id": 15
}
```

**Possible Errors:**

- `400`: Missing required fields
- `404`: Room not found
- `409`: Schedule conflict

---

#### Get My Declarations

```http
GET /api/declarations/me?semester_id={semester_id}
```

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**

- `semester_id` (optional): Filter by semester

**Response:**

```json
[
  {
    "declaration_id": 15,
    "room": "Room 101",
    "building": "Main Building",
    "floor": 1,
    "subject_code": "CS101",
    "class_section": "A",
    "day": "Monday",
    "start_time": "08:00:00",
    "end_time": "10:00:00",
    "semester_name": "Fall 2024"
  }
]
```

---

#### Update Declaration

```http
PUT /api/declarations/{declaration_id}
```

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Request Body (all fields optional):**

```json
{
  "room": "Room 102",
  "subject_code": "CS102",
  "class_section": "B",
  "day": "Tuesday",
  "start_time": "10:00:00",
  "end_time": "12:00:00"
}
```

**Response:**

```json
{
  "message": "Declaration updated successfully"
}
```

---

#### Delete Declaration

```http
DELETE /api/declarations/{declaration_id}
```

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response:**

```json
{
  "message": "Declaration deleted successfully"
}
```

---

### Room Management

#### Get All Rooms

```http
GET /api/rooms/all
```

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response:**

```json
[
  {
    "room_id": 1,
    "building": "Main Building",
    "room_number": "Room 101",
    "floor": 1
  },
  {
    "room_id": 2,
    "building": "Science Building",
    "room_number": "Lab 201",
    "floor": 2
  }
]
```

---

#### Create Room

```http
POST /api/rooms
```

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Request Body:**

```json
{
  "room_name": "Room 305",
  "building": "Engineering Building",
  "floor": 3
}
```

**Response:**

```json
{
  "message": "Room created",
  "room_id": 15
}
```

---

### File Upload (Schedule Import)

#### Upload Schedule File

```http
POST /api/upload/schedule
```

**Headers:**

```
Authorization: Bearer <jwt_token>
Content-Type: multipart/form-data
```

**Form Data:**

- `file`: CSV/XLSX/XLS file
- `semester_id`: Integer

**Response (Success):**

```json
{
  "message": "Schedule uploaded successfully",
  "summary": {
    "total": 50,
    "successful": 50,
    "failed": 0
  },
  "details": []
}
```

**Response (Partial Success):**

```json
{
  "message": "Schedule uploaded with errors",
  "summary": {
    "total": 50,
    "successful": 45,
    "failed": 5
  },
  "failed_rows": [
    {
      "row": 3,
      "error": "Room not found"
    }
  ]
}
```

**Rate Limit:** 30 requests per hour

**Supported File Types:** CSV, XLSX, XLS

---

#### Validate Schedule File

```http
POST /api/upload/schedule/validate
```

**Headers:**

```
Authorization: Bearer <jwt_token>
Content-Type: multipart/form-data
```

**Form Data:**

- `file`: CSV/XLSX/XLS file

**Response:**

```json
{
  "valid": true,
  "row_count": 50,
  "columns": [
    "room",
    "subject_code",
    "class_section",
    "day",
    "start_time",
    "end_time"
  ],
  "preview": [
    {
      "room": "Room 101",
      "subject_code": "CS101",
      "class_section": "A",
      "day": "Monday",
      "start_time": "08:00:00",
      "end_time": "10:00:00"
    }
  ]
}
```

---

#### Download Template

```http
GET /api/upload/template
```

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response:** CSV file download

**Template Format:**

```csv
room,subject_code,class_section,day,start_time,end_time
Room 101,CS101,A,Monday,08:00:00,10:00:00
Room 102,CS102,B,Tuesday,10:00:00,12:00:00
```

---

### Admin - Faculty Management

#### Create Faculty Account

```http
POST /api/admin/create-faculty
```

**Headers:**

```
Authorization: Bearer <admin_jwt_token>
```

**Request Body:**

```json
{
  "faculty_name": "Jane Smith",
  "email": "jane.smith@university.edu",
  "department": "Mathematics",
  "username": "jsmith",
  "password": "SecurePass123!"
}
```

**Response:**

```json
{
  "message": "Faculty created",
  "faculty_id": 25
}
```

**Password Requirements:**

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

---

#### Get All Faculty

```http
GET /api/admin/faculty
```

**Headers:**

```
Authorization: Bearer <admin_jwt_token>
```

**Response:**

```json
[
  {
    "faculty_id": 1,
    "faculty_name": "John Doe",
    "email": "john@example.com",
    "department": "Computer Science",
    "username": "jdoe",
    "has_login": true
  }
]
```

---

#### Delete Faculty

```http
DELETE /api/admin/faculty/{faculty_id}
```

**Headers:**

```
Authorization: Bearer <admin_jwt_token>
```

**Response:**

```json
{
  "message": "Faculty account deleted successfully"
}
```

---

#### Reset Faculty Password

```http
POST /api/admin/reset-password
```

**Headers:**

```
Authorization: Bearer <admin_jwt_token>
```

**Request Body:**

```json
{
  "faculty_id": 5,
  "new_password": "NewSecurePass123!"
}
```

**Response:**

```json
{
  "message": "Password reset successfully"
}
```

---

### Admin - Admin Account Management

#### Get All Admins

```http
GET /api/admin/accounts
```

**Headers:**

```
Authorization: Bearer <admin_jwt_token>
```

**Response:**

```json
[
  {
    "admin_id": 1,
    "admin_name": "Super Admin",
    "email": "admin@university.edu",
    "username": "superadmin"
  }
]
```

---

#### Create Admin Account

```http
POST /api/admin/create-admin
```

**Headers:**

```
Authorization: Bearer <admin_jwt_token>
```

**Request Body:**

```json
{
  "name": "New Admin",
  "email": "newadmin@university.edu",
  "username": "newadmin",
  "password": "SecureAdminPass123!"
}
```

**Response:**

```json
{
  "message": "Admin created",
  "admin_id": 3
}
```

---

#### Reset Admin Password

```http
POST /api/admin/reset-admin-password
```

**Headers:**

```
Authorization: Bearer <admin_jwt_token>
```

**Request Body:**

```json
{
  "admin_id": 2,
  "new_password": "NewAdminPass123!"
}
```

**Response:**

```json
{
  "message": "Admin password reset successfully"
}
```

---

#### Delete Admin Account

```http
DELETE /api/admin/{admin_id}
```

**Headers:**

```
Authorization: Bearer <admin_jwt_token>
```

**Response:**

```json
{
  "message": "Admin account deleted successfully"
}
```

**Note:** Admins cannot delete their own account.

---

## Authentication

### JWT Token Structure

After successful login, you'll receive a JWT token. Include it in subsequent requests:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Expiration

- **Faculty tokens**: Valid for 24 hours (86400 seconds)
- **Admin tokens**: Valid for 12 hours (43200 seconds)

### Example Request with Authentication

```bash
curl -X GET http://localhost:5000/api/semesters \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

---

## Error Handling

### Standard Error Response Format

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

### HTTP Status Codes

| Code | Description                               |
| ---- | ----------------------------------------- |
| 200  | Success                                   |
| 201  | Created                                   |
| 206  | Partial Content (some operations failed)  |
| 400  | Bad Request                               |
| 401  | Unauthorized                              |
| 403  | Forbidden                                 |
| 404  | Not Found                                 |
| 409  | Conflict (duplicate or schedule conflict) |
| 413  | Payload Too Large                         |
| 429  | Too Many Requests (rate limit exceeded)   |
| 500  | Internal Server Error                     |

### Common Error Examples

#### 400 Bad Request

```json
{
  "error": "Missing required fields"
}
```

#### 401 Unauthorized

```json
{
  "error": "Unauthorized",
  "message": "Authentication required"
}
```

#### 409 Conflict

```json
{
  "error": "Schedule conflict detected for Monday 08:00-10:00"
}
```

#### 429 Rate Limit Exceeded

```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please try again later."
}
```

---

## Rate Limiting

### Default Limits

- **Login endpoints**: 5 requests per minute
- **File upload**: 30 requests per hour
- **All other endpoints**: 100 requests per hour (configurable)

### Rate Limit Headers

When rate limited, the response includes:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640000000
```

---

## Security Features

### Password Requirements

- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one number (0-9)
- At least one special character (!@#$%^&\*()\_+-=[]{}|;:,.<>?)

### Username Requirements

- No spaces allowed
- No special characters except underscore and hyphen
- Alphanumeric characters only

### Security Headers

- `X-Frame-Options: SAMEORIGIN`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- CORS configured for specified origins only
- HTTPS enforcement (in production)

---

## Database Schema Overview

### Key Tables

- **faculty**: Faculty member profiles
- **faculty_login**: Authentication credentials
- **admin_accounts**: Administrator accounts
- **semesters**: Academic semester definitions
- **rooms**: Classroom/room information
- **declarations**: Faculty schedule declarations

---

## Troubleshooting

### Container Issues

**Problem**: Containers not starting

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs

# Restart services
docker-compose restart
```

**Problem**: Database connection failed

```bash
# Check MySQL is healthy
docker-compose ps mysql

# Access MySQL container
docker exec -it faculty_mysql mysql -u root -p

# Check database exists
SHOW DATABASES;
```

### API Issues

**Problem**: 401 Unauthorized errors

- Verify JWT token is valid and not expired
- Check Authorization header format: `Bearer <token>`
- Ensure token is for the correct role (faculty vs admin)

**Problem**: CORS errors

- Add your frontend URL to `CORS_ORIGINS` in `.env`
- Restart the API after changing environment variables

---

## Development

### Running in Development Mode

Set `DEBUG=True` in `.env`:

```env
DEBUG=True
```

This enables:

- Detailed error messages
- Auto-reload on code changes
- Debug logging

**Warning**: Never use DEBUG mode in production!

### Adding New Endpoints

1. Create route in appropriate blueprint file
2. Add decorators for authentication/validation
3. Update this README with endpoint documentation

---

## Production Deployment

### Pre-deployment Checklist

- [ ] Set `DEBUG=False`
- [ ] Use strong `JWT_SECRET_KEY` (32+ characters)
- [ ] Use strong database password
- [ ] Enable `FORCE_HTTPS=True`
- [ ] Configure proper `CORS_ORIGINS`
- [ ] Set up SSL/TLS certificates
- [ ] Configure backup strategy for MySQL
- [ ] Review rate limits
- [ ] Set up monitoring and logging

### Environment Variables for Production

```env
DEBUG=False
FORCE_HTTPS=True
JWT_SECRET_KEY=<64-character-random-string>
DB_PASSWORD=<very-strong-password>
CORS_ORIGINS=https://yourdomain.com
```

---

## Support & Contributing

### Reporting Issues

When reporting issues, please include:

1. Environment details (OS, Docker version)
2. Steps to reproduce
3. Expected vs actual behavior
4. Relevant log output

### License

[Specify your license here]

---

## API Version

**Current Version:** 1.0.0

**Last Updated:** January 2025

---

## Contact

For questions or support, contact: [your-email@university.edu]
