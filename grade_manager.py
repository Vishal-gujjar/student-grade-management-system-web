"""
grade_manager.py
Handles all grade-related calculations.

Responsibilities:
- Grade to Grade Point conversion
- School Average calculation
- College SGPA calculation
- Overall CGPA calculation

This class performs calculations only. It does not communicate with the database.
"""


class GradeManager:
    """
    Performs all academic grade calculations.
    """
    GRADE_POINTS = {
        "A+": 10,
        "A": 10,
        "A-": 9,
        "B": 8,
        "B-": 7,
        "C": 6,
        "C-": 5,
        "D": 4,
        "F": 0
    }


    # ---------------------------------------------------------
    # Grade Point
    # ---------------------------------------------------------
    @classmethod
    def grade_to_point(cls, grade):
        """
        Convert a grade into its grade point.
        Parameters
        ----------
        grade : str
        Returns
        -------
        int
        """
        grade = grade.strip().upper()
        if grade not in cls.GRADE_POINTS:
            raise ValueError(f"Invalid grade: {grade}")

        return cls.GRADE_POINTS[grade]


    # ---------------------------------------------------------
    # School Average
    # ---------------------------------------------------------
    @classmethod
    def calculate_average(cls, grades):
        """
        Calculates the average grade point for a school record.
        Parameters
        ----------
        grades : list[str]
        Returns
        -------
        float
        """
        if not grades:
            return 0.0
        total = sum(cls.grade_to_point(grade) for grade in grades)

        return round(total / len(grades), 2)

    # ---------------------------------------------------------
    # SGPA
    # ---------------------------------------------------------
    @classmethod
    def calculate_sgpa(cls, subjects):
        """
        Calculates Semester GPA.
        Parameters
        ----------
        subjects : list
        Each item may be: {"credit": int, "grade": str} or (credit, grade)
        Returns
        -------
        float
        """
        if not subjects:
            return 0.0

        total_credit_points = 0
        total_credits = 0

        for subject in subjects:
            if isinstance(subject, dict):
                credit = subject["credit"]
                grade = subject["grade"]
            else:
                credit, grade = subject

            point = cls.grade_to_point(grade)
            total_credit_points += credit * point
            total_credits += credit

        if total_credits == 0:
            return 0.0

        return round(total_credit_points / total_credits, 2)


    # ---------------------------------------------------------
    # CGPA
    # ---------------------------------------------------------
    @classmethod
    def calculate_cgpa(cls, semester_records):
        """
        Calculates overall CGPA.
        Parameters
        ----------
        semester_records : list
        Each item may be: {"subjects": [...]} or subject list directly
        Returns
        -------
        float
        """

        if not semester_records:
            return 0.0

        total_credit_points = 0
        total_credits = 0

        for record in semester_records:
            if isinstance(record, dict):
                subjects = record["subjects"]
            else:
                subjects = record

            for subject in subjects:
                if isinstance(subject, dict):
                    credit = subject["credit"]
                    grade = subject["grade"]
                else:
                    credit, grade = subject

                point = cls.grade_to_point(grade)
                total_credit_points += credit * point
                total_credits += credit

        if total_credits == 0:
            return 0.0

        return round(total_credit_points / total_credits, 2)


    # ---------------------------------------------------------
    # Grade Validation
    # ---------------------------------------------------------
    @classmethod
    def is_valid_grade(cls, grade):
        """
        Returns True if grade is valid.
        """
        if grade is None:
            return False
        return grade.strip().upper() in cls.GRADE_POINTS


    @classmethod
    def valid_grades(cls):
        """
        Returns all supported grades.
        """
        return list(cls.GRADE_POINTS.keys())
    



