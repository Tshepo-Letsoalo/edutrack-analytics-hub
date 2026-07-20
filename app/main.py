from flask import Flask, render_template
from models import AcademicTracker

app = Flask(__name__)


@app.route("/")
def dashboard():
  sample_modules = [
      {
          "code": "CS101",
          "name": "Introduction to Computer Science",
          "credits": 4,
          "score": 92,
          "grade": "A",
      },
      {
          "code": "NET201",
          "name": "Communications & Networking",
          "credits": 3,
          "score": 88,
          "grade": "B+",
      },
      {
          "code": "SEC301",
          "name": "Network Protection & Threat Prevention",
          "credits": 3,
          "score": 95,
          "grade": "A",
      },
      {
          "code": "DEV102",
          "name": "Python Software Development",
          "credits": 4,
          "score": 90,
          "grade": "A",
      },
  ]

  tracker = AcademicTracker(sample_modules)
  gpa = tracker.calculate_gpa()
  earned_credits = tracker.total_earned_credits()

  return render_template(
      "dashboard.html",
      modules=sample_modules,
      gpa=gpa,
      earned_credits=earned_credits,
  )


if __name__ == "__main__":
  app.run(debug=True, port=5000)