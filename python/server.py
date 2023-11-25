import mariadb
from flask import Flask, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
from datetime import datetime
import pytz
from webforms import StudentForm, SearchForm, CourseForm


#  Create an instance of the Flask application
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost:3308/college_db'
app.config['SECRET_KEY'] = "SECRET"

db = SQLAlchemy(app)


class Course(db.Model):
    __tablename__ = 'course'

    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(20), nullable=False)
    date_created = db.Column(
        db.Date, nullable=datetime.now(pytz.timezone('Asia/Manila')))

    def __repr__(self):
        return f"<Student(course_id={self.course_id}, name='{self.course_name}', department={self.department}')>"


class Student(db.Model):
    __tablename__ = 'student'

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    middle_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    civil_status = db.Column(db.String(2), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def __init__(self, first_name, middle_name, last_name, dob, gender, civil_status, phone, email):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.dob = dob
        self.gender = gender
        self.civil_status = civil_status
        self.phone = phone
        self.email = email

    def __repr__(self):
        return f"<Student(student_id={self.student_id}, name='{self.first_name} {self.middle_name} {self.last_name}', dob={self.dob}, gender='{self.gender}', civil_status='{self.civil_status}', phone='{self.phone}', email='{self.email}')>"

# Form for adding student


# Route to serve home page


@app.route('/')
def index():
    title = 'Table View'
    navactive = 'student'
    active = 'view'
    form = SearchForm()
    students = Student.query

    if form.validate_on_submit():
        searched = form.search.data

        students = students.filter(
            or_(
                Student.first_name.like('%' + searched + '%'),
                Student.middle_name.like('%' + searched + '%'),
                Student.last_name.like('%' + searched + '%')
            )
        )
    else:
        students = students.all()

    return render_template('index.html', students=students, form=form, active=active, navactive=navactive, title=title)
# Route to serve the persons data as JSON


@app.route('/api/search', methods=['POST'])
def search():
    navactive = 'student'
    active = 'view'
    form = SearchForm()
    students = Student.query

    if form.validate_on_submit():
        searched = form.search.data

        students = students.filter(
            or_(
                Student.first_name.like('%' + searched + '%'),
                Student.middle_name.like('%' + searched + '%'),
                Student.last_name.like('%' + searched + '%')
            )
        )
    else:
        students = students.all()

    return render_template('search.html', students=students, form=form, active=active, navactive=navactive)


@app.route('/delete/<int:id>')
def delete(id):
    active = 'view'
    title = 'Table View'
    navactive = 'student'
    form = SearchForm()
    DeleteStudent = Student.query.get_or_404(id)

    try:
        db.session.delete(DeleteStudent)
        db.session.commit()

        flash('Student deleted successfully')
        students = Student.query.all()
        return render_template('index.html', students=students, form=form, active=active, navactive=navactive, title=title)

    except:
        flash('Delete failed')
        return render_template('index.html', students=students, form=form, active=active, navactive=navactive, title=title)


@app.route('/api/addstudent', methods=['GET', 'POST'])
def add_student():
    navactive = 'student'
    title = 'Add Student'
    active = 'add'
    first_name = None
    middle_name = None
    last_name = None
    dob = None
    gender = None
    civil_status = None
    phone = None
    email = None
    form = StudentForm()

    if request.method == 'POST' and form.validate_on_submit:

        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        civil_status = request.form.get('civil_status')
        phone = request.form.get('phone')
        email = request.form.get('email')

        existstudent = Student.query.filter(
            and_(
                Student.first_name == form.first_name.data,
                Student.email == form.email.data
            )
        ).first()

        if existstudent is None:
            student = Student(first_name=first_name, middle_name=middle_name, last_name=last_name,
                              dob=dob, gender=gender, civil_status=civil_status, phone=phone, email=email)
            db.session.add(student)
            db.session.commit()

            flash(f"Student {first_name} {last_name} added successfully")
        else:
            flash(f"Student {first_name} {last_name} already exist")

        form.first_name.data = None
        form.middle_name.data = None
        form.last_name.data = None
        form.dob.data = None
        form.dob.format = None
        form.gender.data = None
        form.civil_status.data = None
        form.phone.data = None
        form.email.data = None

    return render_template('studentform.html', active=active, form=form, title=title, navactive=navactive)


@app.route('/api/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    title = 'Table View'
    navactive = 'student'
    active = 'view'
    form = StudentForm()
    StudentUpdate = Student.query.get_or_404(id)

    if request.method == 'POST' and form.validate_on_submit:
        StudentUpdate.first_name = request.form['first_name']
        StudentUpdate.middle_name = request.form['middle_name']
        StudentUpdate.last_name = request.form['last_name']
        StudentUpdate.gender = request.form['gender']
        StudentUpdate.dob = request.form['dob']
        StudentUpdate.civil_status = request.form['civil_status']
        StudentUpdate.phone = request.form['phone']
        StudentUpdate.email = request.form['email']
        try:
            db.session.commit()
            flash('Student Updated Successfully')

            students = Student.query.all()
            return render_template('index.html', students=students, form=form, active=active, navactive=navactive, title=title)

        except:
            flash('Student Updated Successfully Failed')
            return render_template("update.html", form=form, StudentUpdate=StudentUpdate, navactive='student')
    else:
        return render_template("update.html", form=form, StudentUpdate=StudentUpdate, navactive='student')


@app.route('/course')
def courseindex():
    title = 'Table View'
    navactive = 'course'
    active = 'view'
    form = SearchForm()
    courses = Course.query

    if form.validate_on_submit():
        searched = form.search.data

        courses = courses.filter(
            or_(
                Course.course_name.like('%' + searched + '%'),
                Course.department_name.like('%' + searched + '%'),
            )
        )
    else:
        courses = courses.all()

    return render_template('courseindex.html', courses=courses, form=form, active=active, navactive=navactive, title=title)


@app.route('/api/addcourse', methods=['GET', 'POST'])
def add_course():
    navactive = 'course'
    title = 'Add Course'
    active = 'add'
    course_name = None
    department = None
    form = CourseForm()

    if request.method == 'POST' and form.validate_on_submit:
        course_name = request.form.get('course_name')
        department = request.form.get('department')

        existcourse = Course.query.filter(
            and_(
                Course.course_name == form.course_name.data,
                Course.department == form.department.data
            )
        ).first()

        if existcourse is None:
            course = Course(course_name=course_name, department=department)
            course.date_created = datetime.now(pytz.timezone('Asia/Manila'))
            db.session.add(course)
            db.session.commit()
            flash(f"Course {course_name} added successfully")
        else:
            flash(f"Course {course_name} already exist")

        form.course_name.data = None
        form.department.data = None

    return render_template('courseform.html', active=active, form=form, title=title,  navactive=navactive)


@app.route('/api/searchcourse', methods=['POST'])
def searchcourse():
    navactive = 'course'
    form = SearchForm()
    courses = Course.query

    if form.validate_on_submit():
        searched = form.search.data

        courses = courses.filter(
            or_(
                Course.course_name.like('%' + searched + '%'),
                Course.department.like('%' + searched + '%')
            )
        )
    else:
        courses = courses.all()

    return render_template('searchcourse.html', courses=courses, form=form, navactive=navactive)


@app.route('/deletecourse/<int:id>')
def deletecourse(id):
    active = 'view'
    title = 'Table View'
    navactive = 'course'
    form = SearchForm()
    DeleteCourse = Course.query.get_or_404(id)

    try:
        db.session.delete(DeleteCourse)
        db.session.commit()

        flash('Course deleted successfully')
        courses = Course.query.all()
        return render_template('courseindex.html', courses=courses, form=form, active=active, navactive=navactive, title=title)

    except:
        flash('Delete failed')
        return render_template('courseindex.html', courses=courses, form=form, active=active, navactive=navactive, title=title)


@app.route('/course/update/<int:id>', methods=['GET', 'POST'])
def courseupdate(id):
    title = 'Table View'
    navactive = 'course'
    active = 'view'
    form = CourseForm()
    CourseUpdate = Course.query.get_or_404(id)

    if request.method == 'POST' and form.validate_on_submit:
        existcourse = Course.query.filter(
            and_(
                Course.course_name == form.course_name.data,
                Course.department == form.department.data
            )
        ).first()

        if existcourse is None:
            CourseUpdate.course_name = request.form['course_name']
            CourseUpdate.department = request.form['department']
            CourseUpdate.date_created = datetime.now(
                pytz.timezone('Asia/Manila'))

            try:
                db.session.commit()
                flash('Course Updated Successfully')

                courses = Course.query.all()
                return render_template('courseindex.html', courses=courses, form=form, active=active, navactive=navactive, title=title)

            except:
                flash('Course Updated Successfully Failed')
                return render_template("courseupdate.html", form=form, CourseUpdate=CourseUpdate, navactive='course')
        else:
            flash(
                f"Course {form.course_name.data} in the {form.department.data} department already exists")
            return render_template("courseupdate.html", form=form, CourseUpdate=CourseUpdate, navactive='course')
    else:
        return render_template("courseupdate.html", form=form, CourseUpdate=CourseUpdate, navactive='course')


# Check if the script is being run as the main program
if __name__ == '__main__':
    app.run(debug=True, port=8000)  # start the Flask development web server.
