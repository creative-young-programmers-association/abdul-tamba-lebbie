from django.db import models
from datetime import datetime, time, timedelta
# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=255, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    marital_status = models.CharField(max_length=1, choices=[
        ('M', 'Marriage'),
        ('S', 'Single'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ])
    gender = models.CharField(max_length=1, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ])

    def __str__(self):
        return self.name

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    in_time = models.TimeField()
    out_time = models.TimeField()
    total_hours_worked = models.PositiveBigIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.in_time and self.out_time:
            duration = datetime.combine(datetime.today(), self.out_time) - datetime.combine(datetime.today(), self.in_time)
            self.total_hours_worked = duration.total_seconds() / 3600  # convert to hours
        super().save(*args, **kwargs)

    def __str__(self):
        return self.employee
   