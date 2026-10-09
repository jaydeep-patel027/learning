from functools import wraps

PASS_MARK = 40   

def grade(marks):
    """Turn an average mark into a grade letter. (The guide shows A/B; this
    version adds C and F so that failing students get a sensible grade.)"""
    if marks >= 75:
        return "A"
    if marks >= 60:
        return "B"
    if marks >= PASS_MARK:
        return "C"
    return "F"

def read_students(rows):
    for row in rows:
        yield row          # pause here, hand back one student

def average(*marks):          # marks is a tuple
    if len(marks) == 0:       # safety: avoid dividing by zero
        return 0.0
    return sum(marks) / len(marks)

def log_call(func):
    @wraps(func)                          # keeps the original name/docstring
    def wrapper(*args, **kwargs):         # accepts whatever func accepts
        print("-> calling", func.__name__)
        result = func(*args, **kwargs)
        print("<- finished", func.__name__)
        return result
    return wrapper



@log_call
def make_report(name, *marks, **info):    
    avg = average(*marks)                
    shown_marks = ", ".join(str(m) for m in marks) if marks else "none"

    rows = [
        ("Student", name),
        ("Marks", shown_marks),
        ("Average", f"{avg:.2f}"),
        ("Grade", grade(avg)),
        ("Result", "PASS" if avg >= PASS_MARK else "FAIL"),
    ]
    for key, value in info.items():     
        rows.append((key.title(), value))

    return "\n".join(f"  {label:<8}: {value}" for label, value in rows)


def build_records(rows):
    records = []
    for student in read_students(rows):                 # one student per step
        info = {key: value for key, value in student.items()
                if key not in ("name", "marks")}        # dict comprehension
        records.append({
            "name": student["name"],
            "marks": student["marks"],
            "average": average(*student["marks"]),
            "info": info,
        })
    return records


def run_class(title, rows):
    print("\n" + "=" * 46)
    print(f"  {title}")
    print("=" * 46)

    records = build_records(rows)

    passed = [r for r in records if r["average"] >= PASS_MARK]

    print(f"\nPassed ({len(passed)} of {len(records)}):")
    for r in passed:
        print(f"  {r['name']:<8} average {r['average']:.2f}")

  
    ranked = sorted(records, key=lambda r: r["average"], reverse=True)

   
    print("\nRanked report (highest average first):")
    for rank, r in enumerate(ranked, start=1):
        print(f"\n--- Rank {rank} ---")
        print(make_report(r["name"], *r["marks"], **r["info"]))

def part_one_demos():
    print("=" * 46)
    print("  PART 1: TESTING EACH TOOL ON ITS OWN")
    print("=" * 46)

    print("\n[Generator] pulling students one at a time with next():")
    gen = read_students([{"name": "Riya"}, {"name": "Arjun"}, {"name": "Meera"}])
    print("  first :", next(gen))
    print("  second:", next(gen))
    print("  third :", next(gen))

    print("\n[*args] average() with 1, 3 and 5 marks:")
    print("  average(80)                 =", average(80))
    print("  average(50, 70, 90)         =", average(50, 70, 90))
    print("  average(60, 70, 80, 90, 100) =", average(60, 70, 80, 90, 100))

    print("\n[**kwargs] make_report() WITH extra details:")
    print(make_report("Riya", 50, 70, 90, city="Pune", club="Chess"))
    print("\n[**kwargs] make_report() with NO extra details:")
    print(make_report("Arjun", 45, 52))

    # Lambda: sort in both directions to see what the key does.
    print("\n[Lambda] ranking with sorted(key=lambda ...):")
    people = [{"name": "Riya", "marks": 82},
              {"name": "Arjun", "marks": 45},
              {"name": "Meera", "marks": 91}]
    high_first = sorted(people, key=lambda s: s["marks"], reverse=True)     #descending order
    low_first = sorted(people, key=lambda s: s["marks"])        #ascending order
    print("  highest first:", [p["name"] for p in high_first])
    print("  lowest first :", [p["name"] for p in low_first])

   
    print("\n[List comprehension] filtering marks at or above 40:")
    marks = [35, 72, 40, 88, 51, 23, 67]
    passed = [m for m in marks if m >= 40]
    print("  marks  =", marks)
    print("  passed =", passed, f"({len(passed)} of {len(marks)})")

   
    print("\n[Generator, big class] counting passes among 200,000 students")
    print("  without ever storing all 200,000 in a list:")

    def fake_big_class(n):
        for i in range(n):
            yield {"name": f"Student{i}", "marks": [20 + i % 70, 30 + i % 60]}

    count = sum(1 for s in fake_big_class(200_000)
                if average(*s["marks"]) >= PASS_MARK)
    print(f"  {count} students passed (only one student held in memory at a time)")


class_a = [
    {"name": "Riya",  "marks": [50, 70, 90],     "city": "Pune"},
    {"name": "Arjun", "marks": [45, 38, 52],     "club": "Chess"},
    {"name": "Meera", "marks": [91, 88, 95],     "city": "Delhi", "club": "Drama"},
    {"name": "Kabir", "marks": [30, 25, 38]},
    {"name": "Sana",  "marks": [62, 70, 58, 66], "city": "Surat"},
    {"name": "Dev",   "marks": [40, 40, 40]},
]

class_b = [
    {"name": "Tara",   "marks": [85]},                                 
    {"name": "Omkar",  "marks": [20, 35, 30, 25, 40]},                  
    {"name": "Isha",   "marks": [75, 80, 70],  "club": "Robotics"},
    {"name": "Nikhil", "marks": [55, 45, 60],  "city": "Nashik"},
    {"name": "Zoya",   "marks": [39, 41]},                              
]

if __name__ == "__main__":
    part_one_demos()
    run_class("PART 2: CLASS A", class_a)
    run_class("PART 2: CLASS B", class_b)

