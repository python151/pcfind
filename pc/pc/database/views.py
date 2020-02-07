from django.shortcuts import render
from database.models import Group

# Create your views here.
def findPC(request):
    activities = request.session.get('q')
    for i in activities:
        print(i.get('q'))

def GetGroups():
    ret = []
    
    for i in Group.objects.all():
        opt = []
        for j in i.options.all():
            opt.append({
                "name" : j.name
            })
        ret.append({
            "name" : i.name,
            "options" : opt
        })

    return ret

