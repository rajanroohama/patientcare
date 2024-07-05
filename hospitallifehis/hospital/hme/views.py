from django.shortcuts import render, redirect, get_object_or_404
from .forms import InpatientsForm, NewbornForm,WardForm, CareplanForm,NurseForm,CleaningStaffForm, DischargeForm, TransferForm
from .models import Inpatients, Newborn, Ward, Nurse, Cleaningstaff,Careplan, Discharge, Transfer
from django.db.models import Q
from django.db.models import Max

def index(request):
    inpatient_count = Inpatients.objects.count()
    bed_count = Ward.objects.count()
    newborn_count = Newborn.objects.count()

    context = {
        'inpatient_count': inpatient_count,
        'bed_count': bed_count,
        'newborn_count': newborn_count,
    }
    return render(request, "index.html", context)



def addpatients(request):
    if request.method == "POST":
        form = InpatientsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewpatients')
    else:
        inpatients = Inpatients.objects.filter(status='Active').values_list('roomno_id', flat=True)
        unoccupied_rooms = Ward.objects.exclude(id__in=inpatients).order_by('-pk')
        
        form = InpatientsForm(initial={'roomno': None}) 
        form.fields['roomno'].queryset = unoccupied_rooms

    return render(request, 'addpatients.html', {'form': form})
def viewpatients(request):
    query = request.POST.get('value', '')
    if query:
        patients = Inpatients.objects.filter(Q(name__icontains=query) | Q(address__icontains=query) |
            Q(patientid__icontains=query)).select_related('doct', 'roomno').order_by('-pk')
    else:
    
        discharge_patients = Discharge.objects.all().values_list('name_id', flat=True)
        patients = Inpatients.objects.exclude(patientid__in=discharge_patients).order_by('-pk')
        # patients = Inpatients.objects.select_related('doct', 'roomno').order_by('-pk')
    
    return render(request, 'viewpatients.html', {'patients': patients})

def editpatient(request, patient_id):
    patient = get_object_or_404(Inpatients, pk=patient_id)
    
    if request.method == "POST":
        form = InpatientsForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('viewpatients')
    else:
        form = InpatientsForm(instance=patient)
        unoccupied_rooms = Ward.objects.filter(inpatients__isnull=True) | Ward.objects.filter(pk=patient.roomno.pk)
        form.fields['roomno'].queryset = unoccupied_rooms

    return render(request, 'editpatient.html', {'form': form})


def newborndetails(request):
    if request.method == "POST":
        form = NewbornForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewnewborn')
    else:
        form = NewbornForm()

    inpatients = Inpatients.objects.all()

    return render(request, 'newborndetails.html', {'form': form, 'inpatients': inpatients})



def viewnewborn(request):
    query = request.POST.get('value', '')
    if query:
        newborns = Newborn.objects.select_related('name', 'name__roomno').filter(Q(name__name__icontains=query) | Q(name__patientid__icontains=query))
    else:
        newborns = Newborn.objects.select_related('name', 'name__roomno').all()

    return render(request, 'viewnewborn.html', {'newborns': newborns})


def addbed(request):
    if request.method=='POST':
        form=WardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewward')
    else:
        form=WardForm()
    return render(request,'addbed.html',{'form':form})



def addnurse(request):
    if request.method == 'POST':
        form = NurseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewnurse')
    else:
        form = NurseForm()
    return render(request, 'addnurse.html', {'form': form, 'wards': Ward.objects.all()})


def viewnurse(request):
    nurses = Nurse.objects.annotate(max_id=Max('id')).order_by('-max_id')

    if request.method == 'POST':
        name_query = request.POST.get('name', '')

        if name_query:
            nurses = nurses.filter(name__icontains=name_query)

    return render(request, 'viewnurse.html', {'nurses': nurses})


def addstaff(request):
    if request.method == 'POST':
        form = CleaningStaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewcleaningstaff')
    else:
        form = CleaningStaffForm()
    return render(request, 'addstaff.html', {'form': form, 'wards': Ward.objects.all()})


def viewcleaningstaff(request):
    query = request.POST.get('value', '')
    if query:
        cleaning_staffs = Cleaningstaff.objects.filter(Q(name__icontains=query) | Q(ward__ward__icontains=query))
    else:
        cleaning_staffs = Cleaningstaff.objects.all()
    
    return render(request, 'viewcleaningstaff.html', {'cleaning_staffs': cleaning_staffs})
def viewcleaningstaff(request):
    query = request.POST.get('value', '')
    if query:
        cleaning_staffs = Cleaningstaff.objects.filter(Q(name__icontains=query) | Q(ward__ward__icontains=query))
    else:
        cleaning_staffs = Cleaningstaff.objects.all().order_by('-id') 
    
    return render(request, 'viewcleaningstaff.html', {'cleaning_staffs': cleaning_staffs})
def viewward(request):
    status = request.GET.get('status', None)

    all_patients = Inpatients.objects.all()
    # room_id_list = all_patients.values_list('roomno_id', flat=True)
    inpatients = all_patients.filter(status='Active').values_list('roomno_id', flat=True)
    wards = Ward.objects.all()
    unoccupied_rooms = wards.exclude(id__in=inpatients).order_by('-pk')
    occupied_rooms = wards.filter(id__in=inpatients).order_by('-pk')

    if request.method == 'POST':
        query = request.POST.get('value', '')
        if query:
            wards = wards.filter(roomtype__icontains=query)

    if status == 'occupied':
        wards = occupied_rooms
    elif status == 'unoccupied':
        wards = unoccupied_rooms
    
    ward_statuses = []
    for ward in wards:
        ward_info = {
            'ward': ward.ward,
            'roomno': ward.roomno,
            'roomtype': ward.roomtype,
            'status': 'occupied' if ward.id in inpatients else 'unoccupied'
        }
        ward_statuses.append(ward_info)

    return render(request, "viewward.html", {
        'wards': wards,
        'unoccupied_rooms': unoccupied_rooms,
        'occupied_rooms': occupied_rooms,
        'ward_statuses': ward_statuses,
    })

    # return render(request, "viewward.html", {'wards': wards,'unoccupied_rooms':unoccupied_rooms,
    #     'occupied_rooms':occupied_rooms})


def nursingcareplan(request):
    patients = Inpatients.objects.filter(status__in=['Active', 'Admitted'])

    if request.method == 'POST':
        form = CareplanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewplan')  
    else:
        form = CareplanForm()

    return render(request, 'nursingcareplan.html', {'form': form, 'patients': patients})


def viewplan(request):
    careplans = Careplan.objects.select_related('name', 'name__doct').filter(name__status__in=['Active', 'Admitted']) 

    if request.method == 'POST':
        query = request.POST.get('query', '')

        if query:
            careplans = careplans.filter(
                Q(name__patientid__icontains=query) |
                Q(name__name__icontains=query)
            )

    return render(request, 'viewplan.html', {'careplans': careplans})

def transfer(request):
    patients = Inpatients.objects.filter(status__in=['Active', 'Admitted'])

    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            transfer_instance = form.save()
            patient = transfer_instance.name
            patient.status = 'Transferred'
            patient.save()
            
            
            patient.roomno.inpatients = None
            patient.roomno.save()
            
            return redirect('viewtransfer')
    else:
        form = TransferForm()

    return render(request, 'transfer.html', {'form': form, 'patients': patients})



def viewtransfer(request):
    transfers = Transfer.objects.all().order_by('-date')
    return render(request, 'viewtransfer.html', {'transfers': transfers})

def discharge(request):
    patients = Inpatients.objects.filter(status__in=['Active', 'Admitted'])

    if request.method == 'POST':
        form = DischargeForm(request.POST)
        if form.is_valid():
            discharge_instance = form.save()
            patient = discharge_instance.name
            patient.status = 'Discharged'
            patient.save()
        
            patient.roomno.inpatients = None
            patient.roomno.save()
            
            return redirect('viewdischarge')
    else:
        form = DischargeForm()

    return render(request, "discharge.html", {'form': form, 'patients': patients})


def viewdischarge(request):
    discharges = Discharge.objects.all().order_by('-dischargedate')  
    return render(request, "viewdischarge.html", {'discharges': discharges})
