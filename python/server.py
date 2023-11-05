import mariadb
from flask import Flask, jsonify, request, render_template, flash
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateField, EmailField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email
#  Create an instance of the Flask application
app = Flask(__name__)

app.config['SECRET_KEY'] = "SECRET"

# Database connection  parameters
db_params = {
    "host": "localhost",
    "port": 3308,
    "user": "root",
    "password": "1234",
    "database": "college_db",
}

# Form for adding student


class StudentForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired()])
    middle_name = StringField('Middle name', validators=[InputRequired()])
    last_name = StringField('Last name', validators=[InputRequired()])
    dob = DateField('Date of Birth', format='%Y-%m-%d',
                    validators=[InputRequired()])
    gender = SelectField('Gender', choices=[
        ('', 'Gender'),
        ('M', 'Male'),
        ('F', 'Female')
    ], validators=[InputRequired()])
    civil_status = SelectField('Civil Status', choices=[
        ('', 'Civil Status'),
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
        ('C', 'Civil Partnership'),
        ('O', 'Other')
    ], validators=[InputRequired()])
    phone = IntegerField('Phone number', validators=[DataRequired()])
    email = EmailField('Email', validators=[Email(), InputRequired()])
    submit = SubmitField('Submit')

# Route to serve home page


@app.route('/')
def index():
    active = 'view'
    return render_template('index.html', active=active)
# Route to serve the persons data as JSON


@app.route('/api/student', methods=['GET'])
def get_student():
    # Retrieve the "q" parameter from the query string of the request
    search = request.args.get("q")

    # Check if search param is present, then create SQL LIKE pattern
    if search:
        search = f"%{search}%"
    else:
        search = "%"

    try:
        # Establish a connection to the MariaDB database using provided connection parameters
        connection = mariadb.connect(**db_params)

        # Create a cursor for executing SQL queries
        cursor = connection.cursor()

        # Execute a SQL query to search for persons whose first name contains the search string
        cursor.execute(
            "SELECT * FROM student WHERE first_name LIKE %s", (search,))

        # Fetch all the data from the executed query
        data = cursor.fetchall()

        # Close the database connection
        connection.close()

        # Initialize an empty list to store the results
        students = []

        # Iterate through the fetched data and format it as a list of dictionaries
        for row in data:
            student = {
                "student_id": row[0],
                "first_name": row[1],
                "middle_name": row[2],
                "last_name": row[3],
                "dob": row[4],
                "gender": row[5],
                "civil_status": row[6],
                "phone": row[7],
                "email": row[8]
            }
            students.append(student)

        # Return the results as a JSON response
        return jsonify(students)

    except Exception as e:
        # If an error occurs during the execution, print the error message
        print(f"Error: {e}")

        # Create an error dictionary and return it as a JSON response
        error = {"error": e}
        return jsonify(error)

# Route to serve the filtered persons data as JSON


@app.route('/api/search', methods=['GET'])
def search_student():
    # Retrieve the "q" parameter from the query string of the request
    search = request.args.get("q")

    # Check if search param is present, then create SQL LIKE pattern
    if search:
        search = f"%{search}%"
    else:
        search = "%"
    try:
        # Establish a connection to the MariaDB database using provided connection parameters
        connection = mariadb.connect(**db_params)

        # Create a cursor for executing SQL queries
        cursor = connection.cursor()

        # Execute a SQL query to search for persons whose first name contains the search string
        query = """
            SELECT *
            FROM student
            WHERE first_name LIKE %s
        """

        # Execute the query with a single tuple of parameters
        cursor.execute(query, (search,))

        # Fetch all the data from the executed query
        data = cursor.fetchall()

        # Close the database connection
        connection.close()

        # Close the database connection
        connection.close()

        # Initialize an empty list to store the results
        students = []

        # Iterate through the fetched data and format it as a list of dictionaries
        for row in data:
            student = {
                "student_id": row[0],
                "first_name": row[1],
                "middle_name": row[2],
                "last_name": row[3],
                "dob": row[4],
                "gender": row[5],
                "civil_status": row[6],
                "phone": row[7],
                "email": row[8]
            }
            students.append(student)

        # Return the results as a JSON response
        return jsonify(students)
    except Exception as e:
        # If an error occurs during the execution, print the error message
        print(f"Error: {e}")
        # Create an error dictionary and return it as a JSON response
        error = {"error": e}

    return jsonify(error)


@app.route('/api/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        # Establish a connection to the MariaDB database using provided connection parameters
        connection = mariadb.connect(**db_params)

        # Create a cursor for executing SQL queries
        cursor = connection.cursor()

        # Execute a SQL query to delete a student by their ID
        cursor.execute("DELETE FROM student WHERE student_id = %s", (id,))

        # Commit the transaction to save the changes
        connection.commit()

        # Close the database connection
        connection.close()

        # Return a success message as a JSON response
        return jsonify({"message": f"Student with ID {id} has been deleted"})

    except Exception as e:
        # If an error occurs during the execution, print the error message
        print(f"Error: {e}")

        # Create an error dictionary and return it as a JSON response
        error = {"error": e}
        return jsonify(error)


@app.route('/api/addstudent', methods=['GET', 'POST'])
def add_student():
    first_name = None
    middle_name = None
    last_name = None
    dob = None
    gender = None
    civil_status = None
    phone = None
    email = None
    form = StudentForm()

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        civil_status = request.form.get('civil_status')
        phone = request.form.get('phone')
        email = request.form.get('email')

        form.first_name.data = None
        form.middle_name.data = None
        form.last_name.data = None
        form.dob.data = None
        form.dob.format = '%m-%d-%Y'
        form.gender.data = None
        form.civil_status.data = None
        form.phone.data = None
        form.email.data = None

        try:
            # Establish a connection to the MariaDB database using provided connection parameters
            connection = mariadb.connect(**db_params)

            # Create a cursor for executing SQL queries
            cursor = connection.cursor()

            # Execute an SQL query to insert the student data into the database
            cursor.execute("INSERT INTO student (first_name, middle_name, last_name, dob, gender, civil_status, phone, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (first_name, middle_name, last_name, dob, gender, civil_status, phone, email))

            # Commit the transaction to save the changes
            connection.commit()

            # Close the database connection
            connection.close()

            flash(f"Student {first_name} {last_name} added successfully")

        except Exception as e:
            # If an error occurs during the execution, print the error message
            print(f"Error: {e}")
            flash("An error occurred while adding the student")

    return render_template('studentform.html', active='add', form=form)


@app.route('/api/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = StudentForm()

    try:
        if request.method == 'POST':
            # Establish a connection to the MariaDB database using provided connection parameters
            connection = mariadb.connect(**db_params)

            # Create a cursor for executing SQL queries
            cursor = connection.cursor()

            # Fetch the student's information based on the provided ID
            query = "SELECT * FROM student WHERE student_id = %s"
            cursor.execute(query, (id,))
            student_data = cursor.fetchone()

            if not student_data:
                # If the student with the provided ID doesn't exist, return an error message
                connection.close()
                return jsonify({"error": f"Student with ID {id} not found"})

            # Retrieve the student's existing data
            student_id, first_name, middle_name, last_name, dob, gender, civil_status, phone, email = student_data

            # Update student data based on the form inputs
            first_name = request.form.get('first_name')
            middle_name = request.form.get('middle_name')
            last_name = request.form.get('last_name')
            dob = request.form.get('dob')
            gender = request.form.get('gender')
            civil_status = request.form.get('civil_status')
            phone = request.form.get('phone')
            email = request.form.get('email')

            # Execute a SQL query to update the student's information
            update_query = """
                UPDATE student
                SET first_name = %s, middle_name = %s, last_name = %s, dob = %s, gender = %s, civil_status = %s, phone = %s, email = %s
                WHERE student_id = %s
            """
            cursor.execute(update_query, (first_name, middle_name,
                           last_name, dob, gender, civil_status, phone, email, id))

            # Commit the transaction to save the changes
            connection.commit()

            # Close the database connection
            connection.close()

            flash("Student Updated Successfully!")
            return render_template('update_students.html', student_id=id, first_name=first_name, middle_name=middle_name, last_name=last_name, dob=dob, gender=gender, civil_status=civil_status, phone=phone, email=email, form=form)
        else:
            # Handle the GET request to show the form for updating the student's information
            return render_template('update_students.html', student_id=id, first_name=first_name, middle_name=middle_name, last_name=last_name, dob=dob, gender=gender, civil_status=civil_status, phone=phone, email=email, form=form)

    except Exception as e:
        # If an error occurs during the execution, print the error message
        print(f"Error: {e}")

        # Create an error dictionary and return it as a JSON response
        error = {"error": e}
        return jsonify(error)


# Check if the script is being run as the main program
if __name__ == '__main__':
    app.run(debug=True, port=8000)  # start the Flask development web server.
