# Student Grade Management System

A command-line based **Student Grade Management System** developed using **Python**, **MySQL**, and **Object-Oriented Programming (OOP)**. The project manages a student's complete academic journey—from school education to multiple college degrees—through a single student account.

---

## Features

### Student Management

* Create a student account
* Secure login using Student ID and password
* Store and update personal details
* Delete student account

### Academic Record Management

* Add multiple school academic records
* Add multiple college academic records
* Add additional subjects/courses to existing academic records
* Update academic records
* Update subjects/courses
* Delete academic records
* Delete subjects/courses

### Smart User Interface

* No manual Record ID entry
* No manual Subject ID entry
* Numbered selection menus for records and subjects
* Update only the selected field instead of re-entering all information
* Consistent menu-driven workflow for Add, Update, Delete, and Report operations

### Report Generation

* Complete student profile
* School education displayed before college education
* Subjects/Courses listed for every record
* School average grade calculation
* Semester GPA (SGPA)
* Degree-wise CGPA (each degree has its own CGPA)
* Semester credit summary
* Degree credit summary

---

## Project Structure

```text
Student_Grade_Manager/
│
├── main.py
├── database.py
├── person.py
├── student.py
├── academic_manager.py
├── grade_manager.py
├── sql/
│   └── schema.sql
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Technologies Used

* Python 3
* MySQL
* mysql-connector-python
* Object-Oriented Programming (OOP)

---

## Database

Database Name

```text
student_grade_manager
```

Tables

* students
* education_record
* subject

Database schema is available in:

```text
sql/schema.sql
```

---

## Installation

### Clone the Repository

```bash
git clone <repository-url>
```

or download the ZIP.

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Database

Run the SQL script:

```sql
SOURCE sql/schema.sql;
```

### Configure Database

Update the default values inside `database.py`:

```python
host="localhost"
user="root"
password=""
database="student_grade_manager"
```

Replace them with your own MySQL credentials.

### Run the Project

```bash
python main.py
```

---

## Main Menu

```text
1. Create Account
2. Add Academic Record
3. Update
4. Delete
5. Student Report
6. Exit
```

---

## Grade System

| Grade | Grade Point |
| ----- | ----------: |
| A+    |          10 |
| A     |          10 |
| A-    |           9 |
| B     |           8 |
| B-    |           7 |
| C     |           6 |
| C-    |           5 |
| D     |           4 |
| F     |           0 |

Grade points are calculated in Python and are not stored in the database.

---

## School Academic Records

* Class 1 – Class 12
* Credit automatically assigned as 3
* Store:

  * School Name
  * Board
  * Academic Year
  * Subjects
  * Grades

---

## College Academic Records

Supports multiple degrees, for example:

* B.Tech
* B.E.
* B.Sc.
* MBA
* M.Tech
* MCA
* PhD

Each semester stores:

* College Name
* Branch
* Academic Year
* Courses
* Credits
* Grades

---

## Student Report

The generated report includes:

* Personal Details
* School Education
* College Education
* Subject/Course Details
* School Average
* Semester GPA (SGPA)
* Degree-wise CGPA
* Semester Total Credits
* Degree Total Credits Completed

---

## Requirements

```text
mysql-connector-python
```

---

## .gitignore

```text
__pycache__/
*.pyc
.vscode/
.idea/
.env
```

---

## Future Improvements

Possible future enhancements include:

* School marks support in addition to grades
* PDF report generation
* Export report to Excel
* Search students by name
* Admin dashboard
* Graphical User Interface (GUI)
* Web version using Flask or Django

---

## Author

Vishal Gurjar

B.Tech Engineering Physics, IIT Hyderabad

Python • MySQL • Object-Oriented Programming
