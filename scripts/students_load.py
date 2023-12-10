from user_module.models import User, StaffModel
import csv

def run():
    
    try:
        fhand = open('students.csv')
    except:
        print("The file is not available")
        exit()
    reader = csv.reader(fhand)
    next(reader)
    
    for row in reader:
        rollno = row[0]
        first_name = row[1].lower().capitalize()
        if not User.objects.filter(username=rollno).exists():
            User(username=rollno, first_name=first_name, user_type=3, password=rollno).save()
            print(rollno,"created")
        else:
            print(rollno,"already created")

    