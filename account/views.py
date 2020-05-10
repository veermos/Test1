from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
# from fees.models import Fees
from django.db.models import Sum
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'account/loginuser.html', {'form':AuthenticationForm})
    else:
        user = authenticate(request, code=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'account/loginuser.html', {'form':AuthenticationForm, 'error':'برجاء التأكد من الكود وكلمة المرور'})
        else:
            login(request, user)
            return redirect('dashboard')

def home(request):
    return render(request, 'account/home.html')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

# def dashboard(request):
#     # ddate1=DueDates.objects.get(pk=1)
#     # ddate2=DueDates.objects.get(pk=2)
#     # feess = Fees.objects.filter(student=request.user)
#     student=request.user
#     feess = student.fees_set.all()
#     #totalfees = feess.aggregate(Sum('value'))
#
#     return render(request, 'account/dashboard.html', {'feess':feess})
