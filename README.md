# Django Healthcare Backend

Backend for a healthcare application using Django, Django REST Framework (DRF), PostgreSQL, and JWT authentication.

**Objective**
Build a secure backend where users can register, log in, and manage patient, doctor, and patient-doctor mappings.

**Status Checklist (Implemented)**
- Django + DRF backend
- PostgreSQL database
- JWT authentication with `djangorestframework-simplejwt`
- REST APIs for Patients, Doctors, and Mappings
- Django ORM models and relationships
- Validation and error handling
- Environment variables for secrets/config

**Project Structure**
- `Healthcare/Healthcare/` Django project settings and URLs
- `Healthcare/accounts/` Auth + JWT
- `Healthcare/patients/` Patient APIs
- `Healthcare/doctors/` Doctor APIs
- `Healthcare/mappings/` Patient-Doctor mapping APIs

**Setup**
1. Create `Healthcare/.env`
```env
SECRET_KEY=your-secret
DEBUG=True
DB_NAME=healthcare_db
DB_USER=healthcare_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```
2. Install dependencies
```bash
pip install -r Healthcare/requirements.txt
```
3. Run migrations
```bash
python Healthcare/manage.py migrate
```
4. Start the server
```bash
python Healthcare/manage.py runserver
```

**Seed Data (Optional)**
Seeds 10 doctors and 10 patients.
```bash
python Healthcare/manage.py seed_data
```
Assign patients to a specific user (username or email):
```bash
python Healthcare/manage.py seed_data --username your@email.com
```

**Authentication**
Login accepts `email` (or `username`) and `password`. Tokens are JWT.

Register
```http
POST /api/auth/register/
Content-Type: application/json

{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "password": "password123"
}
```
Response
```json
{
  "user": {
    "id": 1,
    "name": "Jane Doe",
    "email": "jane@example.com"
  },
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "jane@example.com",
  "password": "password123"
}
```
Response
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}
```

**Auth Header for Protected APIs**
```http
Authorization: Bearer <access_token>
```

**Patients API**
Create patient
```http
POST /api/patients/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "John Smith",
  "age": 42,
  "gender": "Male",
  "medical_history": "Diabetes"
}
```

List patients (only the authenticated user’s patients)
```http
GET /api/patients/
Authorization: Bearer <access_token>
```

Get patient
```http
GET /api/patients/<id>/
Authorization: Bearer <access_token>
```

Update patient
```http
PUT /api/patients/<id>/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "John Smith",
  "age": 43,
  "gender": "Male",
  "medical_history": "Diabetes, Hypertension"
}
```

Delete patient
```http
DELETE /api/patients/<id>/
Authorization: Bearer <access_token>
```

**Doctors API**
Create doctor
```http
POST /api/doctors/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Dr. Priya Shah",
  "specialization": "Cardiology",
  "email": "priya.shah@example.com",
  "phone": "+1-555-555-1234"
}
```

List doctors
```http
GET /api/doctors/
Authorization: Bearer <access_token>
```

Get doctor
```http
GET /api/doctors/<id>/
Authorization: Bearer <access_token>
```

Update doctor
```http
PUT /api/doctors/<id>/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Dr. Priya Shah",
  "specialization": "Cardiology",
  "email": "priya.shah@example.com",
  "phone": "+1-555-555-9999"
}
```

Delete doctor
```http
DELETE /api/doctors/<id>/
Authorization: Bearer <access_token>
```

**Patient-Doctor Mappings API**
Assign a doctor to a patient
```http
POST /api/mappings/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "patient": 1,
  "doctor": 1
}
```

List all mappings (only your patients)
```http
GET /api/mappings/
Authorization: Bearer <access_token>
```

Get all doctors assigned to a specific patient
```http
GET /api/mappings/<patient_id>/
Authorization: Bearer <access_token>
```

Remove a doctor from a patient
```http
DELETE /api/mappings/<id>/
Authorization: Bearer <access_token>
```

**Notes**
- Patient records are scoped to the authenticated user.
- Mapping creation validates patient ownership and prevents duplicates.
