from user_module.models import User, StaffModel

def run():
    
    data = [
        ("18BCM524","Kamar"),
        ("18BCM518","Harish"),
        ("18BCM501","Aakass"),
        ("18BCM502","Abinesh"),
        ("18BCM503","Ajay"),
    ]
    
    for rollno, first_name in data:
        if not User.objects.filter(username=rollno).exists():
            User(username=rollno, first_name=first_name, user_type=3, password="1234").save()
            print(rollno,"created")
        else:
            print(rollno,"already created")

    