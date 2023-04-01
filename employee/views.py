from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import *
from .models import Employee

from .models import *

from django.http import HttpResponseRedirect

from django.contrib import messages

import io
import csv
from django.http import HttpResponse

from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.views.generic import View

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UpdateProfile



@login_required(login_url='login')
def Home(request):

    total_employees = Employee.objects.all()
    total_attendance = Attendance.objects.all()
    total_dept = Department.objects.all()

    employee = total_employees.count()
    attendance = total_attendance.count()
    department = total_dept.count()

    recent_employees = Attendance.objects.order_by('-date')[:5]

    context = {'employee':employee, 'attendance':attendance, 'department':department, 'recent_employees':recent_employees}
    
    return render(request, 'home.html', context)

#@login_required(login_url='login')
#def addEmployee(request):
  #  employeeform = EmployeeForm()
   # if request.method == 'POST':
      #print('Done POSTED:', request.POST)
    #   employeeform = EmployeeForm(request.POST)
     #  if employeeform.is_valid():
     #       employeeform.save()
     #       messages.success(request, 'Employee is successfully added.')
      #      return redirect('employee_list')
    #else:
   #     employeeform = EmployeeForm()
    #context = {'employeeform': employeeform }

    return render(request, 'add/addEmployee.html', context)

@login_required(login_url='login')
def addEmployee(request):
    employeeform = EmployeeForm()
    if request.method == 'POST':
        employeeform = EmployeeForm(request.POST)
        if employeeform.is_valid():
            employeeform.save()
            messages.success(request, 'Employee is successfully added.')
            return redirect('employee_list')
        else:
            for field in employeeform:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    context = {'employeeform': employeeform}
    return render(request, 'add/addEmployee.html', context)



@login_required(login_url='login')
def employeeList(request):
    employees = Employee.objects.all()

    context = {'employees':employees}
    return render(request, 'view/viewEmployee.html', context)

@login_required(login_url='login')
def viewEmployee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        # Process the form data and save the group
        employee.name = request.POST['name']
        employee.employee_id = request.POST['employee_id']
        try:
            department = Department.objects.get(name=request.POST['department'])
            employee.department = department
        except ObjectDoesNotExist:
            
            pass
        employee.position = request.POST['position']
        employee.phone_number = request.POST['phone_number']
        employee.save()
        return HttpResponseRedirect(reverse('employee_list'))

    context = {
        'employee': employee
    }
    return render(request, 'del/delEmployee.html', context)

@login_required(login_url='login')
def del_Employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
       # Delete the group
        employee.delete()
        return HttpResponseRedirect(reverse('employee_list'))

    context = {
        'employee': employee
    }
    return render(request, 'add/delete_Employee.html', context)

########################### Attendance ######

@login_required(login_url='login')
def addAttendance(request):
    attendanceform = AttendanceForm()
    if request.method == 'POST':
      #print('Done POSTED:', request.POST)
       attendanceform = AttendanceForm(request.POST)
       if attendanceform.is_valid():
            attendanceform.save()
            messages.success(request, 'Attendance is successfully added.')
            return redirect('attendance_list')
    else:
        for field in attendanceform:
            for error in field.errors:
                messages.error(request, f"{field.label}: {error}")
    context = {'attendanceform': attendanceform }
    return render(request, 'add/addAttendance.html', context)

def addEmployee(request):
    employeeform = EmployeeForm()
    if request.method == 'POST':
        employeeform = EmployeeForm(request.POST)
        if employeeform.is_valid():
            employeeform.save()
            messages.success(request, 'Employee is successfully added.')
            return redirect('employee_list')
        else:
            for field in employeeform:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    context = {'employeeform': employeeform}
    return render(request, 'add/addEmployee.html', context)


@login_required(login_url='login')
def attendanceList(request):
    attendances = Attendance.objects.all()

    context = {'attendances':attendances}
    return render(request, 'view/viewAttendance.html', context)

@login_required(login_url='login')
def del_Attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    if request.method == 'POST':
       # Delete the group
        attendance.delete()
        return HttpResponseRedirect(reverse('attendance_list'))

    context = {
        'attendance': attendance
    }
    return render(request, 'add/delete_Attendance.html', context)

@login_required(login_url='login')
def viewAttendancePDF(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    if request.method == 'POST':
        # Process the form data and save the group
        try:
            employee = Employee.objects.get(name=request.POST['employee'])
            attendance.employee = employee
        except ObjectDoesNotExist:
            
            pass
        attendance.date = request.POST['date']
        
        attendance.in_time = request.POST['in_time']
        attendance.out_time = request.POST['out_time']
        attendance.total_hours_worked = request.POST['total_hours_worked']
        employee.save()
        return HttpResponseRedirect(reverse('attendance_list'))

    context = {
        'attendance': attendance
    }
    return render(request, 'del/delAttendance.html', context)

@login_required(login_url='login')
def addDepartment(request):
    departmentform = DepartmentForm()
    if request.method == 'POST':
      #print('Done POSTED:', request.POST)
       departmentform = DepartmentForm(request.POST)
       if departmentform.is_valid():
            departmentform.save()
            messages.success(request, 'Department is successfully added.')
            return redirect('department_list')
    else:
        departmentform = DepartmentForm()
    context = {'departmentform': departmentform }
    return render(request, 'add/addDept.html', context)

@login_required(login_url='login')
def departmentList(request):
    departments = Department.objects.all()

    context = {'departments':departments}
    return render(request, 'view/viewDepartment.html', context)

@login_required(login_url='login')
def viewDept(request, department_id):
    departments = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        # Delete the group
        departments.name = request.POST['name']
        departments.save()
        return HttpResponseRedirect(reverse('department_list'))

    context = {
        'departments': departments
    }
    return render(request, 'del/delDept.html', context)


@login_required(login_url='login')
def del_Dept(request, department_id):
    departments = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
       # Delete the group
        departments.delete()
        return HttpResponseRedirect(reverse('department_list'))

    context = {
        'departments': departments
    }
    return render(request, 'add/delete_Dept.html', context)

@login_required(login_url='login')
def attendanceReport(request):
    attendances = Attendance.objects.all()
    return render(request, 'report/attendance1.html', {'attendances': attendances})

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser or user.groups.filter(name='admin').exists():
                return redirect('admin:index')
            else:
                return redirect('Home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'registration/login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutUser(request):
    logout(request)
    next_page = reverse('login')  # Assuming "login" is the name of your login URL pattern
    response = redirect(next_page)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@login_required(login_url='/employee/login/')
def userSetting(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateProfile(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('userSetting')
    else:
        form = UpdateProfile(instance=user)
    return render(request, 'userSetting.html', {'form': form})

@login_required
def password_reset(request):

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'your password has been updated successfully')
            return redirect('password_reset')
            
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'password_reset.html', {'form': form})
    
################# To automatically downling pdf reports #################

def pdf_view(request):
    attendances = Attendance.objects.all()
    # Get the HTML of the webpage
    html = get_template('report/attendanceReport.html').render({'attendances': attendances})
    
    # Create a BytesIO object to hold the PDF data
    buffer = BytesIO()
    
    # Use xhtml2pdf to generate the PDF from the HTML
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), buffer)
    
    # Return the PDF as a response, triggering a file download
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="print_dept.pdf"'
    return response

def employee_pdf_view(request):
    employee = Employee.objects.all()
    # Get the HTML of the webpage
    html = get_template('report/employeeReport.html').render({'employee': employee})
    
    # Create a BytesIO object to hold the PDF data
    buffer = BytesIO()
    
    # Use xhtml2pdf to generate the PDF from the HTML
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), buffer)
    
    # Return the PDF as a response, triggering a file download
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="print_dept.pdf"'
    return response

def department_pdf_view(request):
    department = Department.objects.all()
    # Get the HTML of the webpage
    html = get_template('report/departmentReport.html').render({'department': department})
    
    # Create a BytesIO object to hold the PDF data
    buffer = BytesIO()
    
    # Use xhtml2pdf to generate the PDF from the HTML
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), buffer)
    
    # Return the PDF as a response, triggering a file download
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="print_dept.pdf"'
    return response
