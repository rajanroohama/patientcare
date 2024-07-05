from django.urls import path
from . import views
urlpatterns = [ 
     
    
path('',views.index,name='index'),
path('addpatients/',views.addpatients,name='addpatients'),
path('viewpatients/',views.viewpatients,name='viewpatients'),
path('editpatient/<int:patient_id>/', views.editpatient, name='editpatient'),
path('newborndetails/',views.newborndetails,name='newborndetails'),
path('viewnewborn/',views.viewnewborn,name='viewnewborn'),
path('addbed/',views.addbed,name='addbed'),
path('addnurse/',views.addnurse,name='addnurse'),
path('viewnurse/',views.viewnurse,name='viewnurse'),
path('addstaff/',views.addstaff,name='addstaff'),
path('viewcleaningstaff/',views.viewcleaningstaff,name='viewcleaningstaff'),
path('viewward/',views.viewward,name='viewward'),
path('nursingcareplan/',views.nursingcareplan,name='nursingcareplan'),
path('viewplan/',views.viewplan,name='viewplan'),
path('transfer/', views.transfer, name='transfer'),
path('viewtransfer/', views.viewtransfer, name='viewtransfer'),
path('discharge/',views.discharge,name='discharge'),
path('viewdischarge/',views.viewdischarge,name='viewdischarge'),


	
]  	
