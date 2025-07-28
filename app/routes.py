from flask import request, jsonify, Blueprint
from .db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('routes', __name__)

@bp.route("/", methods=["GET"])
def home():
    return "Working"

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    roll_no = data.get("roll_no")
    password = data.get("password")
    cur = get_db().cursor()
    cur.execute(f"SELECT password FROM students WHERE roll_no = {roll_no}")
    student = cur.fetchone()
    if student and check_password_hash(student["password"], password):
        return jsonify({"message": "Login successful"})
    return jsonify({"message": "Invalid credentials"}), 401

@bp.route("/logout", methods=["POST"])
def logout():
    return "Logged out"

@bp.route("/student/<int:roll_no>", methods=["GET"])
def get_student(roll_no):
    cur = get_db().cursor()
    cur.execute(f"SELECT roll_no, name, admission_date, paid_fees FROM students WHERE roll_no = {roll_no}")
    row = cur.fetchone()
    if row:
        return jsonify(dict(row))
    return jsonify({"message": "Student not found"}), 404

@bp.route("/add_student", methods=["POST"])
def add_student():
    data = request.get_json()
    name = data.get("name")
    roll_no = data.get("roll_no")
    password = data.get("password")
    admission_date = data.get("admission_date")
    paid_fees = data.get("paid_fees")

    if not all([name, roll_no, password, admission_date, paid_fees]):
        return jsonify({"message": "Missing required fields"}), 400

    hashed_password = generate_password_hash(password)

    cur = get_db().cursor()
    try:
        cur.execute(
            "INSERT INTO students (name, roll_no, password, admission_date, paid_fees) VALUES (?, ?, ?, ?, ?)",
            (name, roll_no, hashed_password, admission_date, paid_fees),
        )
        get_db().commit()
        return jsonify({"message": "Student added successfully"}), 201
    except Exception as e:
        get_db().rollback()
        return jsonify({"message": str(e)}), 500
