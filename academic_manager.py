"""
academic_manager.py -- Handles all academic records and subjects.
Responsibilities
----------------
- Add school record
- Add college record
- Update education records
- Update subjects/courses
- Delete education records
- Delete subjects/courses
- Generate complete student report

This class contains business logic related to academic records. Grade calculations are delegated to GradeManager. Database communication is delegated to DatabaseManager.
"""

from grade_manager import GradeManager

class AcademicManager:
    """
    Handles all education records and subjects.
    """
    SCHOOL_LEVELS = [f"Class {i}" for i in range(1, 13)]
    COLLEGE_DEGREES = {
        "B.Tech": 8,
        "B.E": 8,
        "B.Sc": 6,
        "B.Com": 6,
        "B.A": 6,
        "BCA": 6,
        "BBA": 6,
        "M.Tech": 4,
        "M.Sc": 4,
        "MBA": 4,
        "MCA": 4,
        "M.Com": 4,
        "M.A": 4,
        "PhD": 8
    }

    def __init__(self, database_manager):
        self.db = database_manager



    # ==========================================================
    # Validation
    # ==========================================================
    @classmethod
    def is_valid_school_level(cls, level):
        return level in cls.SCHOOL_LEVELS


    @classmethod
    def is_valid_college_level(cls, level):
        parts = level.split()
        if len(parts) != 3:
            return False

        degree = parts[0]
        sem = parts[1]
        number = parts[2]
        if degree not in cls.COLLEGE_DEGREES:
            return False
        if sem.lower() != "sem":
            return False
        if not number.isdigit():
            return False

        semester = int(number)

        return 1 <= semester <= cls.COLLEGE_DEGREES[degree]



    # ==========================================================
    # Add Academic Record
    # ==========================================================
<<<<<<< HEAD
    def add_school_record(
        self,
        student_id,
        level,
        school_name,
        board,
        academic_year,
        subjects
    ):
        """
        If the level already exists:
            • Add only new subjects.
            • Skip duplicate subjects.
        """

=======
    def add_school_record(self, student_id, level, school_name, board, academic_year, subjects):
        """
        subjects = [("English", "A+"), ("Math", "O")]
        """
>>>>>>> 6fb370682a64f0b37c8df476e173a2b491196b1b
        if not self.is_valid_school_level(level):
            raise ValueError("Invalid school level.")

        try:
<<<<<<< HEAD

            # --------------------------------------------------
            # Does this school record already exist?
            # --------------------------------------------------

            record = self.db.fetch_one(
                """
                SELECT record_id
                FROM education_record
                WHERE student_id=%s
                AND record_type='School'
                AND level=%s
                """,
                (student_id, level)
            )

            if record is None:

                record_id = self._create_record(
                    student_id,
                    "School",
                    level,
                    school_name,
                    board,
                    academic_year
                )

            else:

                record_id = record["record_id"]

            # --------------------------------------------------
            # Existing subjects
            # --------------------------------------------------

            existing = self.db.fetch_all(
                """
                SELECT subject_name
                FROM subject
                WHERE record_id=%s
                """,
                (record_id,)
            )

            existing_subjects = {
                row["subject_name"].lower()
                for row in existing
            }

            added = []
            skipped = []

            # --------------------------------------------------
            # Insert only new subjects
            # --------------------------------------------------

            for subject_name, grade in subjects:

                if subject_name.lower() in existing_subjects:

                    skipped.append(subject_name)

                    continue

                self._insert_subject(
                    record_id,
                    subject_name,
                    3,
                    grade
                )

                existing_subjects.add(subject_name.lower())
                added.append(subject_name)

            self.db.commit()

            return {
                "record_id": record_id,
                "added": added,
                "skipped": skipped
            }
=======
            record_id = self._create_record(student_id, "School", level, school_name, board, academic_year)
            for subject_name, grade in subjects:
                self._insert_subject(record_id, subject_name, 3, grade)
            self.db.commit()
            return record_id
>>>>>>> 6fb370682a64f0b37c8df476e173a2b491196b1b

        except Exception:
            self.db.rollback()
            raise


<<<<<<< HEAD



    def add_college_record(
        self,
        student_id,
        level,
        college_name,
        branch,
        academic_year,
        subjects
    ):
        """
        If the semester already exists:
            • Add only new courses.
            • Skip duplicate courses.
        """

=======
    def add_college_record(self, student_id, level, college_name, branch, academic_year, subjects):
        """
        subjects = [("Python", 4, "A+"), ("Physics", 3, "O")]
        """
>>>>>>> 6fb370682a64f0b37c8df476e173a2b491196b1b
        if not self.is_valid_college_level(level):
            raise ValueError("Invalid college level.")

        try:
<<<<<<< HEAD

            record = self.db.fetch_one(
                """
                SELECT record_id
                FROM education_record
                WHERE student_id=%s
                AND record_type='College'
                AND level=%s
                """,
                (student_id, level)
            )

            if record is None:
                record_id = self._create_record(
                    student_id,
                    "College",
                    level,
                    college_name,
                    branch,
                    academic_year
                )
            else:
                record_id = record["record_id"]

            existing = self.db.fetch_all(
                """
                SELECT subject_name
                FROM subject
                WHERE record_id=%s
                """,
                (record_id,)
            )

            existing_courses = {
                row["subject_name"].lower()
                for row in existing
            }

            added = []
            skipped = []

            for course_name, credit, grade in subjects:
                if course_name.lower() in existing_courses:
                    skipped.append(course_name)
                    continue

                self._insert_subject(
                    record_id,
                    course_name,
                    credit,
                    grade
                )
                existing_courses.add(course_name.lower())
                added.append(course_name)

            self.db.commit()

            return {
                "record_id":record_id,
                "added":added,
                "skipped":skipped
            }
=======
            record_id = self._create_record(student_id, "College", level, college_name, branch, academic_year)
            for subject_name, credit, grade in subjects:
                self._insert_subject(record_id, subject_name, credit, grade)

            self.db.commit()
            return record_id
>>>>>>> 6fb370682a64f0b37c8df476e173a2b491196b1b

        except Exception:
            self.db.rollback()
            raise


    def add_subject_to_record(self, record_id, subject_name, grade, credit=None):
        """
        Add a new subject/course to an existing academic record.
        School: Credit is automatically 3.
        College: Credit must be provided by the user.
        """

        # Fetch record information
        record = self.db.fetch_one(""" SELECT record_type FROM education_record WHERE record_id=%s""", (record_id,))
        if record is None:
            raise ValueError("Academic record not found.")

        record_type = record["record_type"]

        # School subjects always have 3 credits
        if record_type == "School":
            credit = 3

        else:
            if credit is None:
                raise ValueError("Credit is required for college courses.")
            if credit <= 0:
                raise ValueError("Credit must be greater than zero.")

        try:
            self._insert_subject(record_id, subject_name, credit, grade)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise



    # ==========================================================
    # Internal Insert Helpers
    # ==========================================================
    def _create_record(self, student_id, record_type, level, organization, category, academic_year):
        query = """INSERT INTO education_record(student_id, record_type, level, organization, category, academic_year) VALUES(%s,%s,%s,%s,%s,%s)"""

        return self.db.execute_query(query, (student_id, record_type, level, organization, category, academic_year))


    def _insert_subject(self, record_id, subject_name, credit, grade):
        if not GradeManager.is_valid_grade(grade):
            raise ValueError("Invalid grade.")

        query = """INSERT INTO subject(record_id, subject_name, credit, grade) VALUES(%s,%s,%s,%s)"""
        self.db.execute_query(query, (record_id, subject_name, credit, grade.upper()))



    # ==========================================================
    # Update
    # ==========================================================
    def update_education_record(self, record_id, organization, category, academic_year):
        query = """UPDATE education_record SET organization=%s, category=%s, academic_year=%s WHERE record_id=%s"""

        self.db.execute_query(query, (organization, category, academic_year, record_id))


    def update_subject(self, subject_id, subject_name, credit, grade):
        if not GradeManager.is_valid_grade(grade):
            raise ValueError("Invalid grade.")

        query = """UPDATE subject SET subject_name=%s, credit=%s, grade=%s WHERE subject_id=%s"""
        self.db.execute_query(query, (subject_name, credit, grade.upper(), subject_id))


<<<<<<< HEAD
    def update_school_record(
        self,
        record_id,
        school_name,
        board,
        academic_year,
        subjects
    ):
        """
        Update a complete school record.
        subjects is a list of dictionaries:

        Existing:
        {
            "id": 5,
            "name": "Physics",
            "grade": "A"
        }

        Deleted:
        {
            "id": 5,
            "deleted": True
        }

        New:
        {
            "name": "Biology",
            "grade": "A+"
        }
        """
        try:
            # ---------------------------------------
            # Update school information
            # ---------------------------------------
            self.update_education_record(
                record_id,
                school_name,
                board,
                academic_year
            )
            # ---------------------------------------
            # Process subjects
            # ---------------------------------------
            for subject in subjects:
                # ----------------------------
                # Delete
                # ----------------------------
                if subject.get("deleted"):
                    self.delete_subject(
                        subject["id"]
                    )
                    continue
                # ----------------------------
                # Existing subject
                # ----------------------------
                if subject.get("id"):
                    self.update_subject(
                        subject["id"],
                        subject["name"],
                        3,
                        subject["grade"]
                    )
                # ----------------------------
                # New subject
                # ----------------------------
                else:
                    self.add_subject_to_record(
                        record_id,
                        subject["name"],
                        subject["grade"]
                    )
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

    
    def update_college_record(
        self,
        record_id,
        college_name,
        branch,
        academic_year,
        courses
    ):
        """
        Update a complete college semester.
        """

        try:

            # ---------------------------------------
            # Update semester information
            # ---------------------------------------

            self.update_education_record(
                record_id,
                college_name,
                branch,
                academic_year
            )

            # ---------------------------------------
            # Process courses
            # ---------------------------------------

            for course in courses:

                # Delete existing course
                if course.get("deleted"):

                    self.delete_subject(
                        course["id"]
                    )

                    continue

                # Update existing course
                if course.get("id"):

                    self.update_subject(

                        course["id"],

                        course["name"],

                        int(course["credit"]),

                        course["grade"]

                    )

                # Add new course
                else:

                    self.add_subject_to_record(

                        record_id,

                        course["name"],

                        course["grade"],

                        int(course["credit"])

                    )

            self.db.commit()

        except Exception:

            self.db.rollback()

            raise

=======
>>>>>>> 6fb370682a64f0b37c8df476e173a2b491196b1b

    # ==========================================================
    # Delete
    # ==========================================================
    def delete_record(self, record_id):
<<<<<<< HEAD
        try:
            self.db.execute_query(
                """
                DELETE FROM education_record
                WHERE record_id=%s
                """,
                (record_id,)
            )
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise
=======
        self.db.execute_query("""DELETE FROM education_record WHERE record_id=%s""", (record_id,))
>>>>>>> 6fb370682a64f0b37c8df476e173a2b491196b1b


    def delete_subject(self, subject_id):
        self.db.execute_query("""DELETE FROM subject WHERE subject_id=%s""", (subject_id,))



    # ==========================================================
    # Fetch
    # ==========================================================
    def get_student_records(self, student_id):
        return self.db.fetch_all("""SELECT * FROM education_record WHERE student_id=%s ORDER BY record_id""", (student_id,))


    def get_subjects(self, record_id):
        return self.db.fetch_all("""SELECT * FROM subject WHERE record_id=%s ORDER BY subject_name""", (record_id,))
    

<<<<<<< HEAD
    def get_school_record(self, record_id):

        record = self.db.fetch_one(
            """
            SELECT *
            FROM education_record
            WHERE record_id=%s
            AND record_type='School'
            """,
            (record_id,)
        )

        if record is None:
            return None

        subjects = self.get_subjects(record_id)

        return {
            "record_id": record["record_id"],
            "level": record["level"],
            "school_name": record["organization"],
            "board": record["category"],
            "academic_year": record["academic_year"],
            "subjects":[
                {
                    "subject_id": subject["subject_id"],
                    "name": subject["subject_name"],
                    "grade": subject["grade"]
                }
                for subject in subjects
            ]
        }
    

    def get_college_record(self, record_id):
        record = self.db.fetch_one(
            """
            SELECT *
            FROM education_record
            WHERE record_id=%s
            AND record_type='College'
            """,
            (record_id,)
        )

        if record is None:
            return None

        courses = self.get_subjects(record_id)

        return {
            "record_id": record["record_id"],
            "level": record["level"],
            "college_name": record["organization"],
            "branch": record["category"],
            "academic_year": record["academic_year"],
            "courses":[
                {
                    "subject_id": course["subject_id"],
                    "name": course["subject_name"],
                    "credit": course["credit"],
                    "grade": course["grade"]
                }
                for course in courses
            ]
        }


=======
>>>>>>> 6fb370682a64f0b37c8df476e173a2b491196b1b
    def select_record(self, student_id):
        """
        Display all academic records of a student and
        return the selected record dictionary.
        """
        records = self.get_student_records(student_id)
        if not records:
            print("\nNo academic records found.")
            return None

        print("\n========== Academic Records ==========")
        for index, record in enumerate(records, start=1):
            print(
                f"{index}. "
                f"{record['record_type']} | "
                f"{record['level']} | "
                f"{record['organization']}"
            )

        while True:
            try:
                choice = int(input("\nChoose Record : "))
                if 1 <= choice <= len(records):
                    return records[choice - 1]
                print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a valid number.")


    def select_subject(self, record_id):
        """
        Display all subjects/courses of a record and
        return the selected subject dictionary.
        """
        subjects = self.get_subjects(record_id)
        if not subjects:
            print("\nNo subjects/courses found.")
            return None

        print("\n========== Subjects / Courses ==========")
        for index, subject in enumerate(subjects, start=1):
            print(
                f"{index}. "
                f"{subject['subject_name']} "
                f"(Credit: {subject['credit']}, "
                f"Grade: {subject['grade']})"
            )

        while True:
            try:
                choice = int(input("\nChoose Subject/Course : "))
                if 1 <= choice <= len(subjects):
                    return subjects[choice - 1]
                print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a valid number.")



    # ==========================================================
    # Report
    # ==========================================================
    def generate_student_report(self, student_id):
<<<<<<< HEAD

        from student import Student

        # ---------------------------------------
        # Load Student
        # ---------------------------------------

        student = Student(
            database_manager=self.db,
            student_id=student_id
        )

        student.load_student()

        # ---------------------------------------
        # Report Structure
        # ---------------------------------------

        report = {
            "student": student,

            "statistics": {
                "degree_count": 0,
                "school_count": 0,
                "total_courses": 0,
                "overall_cgpa": 0
            },

            "school": [],
            "college": []
        }

        records = self.get_student_records(student_id)

        records.sort(
            key=lambda record:
            (
                0 if record["record_type"] == "School" else 1,
                record["level"]
            )
        )

        degree_map = {}
        cgpa_subjects = []

        # =====================================================
        # Read Every Record
        # =====================================================

        for record in records:

            subjects = self.get_subjects(record["record_id"])
            report["statistics"]["total_courses"] += len(subjects)

            # --------------------------------------------
            # School
            # --------------------------------------------

            if record["record_type"] == "School":
                grades = [
                    subject["grade"]
                    for subject in subjects
                ]

                report["school"].append(
                    {
                        "record_id": record["record_id"],
                        "level": record["level"],
                        "organization": record["organization"],
                        "category": record["category"],
                        "academic_year": record["academic_year"],
                        "grade": GradeManager.calculate_average(grades),
                        "subjects":[
                            {
                                "name":subject["subject_name"],
                                "grade":subject["grade"]
                            }
                            for subject in subjects
                        ]
                    }
                )

                continue

            # --------------------------------------------
            # College
            # --------------------------------------------

            degree = record["level"].split()[0]

            if degree not in degree_map:
                degree_map[degree] = {
                    "degree":degree,
                    "college":record["organization"],
                    "branch":record["category"],
                    "total_credit":0,
                    "cgpa":0,
                    "semesters":[],
                    "_subjects":[]
                }

            total_credit = sum(
                subject["credit"]
                for subject in subjects
            )

            sgpa = GradeManager.calculate_sgpa(subjects)
            degree_map[degree]["total_credit"] += total_credit
            degree_map[degree]["_subjects"].append(subjects)
            cgpa_subjects.append(subjects)

            degree_map[degree]["semesters"].append(
                {
                    "record_id": record["record_id"],
                    "level":record["level"],
                    "academic_year":record["academic_year"],
                    "total_credit":total_credit,
                    "sgpa":sgpa,

                    "subjects":[
                        {
                            "name":subject["subject_name"],
                            "credit":subject["credit"],
                            "grade":subject["grade"]
                        }
                        for subject in subjects
                    ]
                }
            )

        # =====================================================
        # Degree Summary
        # =====================================================

        for degree in degree_map.values():

            degree["cgpa"] = GradeManager.calculate_cgpa(
                degree["_subjects"]
            )

            degree["semesters"].sort(
                key=lambda semester:
                int(semester["level"].split()[-1])
            )

            del degree["_subjects"]
            report["college"].append(degree)

        # =====================================================
        # Statistics
        # =====================================================

        report["statistics"]["degree_count"] = len(
            report["college"]
        )

        report["statistics"]["school_count"] = len(
            report["school"]
        )

        report["statistics"]["overall_cgpa"] = GradeManager.calculate_cgpa(
            cgpa_subjects
        )

        return report
=======
        school_records = []
        college_records = {}

        records = self.get_student_records(student_id)   
        records.sort(key=lambda record: (0 if record["record_type"] == "School" else 1, record["level"]))

        for record in records:
            subjects = self.get_subjects(record["record_id"])
            grades = [subject["grade"] for subject in subjects]
            record_data = {
                "record": record,
                "subjects": subjects
            }

            # School
            if record["record_type"] == "School":
                record_data["average"] = GradeManager.calculate_average(grades)
                school_records.append(record_data)

            # College
            else:
                record_data["sgpa"] = GradeManager.calculate_sgpa(subjects)
                record_data["total_credits"] = sum(subject["credit"] for subject in subjects)

                degree = record["level"].split()[0]
                if degree not in college_records:
                    college_records[degree] = {
                        "records": [],
                        "all_subjects": [],
                        "total_credits": 0
                    }

                college_records[degree]["records"].append(record_data)
                college_records[degree]["all_subjects"].append(subjects)
                college_records[degree]["total_credits"] += (record_data["total_credits"])

        # Calculate Degree-wise CGPA
        for degree in college_records:
            college_records[degree]["cgpa"] = (GradeManager.calculate_cgpa(college_records[degree]["all_subjects"]))

            # Sort semesters numerically
            college_records[degree]["records"].sort(key=lambda item: int(item["record"]["level"].split()[-1]))

        return {
            "school": school_records,
            "college": college_records
        }






    
>>>>>>> 6fb370682a64f0b37c8df476e173a2b491196b1b
