import json
from abc import ABC, abstractmethod
from pathlib import Path

database = "school_database.json"
data = {"students": [], "teachers": []}

if Path(database).exists():
    with open(database, "r") as f:
        content = f.read()
        if content:
            data = json.loads(content)

def save():
    with open(database, "w") as f:
        json.dump(data, f, indent=4)

class person(ABC):

    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def get_details(self):
        pass

    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email


class student(person):

    def get_roles(self):
        return "student"

    def register(self):
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        roll_no = int(input("Enter your roll no: "))
        subject = input("Enter your subject: ")
        email = input("Enter your email: ")

        if not person.validate_email(email):
            print("Invalid email format")
            return

        for i in data["students"]:
            if i["roll_no"] == roll_no:
                print("Roll no already exists")
                return

        data["students"].append({
            "name": name,
            "age": age,
            "roll_no": roll_no,
            "subject": subject,
            "email": email,
            "grades": {}
        })

        save()
        print(f"Student {name} registered")

    def get_details(self):
        pass

    def grades(self):
        roll_no = int(input("Tell your roll no: "))
        subject = input("Subject: ")
        marks = float(input("Marks: "))

        for i in data["students"]:
            if i["roll_no"] == roll_no:
                i["grades"][subject] = marks
                save()
                print("Grades added successfully")
                return

        print("Student not found")


class teachers(person):

    def get_roles(self):
        return "teachers"

    def register(self):
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        roll_no = int(input("Enter your roll no: "))
        subject = input("Enter your subject: ")
        email = input("Enter your email: ")

        if not person.validate_email(email):
            print("Invalid email format")
            return

        for i in data["teachers"]:
            if i["roll_no"] == roll_no:
                print("Roll no already exists")
                return

        data["teachers"].append({
            "name": name,
            "age": age,
            "roll_no": roll_no,
            "subject": subject,
            "email": email
        })

        save()
        print(f"Teacher {name} registered")

    def get_details(self):
        pass


while True:
    print("\n===== School Management System =====")
    print("1. Student Registration")
    print("2. Teacher Registration")
    print("3. Add Grades")
    print("4. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        student().register()

    elif choice == 2:
        teachers().register()

    elif choice == 3:
        student().grades()

    elif choice == 4:
        print("Thank you!")
        break

    else:
        print("Invalid choice")