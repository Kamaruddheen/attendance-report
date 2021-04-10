from django.shortcuts import render

from attendancess.models import AttendanceIdModel, AttendanceModel


def dashboard_view(request):
    labels = []
    data = []
    Present = 0
    Absent = 0

    queryset = AttendanceModel.objects.order_by('attendance_id')
    for clas in queryset:
        labels.append(clas.rollno)
        if clas.status == 'Present':
            # data.append(1)
            Present += 1
        elif clas.status == 'Absent':
            Absent += 1
            # data.append(0)

    total = float(Present) + float(Absent)
    Present_per = "{:.2f}".format((Present / total) * 100)
    Absent_per = "{:.2f}".format((Absent / total) * 100)

    data = [Present_per, Absent_per]

    # context =
    return render(request, "dashboard/dashboard.html", {
        'labels': labels,
        'data': data,
    })


# Particular student data
def student_details(request):
    rollno = request.POST.get('rollno', None)
    # print(rollno)
    data = AttendanceModel.objects.filter(
        rollno=rollno).order_by('attendance_id')
    details = {
        'data': data
    }   
    return render(request, "dashboard/dashboard.html", details)
