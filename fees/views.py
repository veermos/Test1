from django.shortcuts import render, redirect
from .forms import FeesForm
from .models import Fees
from account.forms import StudentForm
# from django.contrib.auth import authenticate, login

def dashboard(request):
    # ddate1=DueDates.objects.get(pk=1)
    # ddate2=DueDates.objects.get(pk=2)
    # feess = Fees.objects.filter(student=request.user)
    student=request.user
    feess = student.fees_set.all()
    #totalfees = feess.aggregate(Sum('value'))

    return render(request, 'fees/dashboard.html', {'feess':feess})

def addfees(request):
    if request.method == 'GET':
        # feess = Fees.objects.filter(student=request.user.id)
        return render(request, 'fees/addfees.html', {'form':FeesForm()})
    else:
        if request.POST['kind'] == "دراسية":
            # add try: except to solve value Error
            try:
                # get the information from the post request and connect it with our form
                form = FeesForm(request.POST)
                # Create newtodo but dont't save it yet to the database
                newfees = form.save(commit=False)
                # set the user to newtodo
                newfees.student = request.user
                newfees.grade = request.user.grade
                newfees.school = request.user.school
                # save newtodo
                newfees.save()
                # update student data
                request.user.study_paid += int(request.POST['value'])
                request.user.save(update_fields=["study_paid"])
                # redirect user to currenttodos page
                return redirect('dashboard')
            except ValueError:
                    # tell user when error hapen
                    return render(request, 'fees/addfees.html', {'form':FeesForm(),'error':'برجاء مراجعة البيانات'})
        else:
            if request.user.bus_active == True:
                # add try: except to solve value Error
                try:
                    # get the information from the post request and connect it with our form
                    form = FeesForm(request.POST)
                    # Create newtodo but dont't save it yet to the database
                    newfees = form.save(commit=False)
                    # set the user to newtodo
                    newfees.student = request.user
                    newfees.grade = request.user.grade
                    newfees.school = request.user.school
                    # save newtodo
                    newfees.save()
                    # update student data
                    request.user.bus_paid += int(request.POST['value'])
                    request.user.save(update_fields=["bus_paid"])
                    # redirect user to currenttodos page
                    return redirect('dashboard')
                except ValueError:
                        # tell user when error hapen
                        return render(request, 'fees/addfees.html', {'form':FeesForm(),'error':'برجاء مراجعة البيانات'})
            else:
                return render(request, 'fees/agreement.html', {'form':StudentForm, 'error' : 'برجاء تحديد منطقة السكن والموافقة علي تعليمات إستخدام الباص'})

def recorded(request):
    feess = Fees.objects.filter(student=request.user.id)
    return render(request, 'fees/recorded.html',{'feess':feess})


def agreement(request):
    if request.method == 'GET':
        return render(request, 'fees/agreement.html')
    else:
        if request.user.bus_active == False:
            try:
                # # get the information from the post request and connect it with our form
                # form = AccountForm(request.POST)
                # # Create newtodo but dont't save it yet to the database
                # newfees = form.save(commit=False)
                # # set the user to newtodo
                # newfees.student = request.user
                # newfees.grade = request.user.grade
                # newfees.school = request.user.school
                # # save newtodo
                # newfees.save()
                # update student data
                request.user.bus_active = True
                request.user.old_bus = request.POST['old_bus']
                request.user.area = request.POST['area']
                request.user.adress = request.POST['adress']
                request.user.save(update_fields=["bus_paid", "bus_active", "old_bus", "area", "adress"])
                # redirect user to currenttodos page
                return redirect('dashboard')
            except ValueError:
                    # tell user when error hapen
                    return render(request, 'fees/agreement.html', {'form':FeesForm(),'error':'برجاء مراجعة البيانات'})
        else:
            return render(request, 'fees/agreement.html', {'form':FeesForm(),'error':'لتعديل البيانات يجب التواصل مع ادارة تشغيل الباصات'})
