from flask import Flask, render_template, request, session, redirect, url_for, flash
from main import StudentGradeManagementSystem
from flask import send_file
from io import BytesIO
from pdf_generator import PDFGenerator


app = Flask(__name__)
app.secret_key = "student_grade_manager_secret_key"
system = StudentGradeManagementSystem()

@app.route("/")
def home():
    return render_template("home.html")



@app.route("/create-account", methods=["GET", "POST"])
def create_account():

    if request.method == "POST":

        form = request.form.to_dict()

        password = form["password"]
        confirm = form["confirm_password"]

        if password != confirm:

            form["password"] = ""
            form["confirm_password"] = ""

            return render_template(
                "create_account.html",
                error="Passwords do not match.",
                form=form
            )

        try:

            student_id = system.create_student_account(

                form["name"],
                form["father_name"],
                form["mother_name"],
                form["dob"],
                form["gender"],
                form["phone"],
                form["email"],
                form["address"],
                password
            )

            return render_template(
                "success.html",
                student_id=student_id
            )

        except Exception as error:
            message = str(error)
            if "Phone" in message:
                form["phone"] = ""

            if "Email" in message:
                form["email"] = ""

            form["password"] = ""
            form["confirm_password"] = ""

            return render_template(
                "create_account.html",
                error=message,
                form=form
            )

    return render_template(
        "create_account.html",
        error="",
        form={}
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        form = request.form.to_dict()

        try:
            student = system.login_student(
                int(form["student_id"]),
                form["password"]
            )

            session["student_id"] = student.student_id
            return redirect(url_for("dashboard"))

        except Exception:
            form["password"] = ""
            return render_template(
                "login.html",
                error="Invalid Student ID or Password.",
                form=form
            )

    return render_template(
        "login.html",
        error="",
        form={}
    )


@app.route("/dashboard")
def dashboard():

    if "student_id" not in session:
        return redirect(url_for("login"))

    student = system.get_student(
        session["student_id"]
    )

    return render_template(
        "dashboard.html",
        student=student,
        success=request.args.get("success", "")
    )


@app.route("/add-academic-record")
def add_academic_record():

    if "student_id" not in session:
        return redirect(url_for("login"))

    return render_template("add_academic_record.html")


@app.route("/update")
def update():

    if "student_id" not in session:
        return redirect(url_for("login"))

    student = system.get_student(
        session["student_id"]
    )

    return render_template(

        "update.html",

        student=student

    )


@app.route("/update/personal", methods=["GET", "POST"])
def update_personal():

    if "student_id" not in session:
        return redirect(url_for("login"))

    student = system.get_student(
        session["student_id"]
    )

    if request.method == "POST":
        form = request.form.to_dict()

        password = form["password"]
        confirm = form["confirm_password"]

        if password != confirm:

            form["password"] = ""
            form["confirm_password"] = ""

            return render_template(
                "update_personal.html",
                form=form,
                error="Passwords do not match."
            )

        try:
            system.update_student_account(
                session["student_id"],
                form["name"],
                form["father_name"],
                form["mother_name"],
                form["dob"],
                form["gender"],
                form["phone"],
                form["email"],
                form["address"],
                password
            )

            student = system.get_student(
                session["student_id"]
            )

            form = {
                "student_id": student.student_id,
                "name": student.name,
                "father_name": student.father_name,
                "mother_name": student.mother_name,
                "dob": student.date_of_birth,
                "gender": student.gender,
                "phone": student.phone,
                "email": student.email,
                "address": student.address,
                "password": "",
                "confirm_password": ""
            }

            flash(
                "Personal details updated successfully.", "success"
            )

            return redirect(url_for("update"))

        except Exception as error:
            message = str(error)

            if "Phone" in message:
                form["phone"] = ""

            if "Email" in message:
                form["email"] = ""

            form["password"] = ""
            form["confirm_password"] = ""

            return render_template(
                "update_personal.html",
                form=form,
                error=message,
                success=""
            )

    form = {
        "student_id": student.student_id,
        "name": student.name,
        "father_name": student.father_name,
        "mother_name": student.mother_name,
        "dob": student.date_of_birth,
        "gender": student.gender,
        "phone": student.phone,
        "email": student.email,
        "address": student.address,
        "password": "",
        "confirm_password": ""
    }

    return render_template(
        "update_personal.html",
        form=form,
        error="",
        success=""
    )


@app.route("/update/school")
def update_school():

    if "student_id" not in session:
        return redirect(url_for("login"))

    records = system.get_student_records(
        session["student_id"]
    )

    school_records = [
        record
        for record in records
        if record["record_type"] == "School"
    ]

    return render_template(
        "update_school.html",
        school_records=school_records
    )

@app.route("/update/school/<int:record_id>", methods=["GET", "POST"])
def edit_school_record(record_id):

    if "student_id" not in session:
        return redirect(url_for("login"))

    import json
    # =====================================================
    # UPDATE
    # =====================================================
    if request.method == "POST":
        form = request.form.to_dict()
        try:
            subjects = json.loads(form["subjects"])
            system.update_school_record(
                record_id,
                form["school_name"],
                form["board"],
                form["academic_year"],
                subjects
            )

            flash(
                f"{form['level']} updated successfully.",
                "success"
            )       

            return redirect(
                url_for("update_school")
            )

        except Exception as error:
            return render_template(
                "school_record.html",
                mode="update",
                form=form,
                subjects=json.loads(form["subjects"]),
                success="",
                error=str(error)
            )

    # =====================================================
    # LOAD RECORD
    # =====================================================
    record = system.get_school_record(record_id)

    if record is None:
        flash(
            "School record not found.",
            "danger"
        )

        return redirect(
            url_for("update_school")
        )

    form = {
        "level": record["level"],
        "school_name": record["school_name"],
        "board": record["board"],
        "academic_year": record["academic_year"]
    }

    subjects = [
        {
            "id": subject["subject_id"],
            "name": subject["name"],
            "grade": subject["grade"]
        }
        for subject in record["subjects"]
    ]

    return render_template(
        "school_record.html",
        mode="update",
        form=form,
        subjects=subjects,
        success="",
        error=""
    )


@app.route("/update/college")
def update_college():

    if "student_id" not in session:
        return redirect(url_for("login"))

    records = system.get_student_records(
        session["student_id"]
    )

    college_records = [
        record
        for record in records
        if record["record_type"] == "College"
    ]

    return render_template(
        "update_college.html",
        college_records=college_records
    )


@app.route("/update/college/<int:record_id>", methods=["GET", "POST"])
def edit_college_record(record_id):
    if "student_id" not in session:
        return redirect(url_for("login"))


    import json

        # =====================================================
        # UPDATE
        # =====================================================

    if request.method == "POST":
        form = request.form.to_dict()
        try:
            courses = json.loads(form["courses"])
            system.update_college_record(
                record_id,
                form["college_name"],
                form["branch"],
                form["academic_year"],
                courses
            )

            flash(
                "College record updated successfully.",
                "success"
            )

            return redirect(
                url_for("update_college")
            )

        except Exception as error:
            return render_template(
                "college_record.html",
                mode="update",
                form=form,
                courses=json.loads(form["courses"]),
                success="",
                error=str(error)
            )



    record = system.get_college_record(record_id)

    if record is None:
        flash(
            "College record not found.",
            "danger"
        )

        return redirect(
            url_for("update_college")
        )

    level = record["level"].split(" Sem ")

    form = {
        "degree": level[0],
        "semester": level[1],
        "college_name": record["college_name"],
        "branch": record["branch"],
        "academic_year": record["academic_year"]
    }

    courses = [
        {
            "id": course["subject_id"],
            "name": course["name"],
            "credit": course["credit"],
            "grade": course["grade"]
        }
        for course in record["courses"]
    ]

    return render_template(
        "college_record.html",
        mode="update",
        form=form,
        courses=courses,
        success="",
        error=""
    )


@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/delete/school")
def delete_school():

    if "student_id" not in session:
        return redirect(url_for("login"))

    records = system.get_student_records(session["student_id"])

    school_records = [
        record
        for record in records
        if record["record_type"] == "School"
    ]

    return render_template(
        "delete_school.html",
        school_records=school_records
    )

@app.route("/delete/college")
def delete_college():
    if "student_id" not in session:
        return redirect(url_for("login"))

    records = system.get_student_records(
        session["student_id"]
    )

    college_records = [
        record
        for record in records
        if record["record_type"] == "College"
    ]

    return render_template(
        "delete_college.html",
        college_records=college_records
    )

@app.route("/delete/school/<int:record_id>", methods=["POST"])
def delete_school_record(record_id):

    if "student_id" not in session:
        return redirect(url_for("login"))

    try:

        system.delete_record(record_id)

        flash(
            "School record deleted successfully.",
            "success"
        )

    except Exception as error:

        flash(
            str(error),
            "danger"
        )

    return redirect(
        url_for("delete_school")
    )


@app.route("/delete/college/<int:record_id>", methods=["POST"])
def delete_college_record(record_id):
    if "student_id" not in session:
        return redirect(url_for("login"))

    try:
        system.delete_record(record_id)
        flash(
            "College record deleted successfully.",
            "success"
        )

    except Exception as error:
        flash(
            str(error),
            "danger"
        )

    return redirect(
        url_for("delete_college")
    )


@app.route("/delete/student", methods=["GET", "POST"])
def delete_student():

    if "student_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        password = request.form["password"]

        student = system.get_student(
            session["student_id"]
        )

        student.password = password

        if not student.verify_password():

            return render_template(
                "delete_student.html",
                error="Incorrect password."
            )

        # Password correct
        system.delete_student(
            session["student_id"]
        )

        session.clear()

        flash(
            "Student account deleted successfully.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "delete_student.html",
        error=""
    )


@app.route("/student-report")
def student_report():

    if "student_id" not in session:
        return redirect(url_for("login"))

    report = system.get_student_report(
        session["student_id"]
    )

    return render_template(
        "student_report.html",
        report=report
    )


# ===========================================
# Add Academic Record
# ===========================================

@app.route("/school-record", methods=["GET", "POST"])
def school_record():

    if "student_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        import json
        form = request.form.to_dict()

        try:
            subjects = []
            for subject in json.loads(form["subjects"]):
                subjects.append((subject["name"], subject["grade"]))

            result = system.create_school_record(
                session["student_id"],
                form["level"],
                form["school_name"],
                form["board"],
                form["academic_year"],

                subjects
            )

            success = f"Added: {', '.join(result['added'])}"

            if result["skipped"]:
                success += "<br>Already Present: " + ", ".join(result["skipped"])

            return render_template(
                "school_record.html",
                success=success,
                error="",
                form={},
                subjects=[]
            )

        except Exception as error:
            return render_template(
                "school_record.html",
                success="",
                error=str(error),
                form=form,
                subjects=json.loads(form["subjects"])
            )

    return render_template(
        "school_record.html",
        success="",
        error="",
        form={},
        subjects=[]
    )


@app.route("/college-record", methods=["GET","POST"])
def college_record():

    if "student_id" not in session:
        return redirect(url_for("login"))

    if request.method=="POST":

        import json
        form=request.form.to_dict()

        try:
            courses=[]

            for course in json.loads(form["courses"]):
                courses.append(
                    (
                        course["name"],
                        int(course["credit"]),
                        course["grade"]
                    )
                )

            level=f"{form['degree']} Sem {form['semester']}"

            result=system.create_college_record(
                session["student_id"],
                level,
                form["college_name"],
                form["branch"],
                form["academic_year"],
                courses
            )

            success=f"Added : {', '.join(result['added'])}"

            if result["skipped"]:
                success+="<br>Already Present : "
                success+=", ".join(result["skipped"])

            return render_template(
                "college_record.html",
                success=success,
                error="",
                form={},
                courses=[]
            )

        except Exception as error:

            return render_template(
                "college_record.html",
                success="",
                error=str(error),
                form=form,
                courses=json.loads(form["courses"])
            )

    return render_template(
        "college_record.html",
        success="",
        error="",
        form={},
        courses=[]
    )




@app.route("/download-pdf")
def download_pdf():

    if "student_id" not in session:
        return redirect(url_for("login"))

    report = system.get_student_report(
        session["student_id"]
    )

    pdf_generator = PDFGenerator()

    pdf = pdf_generator.generate_student_report(
        report
    )

    return send_file(

        BytesIO(pdf),

        as_attachment=True,

        download_name=f"Transcript_{session['student_id']}.pdf",

        mimetype="application/pdf"

    )



# ===========================================
# Logout
# ===========================================

@app.route("/logout")
def logout():

    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)