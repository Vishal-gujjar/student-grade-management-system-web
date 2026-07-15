"""
student.py

Defines the Student class.

Responsibilities:
- Create student account
- Verify student login
- Retrieve student information
- Update personal information
- Delete student account

Business calculations are NOT performed here.
"""

from person import Person


class Student(Person):
    """
    Student class derived from Person.
    Handles only student account and personal information.
    """
    def __init__(
        self,
        database_manager,
        student_id=None,
        password="",
        name="",
        father_name="",
        mother_name="",
        date_of_birth="",
        gender="",
        phone="",
        email="",
        address=""
    ):
        super().__init__(
            name=name,
            father_name=father_name,
            mother_name=mother_name,
            date_of_birth=date_of_birth,
            gender=gender,
            phone=phone,
            email=email,
            address=address
        )

        self.db = database_manager
        self.student_id = student_id
        self.password = password


    # ----------------------------------------------------------
    # Account Creation
    # ----------------------------------------------------------
    def create_account(self):
        """
        Creates a new student account.
        Returns
        -------
        student_id : int
        """
        if self.phone_exists(self.phone):
            raise ValueError("Phone number already registered.")

        if self.email_exists(self.email):
            raise ValueError("Email already registered.")

        query = """INSERT INTO students(password, name, father_name, mother_name, date_of_birth, gender, phone, email, address) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        values = (self.password, self.name, self.father_name, self.mother_name, self.date_of_birth, self.gender, self.phone, self.email, self.address)

        self.student_id = self.db.execute_query(query, values)
        return self.student_id


    # ----------------------------------------------------------
    # Authentication
    # ----------------------------------------------------------
    def verify_password(self):
        """
        Verifies student id and password.
        Returns
        -------
        bool
        """
        query = """SELECT student_id FROM students WHERE student_id=%s AND password=%s"""
        result = self.db.fetch_one(query, (self.student_id, self.password))
        return result is not None


    # ----------------------------------------------------------
    # Duplicate Checking
    # ----------------------------------------------------------
    def phone_exists(self, phone):
        query = """SELECT student_id FROM students WHERE phone=%s"""
        return self.db.record_exists(query, (phone,))


    def email_exists(self, email):
        query = """SELECT student_id FROM students WHERE email=%s"""
        return self.db.record_exists(query, (email,))


    # ----------------------------------------------------------
    # Student Information
    # ----------------------------------------------------------
    def load_student(self):
        """
        Loads student details into object.
        Returns
        -------
        dict or None
        """
        query = """SELECT * FROM students WHERE student_id=%s"""
        result = self.db.fetch_one(query, (self.student_id,))
        if result is None:
            return None

        self.password = result["password"]
        self.name = result["name"]
        self.father_name = result["father_name"]
        self.mother_name = result["mother_name"]
        self.date_of_birth = result["date_of_birth"]
        self.gender = result["gender"]
        self.phone = result["phone"]
        self.email = result["email"]
        self.address = result["address"]

        return result


    def get_student_details(self):
        """
        Returns student details as dictionary.
        """
        return self.load_student()


    # ----------------------------------------------------------
    # Update Personal Details
    # ----------------------------------------------------------
    def update_personal_details(self, name, father_name, mother_name, date_of_birth, gender, phone, email, address):
        """
        Updates all personal information.
        """
        existing = self.db.fetch_one("""SELECT student_id FROM students WHERE phone=%s AND student_id<>%s""", (phone, self.student_id))
        if existing:
            raise ValueError("Phone number already in use.")

        existing = self.db.fetch_one("""SELECT student_id FROM students WHERE email=%s AND student_id<>%s""", (email, self.student_id))
        if existing:
            raise ValueError("Email already in use.")

        query = """UPDATE students SET name=%s, father_name=%s, mother_name=%s, date_of_birth=%s, gender=%s, phone=%s, email=%s, address=%s WHERE student_id=%s"""

        values = (name, father_name, mother_name, date_of_birth, gender, phone, email, address, self.student_id)
        self.db.execute_query(query, values)

        self.update_details(name=name, father_name=father_name, mother_name=mother_name, date_of_birth=date_of_birth, gender=gender, phone=phone, email=email, address=address)


    # ----------------------------------------------------------
    # Password
    # ----------------------------------------------------------
    def change_password(self, new_password):
        """
        Changes account password.
        """
        query = """UPDATE students SET password=%s WHERE student_id=%s"""
        self.db.execute_query(query, (new_password, self.student_id))
        self.password = new_password


        # ----------------------------------------------------------
    # Update Account
    # ----------------------------------------------------------
    def update_account(
        self,
        name,
        father_name,
        mother_name,
        date_of_birth,
        gender,
        phone,
        email,
        address,
        password=""
    ):
        """
        Updates personal details and optionally password.
        """

        self.update_personal_details(
            name,
            father_name,
            mother_name,
            date_of_birth,
            gender,
            phone,
            email,
            address
        )

        if password.strip():
            self.change_password(password)




    # ----------------------------------------------------------
    # Delete Student
    # ----------------------------------------------------------
    def delete_student(self):
        try:
            query = """
            DELETE FROM students
            WHERE student_id=%s
            """
            self.db.execute_query(
                query,
                (self.student_id,)
            )
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise


    # ----------------------------------------------------------
    # Utility
    # ----------------------------------------------------------
    def student_exists(self):
        """
        Returns True if student exists.
        """
        query = """SELECT student_id FROM students WHERE student_id=%s"""
        return self.db.record_exists(query, (self.student_id,))


    def __str__(self):
        return (
            f"Student("
            f"student_id={self.student_id}, "
            f"name='{self.name}', "
            f"email='{self.email}')"
        )
    





