from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import *
from .models import Employee

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

def addEmployee(request):
    employeeform = EmployeeForm()
    if request.method == 'POST':
      #print('Done POSTED:', request.POST)
       employeeform = EmployeeForm(request.POST)
       if employeeform.is_valid():
            employeeform.save()
            messages.success(request, 'Employee is successfully added.')
            return redirect('employee_list')
    else:
        employeeform = EmployeeForm()
    context = {'employeeform': employeeform }

    return render(request, 'add/addEmployee.html', context)

def employeeList(request):
    employees = Employee.objects.all()

    context = {'employees':employees}
    return render(request, 'view/viewEmployee.html', context)

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

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

#Opens up page as PDF
class ViewEmployeePDF(View):
 def get(self, request, *args, **kwargs):
    employees = Employee.objects.all()
    context  = {
            'employees': employees,
        }

    pdf = render_to_pdf('report/print_employee.html', context )
    return HttpResponse(pdf, content_type='application/pdf')

#Automaticly downloads to PDF file
class DownloadEmployeePDF(View):
    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()
        
        context = {'employees': employees,}
		
        pdf = render_to_pdf('print_transaction.html', context )

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" %("12341231")
        content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
########################### Attendance ######

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
        attendanceform = AttendanceForm()
    context = {'attendanceform': attendanceform }
    return render(request, 'add/addAttendance.html', context)

def attendanceList(request):
    attendances = Attendance.objects.all()

    context = {'attendances':attendances}
    return render(request, 'view/viewAttendance.html', context)

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

def viewAttendance(request, attendance_id):
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

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

#Opens up page as PDF
class ViewAttendancePDF(View):
 def get(self, request, *args, **kwargs):
    attendances = Attendance.objects.all()
    context  = {
            'attendances': attendances,
        }

    pdf = render_to_pdf('report/print_attendance.html', context )
    return HttpResponse(pdf, content_type='application/pdf')

#Automaticly downloads to PDF file
class DownloadAttendancePDF(View):
    def get(self, request, *args, **kwargs):
        attendances = Attendance.objects.all()
        
        context = {'attendances': attendances,}
		
        pdf = render_to_pdf('print_transaction.html', context )

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" %("12341231")
        content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response


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

def departmentList(request):
    departments = Department.objects.all()

    context = {'departments':departments}
    return render(request, 'view/viewDepartment.html', context)

def viewDept(request, department_id):
    departments = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        # Delete the group
        departments.name = request.POST['name']
        return HttpResponseRedirect(reverse('department_list'))

    context = {
        'departments': departments
    }
    return render(request, 'del/delDept.html', context)


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

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

#Opens up page as PDF
class ViewDeptPDF(View):
 def get(self, request, *args, **kwargs):
    departments = Department.objects.all()
    context  = {
            'departments': departments,
        }

    pdf = render_to_pdf('report/print_dept.html', context )
    return HttpResponse(pdf, content_type='application/pdf')

#Automaticly downloads to PDF file
class DownloadDeptPDF(View):
    def get(self, request, *args, **kwargs):
        departments = Department.objects.all()
        
        context = {'departments': departments,}
		
        pdf = render_to_pdf('print_transaction.html', context )

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" %("12341231")
        content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response