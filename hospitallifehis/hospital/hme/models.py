from django.db import models
from django.utils import timezone

class Ward(models.Model):
    ward = models.CharField(max_length=2)
    roomno = models.CharField(max_length=4, unique=True)
    roomtype = models.CharField(max_length=15)
    

    def __str__(self):
        return f"{self.ward} - {self.roomno}-{self.roomtype}"

class Nurse(models.Model):
    name = models.CharField(max_length=60)
    shift = models.CharField(max_length=30)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.name}-{self.shift}"

class Cleaningstaff(models.Model):
    name = models.CharField(max_length=60)
    shift = models.CharField(max_length=30)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.name}-{self.shift}"

class Doctor(models.Model):
    name = models.CharField(max_length=60)
    dept = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}-{self.dept}"

class Inpatients(models.Model):
    patientid = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=60)
    phn = models.CharField(max_length=10)
    address = models.TextField()
    gender = models.CharField(max_length=10)
    age = models.CharField(max_length=3)
    doct = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    admsndate = models.DateField()
    roomno = models.ForeignKey(Ward, on_delete=models.CASCADE, null=True, blank=True)
    bystander = models.CharField(max_length=40)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.name}-{self.patientid}"

class Newborn(models.Model):
    name = models.ForeignKey(Inpatients, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6)
    date = models.DateField(default=timezone.now)
    time = models.TimeField()
    ampm=models.CharField(max_length=4,default='AM')
    weight = models.CharField(max_length=6)
    blood = models.CharField(max_length=4)
    type = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name}-{self.gender}"

class Discharge(models.Model):
    name = models.ForeignKey(Inpatients, on_delete=models.CASCADE)
    dischargedate = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.name}-{self.dischargedate}"

class Transfer(models.Model):
    name = models.ForeignKey(Inpatients, on_delete=models.CASCADE)
    transto = models.CharField(max_length=60)
    date = models.DateField()
    time = models.TimeField()
    mode = models.CharField(max_length=50)

    def __str__ (self):
        return f"{self.name}-{self.transto}"

class Careplan(models.Model):
    name = models.ForeignKey(Inpatients, on_delete=models.CASCADE)
    assessment = models.TextField()
    diagnosis = models.TextField()
    inference = models.TextField()
    planning = models.TextField()
    intervention = models.TextField()
    rationale = models.TextField()
    evaluation = models.TextField()

    def __str__(self):
        return f"{self.name.name} Care Plan"
