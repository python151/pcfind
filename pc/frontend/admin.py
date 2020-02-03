from django.contrib import admin
from authentification.views import adminLog, getAdminInfo, adminReg
from django.shortcuts import render, redirect
from parts.models import Part

def adminLogin(request):
    log = adminLogin(request)
    if log == True:
        info = getAdminInfo(request.POST.getdict().get('username'))

        request.session['name'] = info.get('name')
        request.session['id'] = info.get('id')
        request.session['logged_in'] = True

        return redirect('admin/dashboard')
    else:
        return render(request, 'admin/forms/login.html', {'error':log.get('error')})

def adminRegister(request):
    if request.method == 'POST':
        adminReg(request)
        return redirect('admin/login/')
    else: 
        return render(request, 'admin/forms/register.html')

def dashboard(request):
    return render(request, 'admin/dashboard.html')

def cheapest(request):
    if request.method == 'POST':
        return redirect(search(request.POST.getdict().get("q")))
    else: return render(request, 'admin/search.html')