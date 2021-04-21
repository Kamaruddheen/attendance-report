from user_module.models import User, StaffModel

def run():
    
    staffs = ['yuvaraj_sir','saravanan_sir','hema_mam']
    
    for staff in staffs:
        if not User.objects.filter(username=staff).exists():
            User(username=staff, user_type=2, password="1234").save()
            print(staff,"created")
        else:
            print(staff,"already created")

    