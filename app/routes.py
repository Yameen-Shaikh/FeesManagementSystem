from flask import request, jsonify, render_template, Flask
from main import auth_bp
from db import get_db

app = Flask()
@app.route("/", methods = ["GET"])
def home():
    return render_template('dashboard.html')

@auth_bp.route("/login", method = ["POST"])
def login(): #TODO: password hashing
    return "Working"

@auth_bp.route("/logout", method = ["POST"])
def logout():
    return

@app.route("/student/<int:roll_no>", methods=["GET"])
def get_student(roll_no):
    cur = get_db().cursor()
    cur.execute(f"SELECT * FROM students WHERE roll_no == {roll_no}")
    rows = cur.fetchall()
    return jsonify([dict(row) for row in rows])

@app.route("/add_student", methods=["POST"])
def add_student():
    data = request.get_json()
    name = data.get("name")
    roll_no = data.get("roll_no")
    age = data.get("age")
    
    cur = get_db().cursor()
    cur.execute("INSERT INTO students (name, roll_no, age) VALUES (?, ?, ?)", (name, roll_no, age))
    get_db().commit()
    return jsonify({"message": "Student added successfully"}), 201
