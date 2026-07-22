from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock database of multiple students and their respective modules
students_db = {
    "EDU-2026-8942": {
        "name": "Tshepo Letsoalo",
        "student_id": "EDU-2026-8942",
        "program": "Computer Science",
        "modules": [
            {"code": "CS101", "name": "Introduction to Computer Science", "credits": 4, "score": 92, "grade": "A", "status": "PASSED"},
            {"code": "NET201", "name": "Communications & Networking", "credits": 3, "score": 88, "grade": "B+", "status": "PASSED"},
            {"code": "SEC301", "name": "Network Protection & Threat Prevention", "credits": 3, "score": 95, "grade": "A", "status": "PASSED"},
            {"code": "DEV102", "name": "Python Software Development", "credits": 4, "score": 90, "grade": "A", "status": "PASSED"}
        ]
    },
    "EDU-2026-1045": {
        "name": "Lerato Mokoena",
        "student_id": "EDU-2026-1045",
        "program": "Software Engineering",
        "modules": [
            {"code": "MAT101", "name": "College Algebra", "credits": 3, "score": 75, "grade": "B", "status": "PASSED"},
            {"code": "DEV101", "name": "Introduction to Programming", "credits": 4, "score": 82, "grade": "B+", "status": "PASSED"}
        ]
    }
}

# Keep track of the currently active student ID
current_student_id = "EDU-2026-8942"

@app.route('/')
def index():
    global current_student_id
    
    # Handle search query if provided in URL parameters
    search_query = request.args.get('search', '').strip().upper()
    if search_query in students_db:
        current_student_id = search_query

    learner = students_db.get(current_student_id, list(students_db.values())[0])
    modules_data = learner["modules"]
    
    total_credits = sum(m['credits'] for m in modules_data)
    if modules_data:
        avg_score = sum(m['score'] for m in modules_data) / len(modules_data)
        gpa = round((avg_score / 100) * 4.0, 2)
    else:
        gpa = 0.0
        
    return render_template('dashboard.html', 
                           learner=learner,
                           modules=modules_data, 
                           total_credits=total_credits, 
                           cumulative_gpa=gpa,
                           all_students=students_db.keys())

@app.route('/switch', methods=['POST'])
def switch_student():
    global current_student_id
    selected_id = request.form.get('student_id')
    if selected_id in students_db:
        current_student_id = selected_id
    return redirect(url_for('index'))

@app.route('/add-student', methods=['POST'])
def add_student():
    global current_student_id
    name = request.form.get('name')
    student_id = request.form.get('student_id').strip().upper()
    program = request.form.get('program')
    
    if student_id and student_id not in students_db:
        students_db[student_id] = {
            "name": name,
            "student_id": student_id,
            "program": program,
            "modules": []
        }
        current_student_id = student_id
        
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_module():
    global current_student_id
    learner = students_db[current_student_id]
    
    code = request.form.get('code')
    name = request.form.get('name')
    credits = int(request.form.get('credits', 0))
    score = float(request.form.get('score', 0))
    
    if score >= 90: grade = "A"
    elif score >= 80: grade = "B+"
    elif score >= 70: grade = "B"
    elif score >= 60: grade = "C"
    else: grade = "F"

    status = "PASSED" if score >= 50 else "FAILED"

    new_module = {
        "code": code,
        "name": name,
        "credits": credits,
        "score": score,
        "grade": grade,
        "status": status
    }
    
    learner["modules"].append(new_module)
    return redirect(url_for('index'))

@app.route('/remove/<int:index>', methods=['POST'])
def remove_module(index):
    global current_student_id
    modules_data = students_db[current_student_id]["modules"]
    if 0 <= index < len(modules_data):
        modules_data.pop(index)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)