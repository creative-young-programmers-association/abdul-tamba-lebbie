from django.urls import path
from . import views
from .views import  pdf_view, department_pdf_view, employee_pdf_view

urlpatterns = [
    path('', views.Home, name='Home'),

    path('add_employee', views.addEmployee, name='add_employee'),

    path('add_attendance', views.addAttendance, name='add_attendance'),

    path('add_department', views.addDepartment, name='add_department'),

    ############View Data#####################

    path('employee_list', views.employeeList, name='employee_list'),

    path('attendance_list', views.attendanceList, name='attendance_list'),

    path('department_list', views.departmentList, name='department_list'),

        ############View Data#####################

    path('dept/<str:department_id>/view/', views.viewDept, name='viewDept'),

    path('employee/<str:employee_id>/delete/', views.del_Employee, name='del_Employee'),

    path('dept/<str:department_id>/delete/', views.del_Dept, name='del_Dept'),

    path('atten/<str:attendance_id>/delete/', views.del_Attendance, name='del_Attendance'),


    path('employee/<str:employee_id>/view/', views.viewEmployee, name='viewEmployee'),

    path('attendance/<str:attendance_id>/view/', views.viewAttendancePDF, name='viewAttendance'),
    
    ############PRINT OUT #####################

    path('attendance_pdf_view/', views.viewAttendancePDF, name="attendance_pdf_view"),

    path('attendanceReport/', views.attendanceReport, name="attendanceReport"),

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('userSetting/', views.userSetting, name="userSetting"),

    path('password_reset/', views.password_reset, name="password_reset"),

    path('attendance1.pdf', pdf_view, name='pdf_view'),

    path('employeereport.pdf', employee_pdf_view, name='employee_pdf_view'),
    path('departmentreport.pdf', department_pdf_view, name='department_pdf_view'),
    


]

