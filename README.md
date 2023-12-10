# Student Attendance Management System (SAMS)

Digitally tracks student attendance across any number of courses and classrooms. Automates timetable creation and attendance recording to save teachers time. Intuitive neumorphic UI design provides administrators, staff and students with accessible visibility. Manage schedules and attendance without hassle.

## Key Features

- Record and track daily student attendance 
- Multiple user roles with different permissions (admin, teachers and students)
- Modern, visually appealing Neumorphism UI design

## Tools & Technologies

| Frontend | Backend | Framework + Library |
| -- | -- | -- |
| <a src="https://www.w3schools.com/html/"><img src="https://img.icons8.com/color/48/000000/html-5.png"/></a><a src="https://www.w3schools.com/css/"><img src="https://img.icons8.com/color/48/000000/css3.png"/></a><a src="https://www.javascript.com/"><img style="border-radius:50%;" src="https://img.icons8.com/color/48/000000/javascript.png"/></a><a src="https://sass-lang.com/">&nbsp;<img height="40" src="https://sass-lang.com/assets/img/logos/logo.svg"/></a><a src="https://github.com/"><img src="https://img.icons8.com/color/48/000000/github--v1.png"/></a> | <a src="https://www.python.org/"><img src="https://img.icons8.com/color/48/000000/python.png"/></a><a src="https://sqlite.org/">&nbsp;<img style="border-radius:10%;" height="45" src="https://avatars.githubusercontent.com/u/48680494"/></a> | <a src="https://getbootstrap.com/"><img src="https://img.icons8.com/color/48/000000/bootstrap.png"/></a><a src="https://www.djangoproject.com/">&nbsp;<img height="45" src="https://avatars.githubusercontent.com/u/27804"/></a><a src="https://jquery.com/">&nbsp;<img height="45" src="https://avatars.githubusercontent.com/u/70142"/></a><a src="https://api.jquery.com/jQuery.ajax/">&nbsp;<img style="border-radius:50%;" height="45" src="https://raw.githubusercontent.com/github/explore/8be26d91eb231fec0b8856359979ac09f27173fd/topics/ajax/ajax.png"/></a><a src="https://www.chartjs.org/">&nbsp;<img height="45" src="https://avatars.githubusercontent.com/u/10342521"/></a> |

## Usage

The application has three core user interfaces:

**Admin Panel:** Allows administrative users to configure system settings and manage other users. Can generate timetables and review attendance metrics.

**Teacher Portal:** Teachers can take attendance for each class and submit it to the system. Review class rosters and download attendance reports.  

**Student View:** Students are able to view their personal attendance record for all classes along with their schedule.

## Getting Started

### To run locally

Once you downloaded project, Run this following command
```
pip install -r requirements.txt
```
Next
```
python manage.py runserver
```

(Optional) 

In order to start livereload, run below command in first terminal 
```
python manage.py livereload
```
then, below command in another terminal
```
python manage.py runserver
```
Then, Go to: https://localhost:8000 or http://127.0.0.1:8000

### Login Credentials

The easiest way to test the application is to login with the demo accounts:

| Account | Admin | Hod | Staff |
|--|--|--|--|
|Username| testadmin | hod1 | --all staff account-- |
|Password| testpass | Testpass123 | teststaff |

<!-- - #### Student accounts
     - username : 18BCM552	
    - password : test4321

    - username : 18BCM516
    - password : test4321 -->

## Contributions

Pull requests are welcome! Feel free to browse open issues to find areas for improvement.

<a href="https://github.com/Kamaruddheen/attendance-report/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Kamaruddheen/attendance-report" />
</a>