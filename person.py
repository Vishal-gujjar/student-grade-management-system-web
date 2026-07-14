"""
person.py

Defines the base Person class used by the Student class.

This class stores only personal information.
It does not contain any database logic.
"""


class Person:
    """
    Base class representing a person's personal information.
    """
    def __init__(
        self,
        name="",
        father_name="",
        mother_name="",
        date_of_birth="",
        gender="",
        phone="",
        email="",
        address=""
    ):
        self.name = name
        self.father_name = father_name
        self.mother_name = mother_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone = phone
        self.email = email
        self.address = address


    # ---------------------------------------------------------
    # Getters
    # ---------------------------------------------------------
    def get_name(self):
        return self.name

    def get_father_name(self):
        return self.father_name

    def get_mother_name(self):
        return self.mother_name

    def get_date_of_birth(self):
        return self.date_of_birth

    def get_gender(self):
        return self.gender

    def get_phone(self):
        return self.phone

    def get_email(self):
        return self.email

    def get_address(self):
        return self.address


    # ---------------------------------------------------------
    # Setters
    # ---------------------------------------------------------
    def set_name(self, name):
        self.name = name

    def set_father_name(self, father_name):
        self.father_name = father_name

    def set_mother_name(self, mother_name):
        self.mother_name = mother_name

    def set_date_of_birth(self, date_of_birth):
        self.date_of_birth = date_of_birth

    def set_gender(self, gender):
        self.gender = gender

    def set_phone(self, phone):
        self.phone = phone

    def set_email(self, email):
        self.email = email

    def set_address(self, address):
        self.address = address


    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------
    def to_dict(self):
        """
        Returns all personal information as a dictionary.
        """
        return {
            "name": self.name,
            "father_name": self.father_name,
            "mother_name": self.mother_name,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
        }

    def update_details(
        self,
        name=None,
        father_name=None,
        mother_name=None,
        date_of_birth=None,
        gender=None,
        phone=None,
        email=None,
        address=None
    ):
        """
        Update one or more personal details.
        Only the provided values are updated.
        """
        if name is not None:
            self.name = name

        if father_name is not None:
            self.father_name = father_name

        if mother_name is not None:
            self.mother_name = mother_name

        if date_of_birth is not None:
            self.date_of_birth = date_of_birth

        if gender is not None:
            self.gender = gender

        if phone is not None:
            self.phone = phone

        if email is not None:
            self.email = email

        if address is not None:
            self.address = address

    def display(self):
        """
        Prints the personal information.
        """
        print("\n========== Personal Information ==========")
        print(f"Name           : {self.name}")
        print(f"Father Name    : {self.father_name}")
        print(f"Mother Name    : {self.mother_name}")
        print(f"Date of Birth  : {self.date_of_birth}")
        print(f"Gender         : {self.gender}")
        print(f"Phone          : {self.phone}")
        print(f"Email          : {self.email}")
        print(f"Address        : {self.address}")
        print("==========================================")