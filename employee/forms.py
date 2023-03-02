from django import forms

from .models import *


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['employee_id'].widget.attrs.update({'class': 'form-control'})
        self.fields['department'].widget.attrs.update({'class': 'form-control'})
        self.fields['position'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
       

class AttendanceForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.now().strftime("%Y-%m-%d")}))
    in_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'min': datetime.now().strftime("%I:%M %p")}))
    out_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'min': datetime.now().strftime("%I:%M %p")}))
    class Meta:
        model = Attendance
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
        self.fields['in_time'].widget.attrs.update({'class': 'form-control'})
        self.fields['out_time'].widget.attrs.update({'class': 'form-control'})
        self.fields['total_hours_worked'].widget.attrs.update({'class': 'form-control'})

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
       