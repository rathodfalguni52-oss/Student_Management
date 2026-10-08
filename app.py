from flask import Flask,request,jsonify
from database import get_connection,initialize_database

app=Flask(__name__)
initialize_database()

# Home
@app.route("/")
def home():
    return jsonify({
        "message":"Student Management REST API is running"
    })

#CREATE STUDENT 
@app.route("/students",methods=["POST"])
def add_student():
    data=request.get_json()
    if not isinstance(data,dict):
        return jsonify({
            "error":"Request body must be valid JSON object"
        }),400
    name=data.get("name")
    email=data.get("email")
    age=data.get("age")
    course=data.get("course")
    if not name or not email or age is None or not course:
        return jsonify({
            "error":"name,email,age and course are required"
        }),400
    connection=get_connection()
    try:
        cursor=connection.cursor()
        cursor.execute("""INSERT INTO students (name,email,age,course)
        VALUES(?,?,?,?)""",(name,email,age,course))
        connection.commit()
        student_id=cursor.lastrowid
        return jsonify({
            "message":"Student added successfully",
            "student_id":student_id
        }),201
    except Exception as e:
        return jsonify({
            "Error":str(e)
        }),400
    finally:
        connection.close()

# GET ALL STUDENTS
@app.route("/students",methods=["GET"])
def get_students():
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM students")
    students=cursor.fetchall()
    connection.close()
    student_list=[]
    for student in students:
        student_list.append({
            "id":student["id"],
            "name":student["name"],
            "email":student["email"],
            "age":student["age"],
            "course":student["course"]
        })
    return jsonify(student_list)

# GET STUDENT BY ID
@app.route("/students/<int:student_id>",methods=["GET"])
def get_student(student_id):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM students WHERE id=?",(student_id,))
    student=cursor.fetchone()
    connection.close()
    if student is None:
        return jsonify({
            "Error":"Student not found"
        }),404
    return jsonify({
        "id":student["id"],
        "name":student["name"],
        "email":student["email"],
        "age":student["age"],
        "course":student["course"]
    })

# GET STUDENT BY NAME
@app.route("/students/search",methods=["GET"])
def search_student():
    name=request.args.get("name")
    if not name:
        return jsonify({
            "Error":"Name query parameter is required"
        }),400
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM students WHERE name LIKE ?",("%"+name+"%",))
    students=cursor.fetchall()
    connection.close()
    if not students:
        return jsonify({
            "Error":"No students found with the given name"
        }),404
    student_list=[]
    for student in students:
        student_list.append({
            "id":student["id"],
            "name":student["name"],
            "email":student["email"],
            "age":student["age"],
            "course":student["course"]
        })
    return jsonify(student_list)

# FILTER STUDENTS BY COURSE
@app.route("/students/course/<string:course>",methods=["GET"])
def get_students_by_course(course):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM students WHERE course=?",(course,))
    students=cursor.fetchall()
    connection.close()
    if not students:
        return jsonify({
            "Error":"No students found for the given course"
        }),404
    student_list=[]
    for student in students:
        student_list.append({
            "id":student["id"],
            "name":student["name"],
            "email":student["email"],
            "age":student["age"],
            "course":student["course"]
        })
    return jsonify(student_list)

# UPDATE STUDENT
@app.route("/students/<int:student_id>",methods=["PUT"])
def update_student(student_id):
    data=request.get_json()
    if not data:
        return jsonify({
            "Error":"Request body is required"
        }),400

    name=data.get("name")
    email=data.get("email")
    age=data.get("age")
    course=data.get("course")

    if not name or not email or age is None or not course:
        return jsonify({
            "Error":"name,email,age and course are required"
        }),400
    connection=get_connection()

    try:
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM student WHERE id=?",(student_id,))
        student=cursor.fetchone()
        if student is None:
            connection.close()
            return jsonify({
                "Error":"Student not found"
            }),400
        cursor.execute("""UPDATE students SET name=?,email=?,age=?,course=? WHERE id=?""",
                       (name,email,age,course,student_id))
        connection.commit()
        return({
            "Message":"Student updated successfully"
        })

    except Exception as e:
        return jsonify({
            "Error":str(e)
        }),400

    finally:
        connection.close()

# DELETE STUDENT
@app.route("/students/<int:student_id>",methods=["DELETE"])
def delete_student(student_id):
    connection=get_connection()
    try:
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM students where id=?",(student_id,))
        student=cursor.fetchone()
        if student is None:
            return jsonify({
                "Error":"Student not found"
            }),404

        cursor.execute("DELETE FROM students WHERE id=?",(student_id,))
        connection.commit()
        return jsonify({
            "Message":"Student deleted successfully"
        })
    finally:
        connection.close()

# RUN APPLICATION
if __name__=="__main__":
    app.run(debug=True)