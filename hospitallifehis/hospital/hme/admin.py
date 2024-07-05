from django.contrib import admin
from .models import Ward,Nurse,Cleaningstaff,Doctor,Inpatients,Newborn,Discharge,Transfer,Careplan

# Register your models here.

admin.site.register(Ward)
admin.site.register(Nurse)
admin.site.register(Cleaningstaff)
admin.site.register(Doctor)
admin.site.register(Inpatients)
admin.site.register(Newborn)
admin.site.register(Discharge)
admin.site.register(Transfer)
admin.site.register(Careplan)