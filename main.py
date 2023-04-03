import math
import smtplib
from email.mime.text import MIMEText
def findGrade(pts):
    grades = {0:2,50:2,51:3,60:3,61:3.5,70:3.5,71:4,80:4,81:4.5,90:4.5,91:5,100:5}
    for key1 in grades:
        if pts >= key1:
            for key2 in grades:
                if pts < key2 and grades.get(key1) == grades.get(key2):
                    return grades.get(key1)

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()

if __name__ == '__main__':
    file = open('students.txt', 'r')
    Lines = file.readlines()
    file.close()
    students = []

    for line in Lines:
        arr = line.split(",")
        if len(arr)==4:
            students.append({"email":arr[0], "Imie":arr[1], "Nazwisko":arr[2], "Punkty":arr[3], "Ocena":findGrade(int(arr[3])), "Status":"GRADED"})
        if len(arr)==6:
            students.append({"email": arr[0], "Imie": arr[1], "Nazwisko": arr[2], "Punkty": arr[3], "Ocena": arr[4], "Status":arr[5]})

    answer = input("DODAC czy USUNAC studenta? ")
    if answer == "DODAC":
        line = input("Podaj dane studenta w formacie \"<email>,<imie>,<nazwisko>,<punkty>\": ")
        arr = line.split(",")
        ok = True
        for student in students:
            if student.get("email") == arr[0]:
                ok = False
        if len(arr) == 4 and ok:
            send_email("Ocena", student.get("Ocena"), student.get("email"), "xxx@gmail.com", "xxx")
            students.append({"email": arr[0], "Imie": arr[1], "Nazwisko": arr[2], "Punkty": arr[3], "Ocena": findGrade(int(arr[3])),"Status": "GRADED"})
        if not(ok):
            print("Student już istnieje")

    if answer == "USUNAC":
        line = input("Podaj adres email studenta którego chcesz usunąć: ")
        ok = False
        for student in students:
            if student.get("email") == line:
                students.remove(student)
                ok=True
        if ok:
            print("Usunieto studenta")
        else:
            print("Nie znaleziono studenta")

    for student in students:
        if student.get("Status") != "MAILED":
            send_email("Ocena", str(student.get("Ocena")), student.get("email"),"xxx@gmail.com", "xxx")
            students[students.index(student)] \
                = {"email":student.get("email"), "Imie":student.get("Imie"), "Nazwisko":student.get("Nazwisko")
                , "Punkty":student.get("Punty"), "Ocena":student.get("Ocena"), "Status":"MAILED"}

    filepath = "studentsOut.txt"
    with open(filepath, "w") as file_object:
        for student in students:
            line = student.get("email") +"," +student.get("Imie")+"," +student.get("Nazwisko")+"," +student.get("Punkty")
            line +="," + str(student.get("Ocena"))+"," +student.get("Status") + "\n"
            file_object.write(line)
