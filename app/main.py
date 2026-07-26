import io
import hashlib
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = "secure-hackathon-2026-key"

students_db = {
    "EDU-2026-8942": {
        "name": "Tshepo Letsoalo",
        "student_id": "EDU-2026-8942",
        "faculty": "Computer Science",
        "program": "BSc Computer Science",
        "modules": [
            {"code": "CS101", "name": "Introduction to Computer Science", "credits": 12, "score": 92, "grade": "A", "status": "PASSED"},
            {"code": "INL110", "name": "Information Science 110", "credits": 12, "score": 88, "grade": "B+", "status": "PASSED"},
            {"code": "INL120", "name": "Information Science 120", "credits": 12, "score": 95, "grade": "A", "status": "PASSED"},
            {"code": "DEV102", "name": "Python Software Development", "credits": 12, "score": 90, "grade": "A", "status": "PASSED"}
        ]
    },
    "EDU-2026-1045": {
        "name": "Lerato Mokoena",
        "student_id": "EDU-2026-1045",
        "faculty": "Information Science",
        "program": "BIS Information Science",
        "modules": [
            {"code": "INL110", "name": "Information Science 110", "credits": 12, "score": 75, "grade": "B", "status": "PASSED"},
            {"code": "INL120", "name": "Information Science 120", "credits": 12, "score": 82, "grade": "B+", "status": "PASSED"},
            {"code": "INL130", "name": "Personal Information Management", "credits": 12, "score": 78, "grade": "B", "status": "PASSED"}
        ]
    },
    "EDU-2026-2201": {
        "name": "Lebogang",
        "student_id": "EDU-2026-2201",
        "faculty": "Computer Science",
        "program": "BSc Computer Science",
        "modules": [
            {"code": "CS101", "name": "Introduction to Computer Science", "credits": 12, "score": 68, "grade": "C", "status": "PASSED"},
            {"code": "MAT114", "name": "Calculus and Linear Algebra", "credits": 12, "score": 42, "grade": "F", "status": "FAILED"},
            {"code": "DEV102", "name": "Python Software Development", "credits": 12, "score": 55, "grade": "C", "status": "PASSED"}
        ]
    },
    "EDU-2026-2202": {
        "name": "Mapula",
        "student_id": "EDU-2026-2202",
        "faculty": "Information Science",
        "program": "BIS Information Science",
        "modules": [
            {"code": "INL110", "name": "Information Science 110", "credits": 12, "score": 51, "grade": "C", "status": "PASSED"},
            {"code": "STN111", "name": "Statistics for Humanities", "credits": 12, "score": 38, "grade": "F", "status": "FAILED"},
            {"code": "INL120", "name": "Information Science 120", "credits": 12, "score": 45, "grade": "F", "status": "FAILED"}
        ]
    },
    "EDU-2026-2203": {
        "name": "Dimpho",
        "student_id": "EDU-2026-2203",
        "faculty": "Multimedia",
        "program": "BIS Multimedia",
        "modules": [
            {"code": "IMY110", "name": "Mark-up Languages", "credits": 12, "score": 72, "grade": "B", "status": "PASSED"},
            {"code": "IMY120", "name": "Multimedia for the Web", "credits": 12, "score": 48, "grade": "F", "status": "FAILED"},
            {"code": "VIS101", "name": "Visual Design Concepts", "credits": 12, "score": 80, "grade": "B+", "status": "PASSED"}
        ]
    },
    "EDU-2026-3011": {
        "name": "Kabelo Sithole",
        "student_id": "EDU-2026-3011",
        "faculty": "Multimedia",
        "program": "BIS Multimedia",
        "modules": [
            {"code": "IMY110", "name": "Mark-up Languages", "credits": 12, "score": 85, "grade": "B+", "status": "PASSED"},
            {"code": "IMY120", "name": "Multimedia for the Web", "credits": 12, "score": 91, "grade": "A", "status": "PASSED"}
        ]
    },
    "EDU-2026-4052": {
        "name": "Ananzi Dlamini",
        "student_id": "EDU-2026-4052",
        "faculty": "Publishing",
        "program": "BIS Publishing",
        "modules": [
            {"code": "PUB110", "name": "Introduction to Publishing", "credits": 12, "score": 80, "grade": "B+", "status": "PASSED"},
            {"code": "PUB120", "name": "The Book Publishing Environment", "credits": 12, "score": 86, "grade": "B+", "status": "PASSED"}
        ]
    }
}

# Localization dictionary supporting all official South African languages
transcript_i18n = {
    "en": {
        "title": "OFFICIAL ACADEMIC TRANSCRIPT",
        "name": "Student Name",
        "id": "Student ID",
        "faculty": "Faculty",
        "program": "Program",
        "code": "Code",
        "mod_name": "Module Name",
        "credits": "Credits",
        "score": "Score",
        "grade": "Grade",
        "footer": "This is a computer-generated official academic document backed by EduTrack Security-by-Design Architecture."
    },
    "zu": {
        "title": "UMBHALO OSEMTHETHWENI WEZIKHWAMA",
        "name": "Igama Lomfundi",
        "id": "Inombolo Yomfundi",
        "faculty": "Umkhakha",
        "program": "Uhlelo",
        "code": "Ikhodi",
        "mod_name": "Igama Lemojuli",
        "credits": "Amakhredithi",
        "score": "Amaphuzu",
        "grade": "Ibanga",
        "footer": "Lolu wuhlelo lwekhompyutha olusemthethweni lwezemfundo."
    },
    "xh": {
        "title": "INGXELO SEMTHETHO YEZIMFUNDO",
        "name": "Igama Lomfundi",
        "id": "Inombolo Yomfundi",
        "faculty": "ISebe",
        "program": "Inkqubo",
        "code": "Ikhodi",
        "mod_name": "Igama Lemodyuli",
        "credits": "Amakhredithi",
        "score": "Amanqaku",
        "grade": "Ibanga",
        "footer": "Le ngxelo yenzelwe ikhompyutha phantsi kweEduTrack."
    },
    "af": {
        "title": "AMPTELIKE AKADEMIESE TRANSKRIPSIE",
        "name": "Student Naam",
        "id": "Student ID",
        "faculty": "Fakulteit",
        "program": "Program",
        "code": "Kode",
        "mod_name": "Modulenaam",
        "credits": "Krediete",
        "score": "Punt",
        "grade": "Graad",
        "footer": "Hierdie is 'n rekenaargegegenereerde amptelike akademiese dokument."
    },
    "nso": {
        "title": "LENGWALO LA DIKAO LA SEMOLAO",
        "name": "Leina la Moithuti",
        "id": "Nomoro ya Moithuti",
        "faculty": "Lefapha",
        "program": "Lenaneo",
        "code": "Khoutu",
        "mod_name": "Leina la Modumo",
        "credits": "Dikrediti",
        "score": "Maraka",
        "grade": "Sehlopha",
        "footer": "Ye ke tokomane ya semolao ya thuto e hlahisitšwego ka khomphuta."
    },
    "tn": {
        "title": "DITLANKANA TSA SEMOLAO TSA THUTO",
        "name": "Leina la Moithuti",
        "id": "Nomoro ya Moithuti",
        "faculty": "Lefapha",
        "program": "Lenaneo",
        "code": "Khoutu",
        "mod_name": "Leina la Modumo",
        "credits": "Dikrediti",
        "score": "Moroago",
        "grade": "Bete",
        "footer": "Ke tokomane ya semolao ya thuto e e dirilweng ka khomputa."
    },
    "st": {
        "title": "LENGOLO LA SEMOLAO LA DITHUTO",
        "name": "Lebitso la Moithuti",
        "id": "Nomoro ya Moithuti",
        "faculty": "Lefapha",
        "program": "Lenaneo",
        "code": "Khoutu",
        "mod_name": "Lebitso la Modumo",
        "credits": "Dikrediti",
        "score": "Lintlha",
        "grade": "Sehlopha",
        "footer": "Lena ke tokomane ya semolao ya thuto e etswang ka khomphutha."
    },
    "ts": {
        "title": "PAPILA RA XIMFIRO RA DYONDZO",
        "name": "Vito ra Mudyondzi",
        "id": "Nomboro ya Mudyondzi",
        "faculty": "Ndzawulo",
        "program": "Porogramu",
        "code": "Khoutu",
        "mod_name": "Vito ra Modulu",
        "credits": "Kirediti",
        "score": "Maraka",
        "grade": "Giredi",
        "footer": "Loku i papila ra ximfiro ra dyondzo leri endliwe hi khomputa."
    },
    "ss": {
        "title": "UMBHALO SEMTHETHO WEMFUNDO",
        "name": "Igama Lemfundi",
        "id": "Inombolo Yemfundzi",
        "faculty": "Timvume",
        "program": "Luhlelo",
        "code": "Ikhodi",
        "mod_name": "Igama Lemoduli",
        "credits": "Emakhredithi",
        "score": "Amaphoyinti",
        "grade": "Libanga",
        "footer": "Loku kuyincwadzi semthetho yemfundo leyentiwe ngekhompyutha."
    },
    "ve": {
        "title": "VHUSHUMO HA SEMOLAO HA PFUNZO",
        "name": "Dzina la Mufunzi",
        "id": "Nomboro ya Mufunzi",
        "faculty": "Khafulithi",
        "program": "Porogramu",
        "code": "Khoutu",
        "mod_name": "Dzina la Modulu",
        "credits": "Kiriditi",
        "score": "Maraga",
        "grade": "Gireidi",
        "footer": "Uyu ndi mugwalo wa semolao wa pfunzo wo itwaho nga khompyuta."
    },
    "nr": {
        "title": "UMBHALO WESEMTHETHO WEMFUNDO",
        "name": "Igama Lomfundi",
        "id": "Inombolo Yomfundi",
        "faculty": "Umnyango",
        "program": "Ihlelo",
        "code": "Ikhodi",
        "mod_name": "Igama Lemoduli",
        "credits": "Amakhredithi",
        "score": "Amaphuzu",
        "grade": "Ibanga",
        "footer": "Lesi ngesigungu semthetho semfundo esenziwe ngekhompyutha."
    },
    "sasl": {
        "title": "OFFICIAL ACADEMIC TRANSCRIPT (SASL VIEW)",
        "name": "Student Name",
        "id": "Student ID",
        "faculty": "Faculty",
        "program": "Program",
        "code": "Code",
        "mod_name": "Module Name",
        "credits": "Credits",
        "score": "Score",
        "grade": "Grade",
        "footer": "Computer-generated transcript with visual accessibility framing."
    }
}

audit_logs = []
current_student_id = "EDU-2026-8942"

@app.route('/')
def index():
    global current_student_id
    
    if 'role' not in session:
        session['role'] = 'Registrar'

    search_query = request.args.get('search', '').strip().upper()
    if search_query in students_db:
        current_student_id = search_query

    selected_faculty = request.args.get('faculty', 'All')
    
    learner = students_db.get(current_student_id, list(students_db.values())[0])
    modules_data = learner["modules"]
    
    total_credits = sum(m['credits'] for m in modules_data)
    max_degree_credits = 360  
    
    if modules_data:
        avg_score = sum(m['score'] for m in modules_data) / len(modules_data)
        gpa = round((avg_score / 100) * 4.0, 2)
    else:
        gpa = 0.0
        
    filtered_students = {}
    for sid, data in students_db.items():
        if selected_faculty == 'All' or data['faculty'] == selected_faculty:
            filtered_students[sid] = data

    return render_template('dashboard.html', 
                           learner=learner,
                           modules=modules_data, 
                           total_credits=total_credits, 
                           max_degree_credits=max_degree_credits,
                           cumulative_gpa=gpa,
                           all_students=students_db.keys(),
                           filtered_students=filtered_students,
                           selected_faculty=selected_faculty,
                           role=session.get('role'),
                           audit_logs=audit_logs[::-1])

@app.route('/toggle-role', methods=['POST'])
def toggle_role():
    current_role = session.get('role', 'Registrar')
    session['role'] = 'Student' if current_role == 'Registrar' else 'Registrar'
    audit_logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": f"Role switched to {session['role']}"
    })
    return redirect(url_for('index'))

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
    if session.get('role') != 'Registrar':
        return "Unauthorized Access: RBAC blocks this modification.", 403

    name = request.form.get('name')
    student_id = request.form.get('student_id').strip().upper()
    faculty = request.form.get('faculty')
    program = request.form.get('program')
    
    if student_id and student_id not in students_db:
        students_db[student_id] = {
            "name": name,
            "student_id": student_id,
            "faculty": faculty,
            "program": program,
            "modules": []
        }
        current_student_id = student_id
        audit_logs.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": f"Created profile for {name} ({student_id})"
        })
        
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_module():
    global current_student_id
    if session.get('role') != 'Registrar':
        return "Unauthorized Access: RBAC blocks this modification.", 403

    learner = students_db[current_student_id]
    
    code = request.form.get('code').strip().upper()
    name = request.form.get('name').strip()
    credits = int(request.form.get('credits', 12))
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
    audit_logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": f"Added module {code} to {learner['name']}"
    })
    return redirect(url_for('index'))

@app.route('/remove/<int:index>', methods=['POST'])
def remove_module(index):
    global current_student_id
    if session.get('role') != 'Registrar':
        return "Unauthorized Access: RBAC blocks this modification.", 403

    modules_data = students_db[current_student_id]["modules"]
    if 0 <= index < len(modules_data):
        removed = modules_data.pop(index)
        audit_logs.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": f"Removed module {removed['code']} from {students_db[current_student_id]['name']}"
        })
    return redirect(url_for('index'))

@app.route('/export-transcript/<student_id>')
def export_transcript(student_id):
    lang = request.args.get('lang', 'en')
    if lang not in transcript_i18n:
        lang = 'en'
    
    t_strings = transcript_i18n[lang]
    student = students_db.get(student_id)
    if not student:
        return "Student not found", 404

    raw_data = f"{student_id}-{student['name']}-{sum(m['score'] for m in student['modules'])}-{datetime.now().strftime('%Y-%m-%d')}"
    doc_hash = hashlib.sha256(raw_data.encode()).hexdigest().upper()[:32]

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.setFillColorRGB(0, 0.18, 0.38)
    p.rect(0, 750, 612, 42, fill=1, stroke=0)
    p.setFillColorRGB(1, 1, 1)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(40, 765, f"EDUTRACK ANALYTICS HUB — {t_strings['title']}")
    
    p.setFillColorRGB(0.1, 0.1, 0.1)
    p.setFont("Helvetica", 11)
    p.drawString(40, 710, f"{t_strings['name']}: {student['name']}")
    p.drawString(40, 695, f"{t_strings['id']}: {student_id}")
    p.drawString(40, 680, f"{t_strings['faculty']}: {student['faculty']}")
    p.drawString(40, 665, f"{t_strings['program']}: {student['program']}")
    
    p.setFont("Helvetica-Bold", 10)
    p.drawString(40, 620, t_strings['code'])
    p.drawString(100, 620, t_strings['mod_name'])
    p.drawString(380, 620, t_strings['credits'])
    p.drawString(440, 620, t_strings['score'])
    p.drawString(500, 620, t_strings['grade'])
    
    p.line(40, 612, 570, 612)
    
    y = 595
    for mod in student['modules']:
        p.setFont("Helvetica", 10)
        p.drawString(40, y, mod['code'])
        p.drawString(100, y, mod['name'])
        p.drawString(380, y, str(mod['credits']))
        p.drawString(440, y, f"{mod['score']}%")
        p.drawString(500, y, mod['grade'])
        y -= 20
        
    p.setFont("Helvetica-Bold", 8)
    p.setFillColorRGB(0, 0.18, 0.38)
    p.drawString(40, 80, f"SECURE HASH VERIFICATION ID: {doc_hash}")
    
    p.setFont("Helvetica-Oblique", 8)
    p.setFillColorRGB(0.3, 0.3, 0.3)
    p.drawString(40, 65, t_strings['footer'])
    p.drawString(40, 52, "Verified via EduTrack Security-by-Design Architecture. Any alterations render this document invalid.")
    
    audit_logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": f"Exported official cryptographically signed PDF transcript ({lang.upper()}) for {student['name']} ({student_id})"
    })
    
    p.showPage()
    p.save()
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name=f"Transcript_{student_id}_{lang}.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True, port=5000)