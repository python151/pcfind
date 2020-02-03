from django.shortcuts import render
from database import models

# Create your views here.
def adminLog(request):
    data = request.POST.getdict()
    email = data.get('email')

    try: 
        user = models.User.objects.get(email=email)

    except DoesNotExist:
        return {'error': 'account not found'}

    password = data.get('password')
    if password == user.password:
        return True
    else:
        return {'error': 'password incorrect'}

def getAdminInfo():
    pass

def adminReg():
    pass

