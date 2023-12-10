from timetable.models import TimetableModel, TimetablesetModel
from subject.models import SubjectModel
import csv

def run():
    try:
        fhand = open('scripts/timetable.csv')
    except:
        print("The file is not available")
        exit()
    reader = csv.reader(fhand)
    next(reader)

    for row in reader:
        hour = row[0]
        day = row[1]
        subject = row[2]
        set_name = row[3]
        if not TimetableModel.objects.filter(hour = hour, day = day).exists():
            subject = SubjectModel.objects.get(hour_name = subject)
            set = TimetablesetModel.objects.get(id = set_name)
            TimetableModel(
                hour=hour, 
                day=day, 
                subject=subject, 
                set_name=set).save()
            print(hour,"-",day,"-",subject,"is added.")
        else:
            print(hour,"-",day,"-",subject,"is already there.")

