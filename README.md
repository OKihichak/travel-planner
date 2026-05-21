# Travel Planner API

Travel Planner API built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

The application allows travellers to create travel projects, manage places to visit, attach notes, and track visited locations.

---

# Setup

Clone repository:

```bash
git clone https://github.com/OKihichak/travel-planner.git
cd travel-planner
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
uvicorn main:app --reload
```

Application will run on:

```txt
http://127.0.0.1:8000
```

---

# API Documentation

Swagger UI:

```txt
http://127.0.0.1:8000/docs
```

OpenAPI schema:

```txt
http://127.0.0.1:8000/openapi.json
```

---

# Technologies Used

- FastAPI
- SQLAlchemy
- SQLite
- Requests
- Pydantic
- Uvicorn
- Art Institute of Chicago API

---

# Features

## Travel Projects

Implemented functionality:

- Create travel projects
- Update project information
- Delete projects
- List all projects
- Get a single project

Project fields:

- Name
- Description (optional)
- Start Date (optional)

Additional business logic:

- A project **cannot be deleted** if any of its places are already marked as visited.
- A project is automatically marked as **completed** when all project places are visited.

---

## Places / Project Places

Implemented functionality:

- Create project **with places in a single request**
- Add places to existing projects
- Update place information
- Update notes
- Mark places as visited
- List all places for a project
- Get a single place inside a project

---

## Third-Party API Integration

The application integrates with the **Art Institute of Chicago API**.

External artworks are validated before storage.

Example API used:

```txt
https://api.artic.edu/api/v1/artworks
```

Before saving a place:

- artwork existence is validated
- artwork title is fetched from external API
- external artwork ID is stored

---

## Validation Rules

Implemented validations:

- Maximum **10 places** per project
- Duplicate external places inside the same project are prevented
- Invalid artwork IDs return appropriate HTTP errors
- Request body validation handled through **FastAPI + Pydantic**

---

## Filtering

Implemented filtering for listing endpoints.

Examples:

Filter projects by name:

```txt
GET /projects?name=Berlin
```

Filter places by visited status:

```txt
GET /projects/{project_id}/places?visited=true
```

---

## Authentication

A simple authentication mechanism was implemented for demonstration purposes.

Protected endpoints require credentials.

Example credentials:

```txt
username: admin
password: password123
```

For a production application, a token-based solution (JWT / expiring access tokens / hashed passwords) would be recommended.


---

## Project Structure

```txt
travel-planner/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── services.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Database

SQLite database used for persistence.

No external database setup required.

---

## Notes

This project was developed with focus on:

- REST API design
- Database interaction
- Third-party API integration
- Validation and business logic
- FastAPI best practices
