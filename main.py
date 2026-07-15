"""
main.py
Entry point for the Student Grade Management System.

Responsibilities
----------------
- Display menus
- Take user input
- Call Student, AcademicManager and GradeManager methods
"""

from copy import error

from database import DatabaseManager
from student import Student
from academic_manager import AcademicManager


class StudentGradeManagementSystem:
    def __init__(self):
        self.db = DatabaseManager()
        self.academic_manager = AcademicManager(self.db)


    # ==========================================================
    # Main Menu
    # ==========================================================
    def run(self):
        while True:
            print("\n" + "=" * 55)
            print("      STUDENT GRADE MANAGEMENT SYSTEM")
            print("=" * 55)
            print("1. Create Account")
            print("2. Add Academic Record")
            print("3. Update")
            print("4. Delete")
            print("5. Student Report")
            print("6. Exit")
            print("=" * 55)

            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.add_academic_record()
            elif choice == "3":
                self.update_menu()
            elif choice == "4":
                self.delete_menu()
            elif choice == "5":
                self.student_report()
            elif choice == "6":
                print("\nThank you for using Student Grade Management System.")
                break
            else:
                print("Invalid choice.")


    # ==========================================================
    # Authentication
    # ==========================================================
    def get_student(self, student_id):
        student = Student(
            database_manager=self.db,
            student_id=student_id
        )

        student.load_student()
        return student


    def login_student(self, student_id, password):
        student = Student(
            database_manager=self.db,
            student_id=student_id,
            password=password
        )

        if not student.verify_password():
            raise ValueError("Invalid Student ID or Password.")

        student.load_student()

        return student


    def authenticate(self):
        try:
            student_id = int(input("Student ID : "))
        except ValueError:
            print("Invalid Student ID.")
            return None

        password = input("Password : ")

        try:
            return self.login_student(student_id, password)
        except Exception:
            print("Invalid Student ID or Password.")
            return None


    # ==========================================================
    # Create Account
    # ==========================================================
    def create_student_account(
        self,
        name,
        father_name,
        mother_name,
        dob,
        gender,
        phone,
        email,
        address,
        password
    ):

        student = Student(
            database_manager=self.db,
            password=password,
            name=name,
            father_name=father_name,
            mother_name=mother_name,
            date_of_birth=dob,
            gender=gender,
            phone=phone,
            email=email,
            address=address
        )

        return student.create_account()


    def create_account(self):
        print("\nCreate Student Account")
        name = input("Name : ")
        father = input("Father Name : ")
        mother = input("Mother Name : ")
        dob = input("Date of Birth (YYYY-MM-DD) : ")
        gender = input("Gender (Male/Female/Other) : ")
        phone = input("Phone : ")
        email = input("Email : ")
        address = input("Address : ")

        password = input("Password : ")
        confirm = input("Confirm Password : ")
        if password != confirm:
            print("Passwords do not match.")
            return

        try:
            student_id = self.create_student_account(
                name,
                father,
                mother,
                dob,
                gender,
                phone,
                email,
                address,
                password
            )

            print("\nAccount created successfully.")
            print(f"Student ID : {student_id}")

        except Exception as error:
            print(error)


    # ==========================================================
    # Add Academic Record
    # ==========================================================
    def create_school_record(
        self,
        student_id,
        level,
        school_name,
        board,
        academic_year,
        subjects
    ):
        return self.academic_manager.add_school_record(
            student_id,
            level,
            school_name,
            board,
            academic_year,
            subjects
        )
    


    def create_college_record(
        self,
        student_id,
        level,
        college_name,
        branch,
        academic_year,
        subjects
    ):
        return self.academic_manager.add_college_record(
            student_id,
            level,
            college_name,
            branch,
            academic_year,
            subjects
        )



    def get_student_report(self, student_id):
        return self.academic_manager.generate_student_report(
            student_id
        )


    def get_school_record(self, record_id):
        return self.academic_manager.get_school_record(
            record_id
        )
    
    def get_college_record(self, record_id):
        return self.academic_manager.get_college_record(
            record_id
        )
    
    def get_student_records(self, student_id):
        return self.academic_manager.get_student_records(
            student_id
        )


    def add_academic_record(self):
        student = self.authenticate()
        if student is None:
            return

        print("\n1. School Record")
        print("2. College Record")
        choice = input("Choose : ")

        try:
            if choice == "1":
                print("\nValid Levels Like: Class 10")
                level = input("\nLevel : ")
                school = input("School Name : ")
                board = input("Board : ")
                year = input("Academic Year : ")

                count = int(input("Number of Subjects : "))
                subjects = []
                for i in range(count):
                    print(f"\nSubject {i+1}")
                    subject = input("Subject Name : ")
                    grade = input("Grade : ")
                    subjects.append((subject, grade))

                self.academic_manager.add_school_record(student.student_id, level, school, board, year, subjects)

                print("\nSchool record added successfully.")


            elif choice == "2":
                print("\nExamples: Degree(B.Tech, B.E, B.Sc, B.Com, B.A, BCA, BBA, M.Tech, M.Sc, MBA, MCA, M.Com, M.A, PhD) 'Sem' semester_number")
                level = input("\nLevel : ")
                college = input("College Name : ")
                branch = input("Branch : ")
                year = input("Academic Year : ")

                count = int(input("Number of Courses : "))
                subjects = []
                for i in range(count):
                    print(f"\nCourse {i+1}")
                    name = input("Course Name : ")
                    credit = int(input("Credit : "))
                    grade = input("Grade : ")
                    subjects.append((name, credit, grade))

                self.academic_manager.add_college_record(student.student_id, level, college, branch, year, subjects)

                print("\nCollege record added successfully.")

            else:
                print("Invalid option.")

        except Exception as error:
            print(error)


    # ==========================================================
    # Update
    # ==========================================================
    def update_student_account(
        self,
        student_id,
        name,
        father_name,
        mother_name,
        dob,
        gender,
        phone,
        email,
        address,
        password=""
    ):
        student = Student(
            database_manager=self.db,
            student_id=student_id
        )

        student.load_student()

        student.update_account(
            name,
            father_name,
            mother_name,
            dob,
            gender,
            phone,
            email,
            address,
            password
        )

    def update_school_record(
        self,
        record_id,
        school_name,
        board,
        academic_year,
        subjects
    ):

        self.academic_manager.update_school_record(
            record_id,
            school_name,
            board,
            academic_year,
            subjects
        )


    def update_college_record(
        self,
        record_id,
        college_name,
        branch,
        academic_year,
        courses
    ):

        self.academic_manager.update_college_record(
            record_id,
            college_name,
            branch,
            academic_year,
            courses
        )

    def delete_record(self, record_id):
        self.academic_manager.delete_record(
            record_id
        )

    def delete_student(self, student_id):
        student = self.get_student(student_id)
        student.delete_student()


    def update_menu(self):
        student = self.authenticate()
        if student is None:
            return

        while True:
            print("\nUpdate Menu")
            print("1. Update Personal Details")
            print("2. Update Academic Record")
            print("3. Update Subject/Course")
            print("4. Add Subject/Course")
            print("5. Back")

            choice = input("Choice : ")
            try:
                # --------------------------------------------------
                # Personal Details
                # --------------------------------------------------
                if choice == "1":

                    print("\nWhich field do you want to update?")
                    print("1. Name")
                    print("2. Father Name")
                    print("3. Mother Name")
                    print("4. Date of Birth")
                    print("5. Gender")
                    print("6. Phone")
                    print("7. Email")
                    print("8. Address")
                    field = input("Choice : ")

                    name = student.name
                    father = student.father_name
                    mother = student.mother_name
                    dob = student.date_of_birth
                    gender = student.gender
                    phone = student.phone
                    email = student.email
                    address = student.address

                    if field == "1":
                        name = input("New Name : ")
                    elif field == "2":
                        father = input("New Father Name : ")
                    elif field == "3":
                        mother = input("New Mother Name : ")
                    elif field == "4":
                        dob = input("New Date of Birth : ")
                    elif field == "5":
                        gender = input("New Gender : ")
                    elif field == "6":
                        phone = input("New Phone : ")
                    elif field == "7":
                        email = input("New Email : ")
                    elif field == "8":
                        address = input("New Address : ")
                    else:
                        print("Invalid choice.")
                        continue

                    student.update_personal_details(name, father, mother, dob, gender, phone, email, address)

                    print("\nPersonal details updated successfully.")


                # --------------------------------------------------
                # Academic Record
                # --------------------------------------------------
                elif choice == "2":

                    record = self.academic_manager.select_record(student.student_id)
                    if record is None:
                        continue

                    print("\nCurrent Record")
                    print(f"Organization : {record['organization']}")
                    print(f"Category     : {record['category']}")
                    print(f"Academic Year: {record['academic_year']}")

                    print("\nWhich field do you want to update?")
                    print("1. Organization")
                    print("2. Category")
                    print("3. Academic Year")

                    field = input("Choice : ")
                    organization = record["organization"]
                    category = record["category"]
                    year = record["academic_year"]

                    if field == "1":
                        organization = input("New Organization : ")
                    elif field == "2":
                        category = input("New Category : ")
                    elif field == "3":
                        year = input("New Academic Year : ")
                    else:
                        print("Invalid choice.")
                        continue

                    self.academic_manager.update_education_record(record["record_id"], organization, category, year)

                    print("\nAcademic record updated successfully.")


                # --------------------------------------------------
                #Subject / Course
                # --------------------------------------------------
                elif choice == "3":

                    record = self.academic_manager.select_record(student.student_id)
                    if record is None:
                        continue
                    subject = self.academic_manager.select_subject(record["record_id"])
                    if subject is None:
                        continue

                    print("\nCurrent Subject")
                    print(f"Name   : {subject['subject_name']}")
                    print(f"Credit : {subject['credit']}")
                    print(f"Grade  : {subject['grade']}")

                    print("\nWhich field do you want to update?")
                    print("1. Subject Name")
                    print("2. Credit")
                    print("3. Grade")

                    field = input("Choice : ")
                    name = subject["subject_name"]
                    credit = subject["credit"]
                    grade = subject["grade"]

                    if field == "1":
                        name = input("New Subject Name : ")
                    elif field == "2":
                        credit = int(input("New Credit : "))
                    elif field == "3":
                        grade = input("New Grade : ")
                    else:
                        print("Invalid choice.")
                        continue

                    self.academic_manager.update_subject(subject["subject_id"], name, credit, grade)

                    print("\nSubject updated successfully.")


                # --------------------------------------------------
                # Add Subject / Course
                # --------------------------------------------------
                elif choice == "4":

                    record = self.academic_manager.select_record(student.student_id)
                    if record is None:
                        continue
                
                    print(f"\nSelected Record : {record['level']}")
                    subject_name = input("Subject/Course Name : ")

                    grade = input("Grade : ")
                    if record["record_type"] == "School":
                        self.academic_manager.add_subject_to_record(record["record_id"], subject_name, grade)
                    else:
                        credit = int(input("Credit : "))
                        self.academic_manager.add_subject_to_record(record["record_id"], subject_name, grade, credit)

                    print("\nSubject/Course added successfully.")


                # --------------------------------------------------
                # Back
                # --------------------------------------------------
                elif choice == "5":
                    break

                else:
                    print("Invalid choice.")

            except Exception as error:
                print(error)

    # ==========================================================
    # Delete
    # ==========================================================

    def delete_menu(self):
        student = self.authenticate()
        if student is None:
            return

        while True:

            print("\nDelete Menu")
            print("1. Delete Student")
            print("2. Delete School/College Record")
            print("3. Delete Subject/Course")
            print("4. Back")

            choice = input("Choice : ")
            try:
                # ------------------------------------------
                # Delete Student
                # ------------------------------------------
                if choice == "1":
                    confirm = input("Are you sure? (YES to confirm): ")

                    if confirm == "YES":
                        student.delete_student()
                        print("\nStudent deleted successfully.")
                        # Student no longer exists
                        break


                # ------------------------------------------
                # Delete Academic Record
                # ------------------------------------------
                elif choice == "2":
                    record = self.academic_manager.select_record(student.student_id)
                    if record is None:
                        continue

                    self.academic_manager.delete_record(record["record_id"])
                    print("\nAcademic record deleted successfully.")


                # ------------------------------------------
                # Delete Subject / Course
                # ------------------------------------------
                elif choice == "3":
                    record = self.academic_manager.select_record(student.student_id)
                    if record is None:
                        continue

                    subject = self.academic_manager.select_subject(record["record_id"])
                    if subject is None:
                        continue

                    self.academic_manager.delete_subject(subject["subject_id"])
                    print("\nSubject/Course deleted successfully.")


                # ------------------------------------------
                # Back
                # ------------------------------------------
                elif choice == "4":
                    break

                else:
                    print("Invalid choice.")

            except Exception as error:
                print(error)


    # ==========================================================
    # Student Report
    # ==========================================================
    def student_report(self):
        student = self.authenticate()
        if student is None:
            return

        report = self.academic_manager.generate_student_report(student.student_id)


        # --------------------------------------------------
        # Personal Details
        # --------------------------------------------------
        print("\n" + "=" * 60)
        print("PERSONAL DETAILS")
        print("=" * 60)
        student.display()


        # --------------------------------------------------
        # School Education
        # --------------------------------------------------
        if report["school"]:
            print("\n" + "=" * 60)
            print("SCHOOL EDUCATION")
            print("=" * 60)

            for item in report["school"]:
                record = item["record"]
                print("\n" + "-" * 60)
                print(f"Level          : {record['level']}")
                print(f"School         : {record['organization']}")
                print(f"Board          : {record['category']}")
                print(f"Academic Year  : {record['academic_year']}")

                print("\nSubjects")
                for index, subject in enumerate(item["subjects"], start=1):
                    print(
                        f"{index:>2}. "
                        f"{subject['subject_name']:<25}"
                        f"Grade : {subject['grade']}"
                    )

                print(f"\nOverall Grade : {item['average']}")


        # --------------------------------------------------
        # College Education
        # --------------------------------------------------
        if report["college"]:
            print("\n" + "=" * 60)
            print("COLLEGE EDUCATION")
            print("=" * 60)

            for degree, degree_data in report["college"].items():
                print("\n" + "#" * 60)
                print(f"{degree}")
                print("#" * 60)

                for item in degree_data["records"]:
                    record = item["record"]
                    print("\n" + "-" * 60)
                    print(f"Semester       : {record['level']}")
                    print(f"College        : {record['organization']}")
                    print(f"Branch         : {record['category']}")
                    print(f"Academic Year  : {record['academic_year']}")
                    print("\nCourses")

                    for index, subject in enumerate(item["subjects"], start=1):
                        print(
                            f"{index:>2}. "
                            f"{subject['subject_name']:<25}"
                            f"Credit : {subject['credit']:<2}"
                            f"Grade : {subject['grade']}"
                        )

                    print(f"\nTotal Credits : {item['total_credits']}")
                    print(f"SGPA          : {item['sgpa']}")

                print("\n" + "-" * 60)
                print(
                    f"Total Credits Completed : "
                    f"{degree_data['total_credits']}"
                )
                print(f"{degree} CGPA            : {degree_data['cgpa']}")
                print("-" * 60)




if __name__ == "__main__":
    system = StudentGradeManagementSystem()
    try:
        system.run()
    finally:
        system.db.disconnect()

     