# Student Grade Management System

A Flask-based web application for managing student profiles and academic records. Students can maintain school and college records, add subjects and grades, calculate academic performance metrics such as SGPA and CGPA, and download a PDF report.

<p align="center">
  <a href="https://student-grade-management-system-web.onrender.com/">
    <img src="https://img.shields.io/badge/Live%20Demo-Open%20Application-success?style=for-the-badge" alt="Open live demo">
  </a>
</p>

**Live application:** <https://student-grade-management-system-web.onrender.com/>

## Features

### Student account management
- Create a student account and receive a student ID.
- Log in and log out using a session-based flow.
- View and update personal details.
- Delete an account after password confirmation.
- Validate duplicate phone numbers and email addresses.

### Academic record management
- Add, view, update, and delete school academic records.
- Add, view, update, and delete college academic records by degree and semester.
- Store institution, board/branch, and academic-year information.
- Add subjects or courses with grades; college courses also store credit values.
- Prevent duplicate academic records and duplicate subjects within a record.

### Grade calculations and reports
- Convert letter grades to grade points using the mapping defined in `grade_manager.py`.
- Calculate school-record grade averages.
- Calculate semester SGPA using credit-weighted grade points.
- Calculate CGPA across the recorded college subjects.
- View an academic report and download it as a PDF transcript.

## Screenshots

### Home page
![Home page](images/home-page.png)

### Login page
![Login page](images/login-page.png)

### Create account
![Create account](images/create-account.png)

### Dashboard
![Dashboard](images/dashboard.png)

### Update academic record
![Update academic record](images/update-academic-record.png)

### Delete account
![Delete account](images/delete-account.png)

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, Bootstrap, JavaScript, Jinja templates |
| Database | PostgreSQL |
| Database driver | `psycopg2-binary` |
| PDF generation | ReportLab |
| Production application server | Gunicorn |
| Version control | Git and GitHub |

> **Database history:** An earlier command-line version of this project used MySQL. The current web application in this repository uses PostgreSQL through `psycopg2` and the `DATABASE_URL` environment variable. Both MySQL and PostgreSQL are relational database systems and use SQL, but their drivers and some SQL syntax differ. This repository contains the PostgreSQL implementation.

## Application Architecture

The application separates web request handling, student and academic operations, grade calculations, database access, and PDF generation.

```text
Browser
   |
   v
Flask routes and page rendering (app.py)
   |
   v
Application operations (main.py)
   |-- Student and personal information (student.py, person.py)
   |-- Academic records and subjects (academic_manager.py)
   |-- Grade calculations (grade_manager.py)
   |
   v
Database access layer (database.py)
   |
   v
PostgreSQL database

Student report ---> PDFGenerator (pdf_generator.py) ---> PDF download
```

## Project Structure

```text
student-grade-management-system-web/
|
|-- app.py                 # Flask application and web routes
|-- main.py                # Application operations used by the web layer
|-- database.py            # PostgreSQL connection and query execution
|-- person.py              # Base Person class
|-- student.py             # Student account and profile operations
|-- academic_manager.py    # School/college records and subject operations
|-- grade_manager.py       # Grade-point, average, SGPA and CGPA calculations
|-- pdf_generator.py       # PDF transcript generation
|-- requirements.txt       # Python dependencies
|-- sql/
|   `-- schema.sql         # PostgreSQL tables, constraints and indexes
|-- templates/             # Jinja/HTML pages
|-- static/                # CSS, JavaScript and static assets
|-- images/                # README screenshots
|-- README.md
`-- LICENSE
```

## Database Design

The PostgreSQL schema is defined in `sql/schema.sql` and contains three main tables:

| Table | Purpose |
|---|---|
| `students` | Student profile and account information |
| `education_record` | School or college record associated with a student |
| `subject` | Subjects/courses and their grades, associated with an education record |

Relationships:
- One student can have multiple education records.
- One education record can contain multiple subjects/courses.
- Foreign keys use `ON DELETE CASCADE` so dependent records are removed when their parent record is deleted.
- Unique constraints help prevent duplicate phone numbers, email addresses, academic records, and subjects within a record.

## Run Locally

### Prerequisites
- Python 3.x
- Access to a PostgreSQL database
- `psql` command-line client (or another PostgreSQL client) to apply the schema

### 1. Clone the repository

```bash
git clone https://github.com/Vishal-gujjar/student-grade-management-system-web.git
cd student-grade-management-system-web
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a new, empty PostgreSQL database. Set the connection URL and Flask session secret in your shell. Use the connection URL provided by your database host; do not put real credentials in source code or commit them to GitHub.

**Windows PowerShell:**

```powershell
$env:DATABASE_URL = "postgresql://USERNAME:PASSWORD@HOST:5432/DATABASE_NAME"
$env:SECRET_KEY = "replace-with-a-long-random-secret"
```

**macOS/Linux:**

```bash
export DATABASE_URL="postgresql://USERNAME:PASSWORD@HOST:5432/DATABASE_NAME"
export SECRET_KEY="replace-with-a-long-random-secret"
```

Some hosted PostgreSQL providers require SSL parameters in the connection URL.

### 5. Create the database tables

Run the schema against the new database.

**Windows PowerShell:**

```powershell
psql "$env:DATABASE_URL" -f .\sql\schema.sql
```

**macOS/Linux:**

```bash
psql "$DATABASE_URL" -f sql/schema.sql
```

> **Important:** `sql/schema.sql` starts by dropping the `subject`, `education_record`, and `students` tables (using `CASCADE`) before recreating them. Run it only against a new/empty database, or back up existing data first. Running it against a database containing application data will delete that data.

### 6. Start the application

```bash
python app.py
```

Open <http://127.0.0.1:5000> in your browser.

## Deployment

The project includes Gunicorn in `requirements.txt` and can be served by a WSGI-compatible hosting platform.

Typical Render settings:

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app`
- **Environment variables:** `DATABASE_URL` and `SECRET_KEY`

The hosted PostgreSQL database must already contain the tables defined in `sql/schema.sql`. Keep database credentials and secret keys in the hosting provider's environment-variable settings; never commit them to GitHub.

## Grade Calculation

The grade-point mapping is defined in `grade_manager.py`:

| Grade | Grade point |
|---|---:|
| A+, A | 10 |
| A- | 9 |
| B | 8 |
| B- | 7 |
| C | 6 |
| C- | 5 |
| D | 4 |
| F | 0 |

**SGPA**

```text
SGPA = Sum(credit × grade_point) / Sum(credits)
```

**CGPA**

```text
CGPA = Sum(all subject credit × grade_point values) / Sum(all subject credits)
```

School-record averages are calculated separately from the credit-weighted college GPA calculations.

## Security Considerations

This is an academic/learning project and has not been hardened for storing sensitive real-world personal information. Before using it with real student data, important improvements include:

- Hash passwords with a password-hashing function instead of storing plain-text passwords.
- Remove the hardcoded fallback Flask secret key and require a strong `SECRET_KEY` from the environment.
- Add CSRF protection to forms and configure secure session-cookie settings.
- Disable Flask debug mode outside local development.
- Review input validation and authorization checks for every state-changing operation.

Never commit `.env` files, database connection strings, passwords, API tokens, private keys, or production student data.

## License

This project is available under the MIT License. See [LICENSE](LICENSE).

## Author

**Vishal** — [GitHub](https://github.com/Vishal-gujjar)
