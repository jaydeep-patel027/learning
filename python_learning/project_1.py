name = input("Enter your name: ").strip()

age = int(input("Enter your age: "))

gpa = float(input("Enter your GPA: "))

full_time_answer = input("Full=time? (yes/no): ").strip().lower()
is_full_time = (full_time_answer == "yes")

years_complated = int(input("Years completed: "))

years_left = 4 - years_complated
age_next_year = age + 1


print()
print("====Student Profile ====")
print(f"Name          :{name}")
print(f"Age           :{age}")
print(f"GPA           :{gpa}")
print(f"Full-time     :{is_full_time}")
print(f"Years left    :{years_left}")
print(f"Age next year :{age_next_year}")
print("==========================")