class AcademicTracker:

  def __init__(self, modules=None):
    self.modules = modules or []

  def calculate_gpa(self):
    grade_points = {
        "A": 4.0,
        "A-": 3.7,
        "B+": 3.3,
        "B": 3.0,
        "B-": 2.7,
        "C+": 2.3,
        "C": 2.0,
        "F": 0.0,
    }
    total_points = 0.0
    total_credits = 0

    for module in self.modules:
      grade = module.get("grade", "F")
      credits = module.get("credits", 0)
      points = grade_points.get(grade, 0.0)

      total_points += points * credits
      total_credits += credits

    if total_credits == 0:
      return 0.0

    return round(total_points / total_credits, 2)

  def total_earned_credits(self):
    return sum(
        m.get("credits", 0) for m in self.modules if m.get("score", 0) >= 50
    )