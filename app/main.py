from flask import Flask, jsonify

app = Flask(__name__)

students = []
courses = []

@app.route("/")
def home():
    return jsonify({
        "message": "Student Academic Management Platform",
        "status": "running"
    })

@app.route("/students")
def get_students():
    return jsonify(students)

@app.route("/courses")
def get_courses():
    return jsonify(courses)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
