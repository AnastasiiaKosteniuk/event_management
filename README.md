# Event Management API

This is a RESTful API for managing events and user registrations, built with Django and Django REST Framework. It provides endpoints for creating, reading, updating, and deleting events, as well as user registration and authentication using JSON Web Tokens (JWT).

## Features

- **Event Management**: Full CRUD functionality for events.
- **User Authentication**: User registration and JWT-based authentication.
- **Event Registration**: Users can register/unregister for events.
- **Permissions**: Only event organizers can modify, delete, or view participants of their events.
- **Search, Filtering & Ordering**: Events can be searched, filtered by date/location, and ordered.
- **API Documentation**: Interactive docs via Swagger UI and ReDoc (`drf-spectacular`).

## API Endpoints

All endpoints are prefixed with `/api/`.

### Authentication

| Method | Endpoint               | Description                          |
|--------|------------------------|--------------------------------------|
| POST   | `/api/auth/register/`  | Register a new user.                 |
| POST   | `/api/auth/login/`     | Obtain JWT access and refresh tokens.|
| POST   | `/api/auth/token/refresh/` | Refresh an expired access token. |

### Events

| Method | Endpoint                     | Description                                                                 |
|--------|------------------------------|-----------------------------------------------------------------------------|
| GET    | `/api/events/`               | List all events (authenticated users only).                                |
| POST   | `/api/events/`               | Create a new event (authenticated users only).                             |
| GET    | `/api/events/{id}/`          | Retrieve event details.                                                    |
| PUT    | `/api/events/{id}/`          | Update event (organizer only).                                             |
| PATCH  | `/api/events/{id}/`          | Partial update (organizer only).                                           |
| DELETE | `/api/events/{id}/`          | Delete event (organizer only).                                             |
| POST   | `/api/events/{id}/register/` | Register for an event (not for past events or own events).                 |
| DELETE | `/api/events/{id}/unregister/`| Unregister from an event.                                                 |
| GET    | `/api/events/{id}/participants/`| List participants (organizer only).                                      |

### API Documentation

| Method | Endpoint        | Description                     |
|--------|-----------------|---------------------------------|
| GET    | `/api/schema/`  | OpenAPI 3.0 schema (JSON)       |
| GET    | `/api/docs/`    | Swagger UI                      |
| GET    | `/api/redoc/`   | ReDoc                           |

## JWT Authentication

- **Access Token**: 15 minutes
- **Refresh Token**: 7 days
- **Token Rotation**: Enabled (old refresh token invalidated on use)

> 🔒 **Include token in requests**:
> ```http
> Authorization: Bearer <your_access_token>
> ```

## Getting Started

### Prerequisites

- Python 3.8+
- Docker & Docker Compose

### Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/AnastasiiaKosteniuk/event_management
   cd event_management
   ```

2. **Create .env**
    ```ini
    # .env.example
    SECRET_KEY=your_strong_secret_key_here
    DEBUG=True
    
    POSTGRES_DB=eventdb
    POSTGRES_USER=eventuser
    POSTGRES_PASSWORD=eventpass
    DB_HOST=db
    DB_PORT=5432
    ```

3. **Run with Docker**
    ```bash
    docker-compose up --build
    ```

4. **API is ready at:**
- Base URL: http://localhost:8000/api/
- Swagger UI: http://localhost:8000/api/docs/