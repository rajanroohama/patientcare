from django import forms
from .models import Inpatients, Doctor, Ward, Newborn, Nurse, Cleaningstaff, Careplan, Discharge, Transfer

class InpatientsForm(forms.ModelForm):
    class Meta:
        model = Inpatients
        fields = ['patientid', 'name', 'phn', 'address', 'gender', 'age', 'doct', 'admsndate', 'roomno', 'bystander']
        widgets = {
            'admsndate': forms.DateInput(attrs={'type': 'date'}),
            'doct': forms.Select(),
            'roomno': forms.Select(),
        }

class NewbornForm(forms.ModelForm):
    class Meta:
        model = Newborn
        fields=['name','gender','date','time','weight','blood','type']

class WardForm(forms.ModelForm):
    class Meta:
        model=Ward
        fields=['ward','roomno','roomtype']


class CareplanForm(forms.ModelForm):
    class Meta:
        model = Careplan
        fields = ['name', 'assessment', 'diagnosis', 'inference', 'planning', 'intervention', 'rationale', 'evaluation']
        widgets = {
            'assessment': forms.Textarea(),
            'diagnosis': forms.Textarea(),
            'inference': forms.Textarea(),
            'planning': forms.Textarea(),
            'intervention': forms.Textarea(),
            'rationale': forms.Textarea(),
            'evaluation': forms.Textarea(),
        }

class NurseForm(forms.ModelForm):
    class Meta:
        model = Nurse
        fields = ['name', 'shift', 'ward', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class CleaningStaffForm(forms.ModelForm):
    class Meta:
        model = Cleaningstaff
        fields = ['name', 'shift', 'ward', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
class DischargeForm(forms.ModelForm):
    class Meta:
        model = Discharge
        fields = ['name', 'dischargedate', 'time']
        widgets = {
            'dischargedate': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['name', 'transto', 'date', 'time', 'mode']
        widgets = {
            'dischargedate': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }