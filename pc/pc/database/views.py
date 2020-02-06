from django.shortcuts import render
from models import Groups

# Create your views here.
def findPC(request):
    activities = request.session.get('q')
    for i in activities:
        print(i.get('q'))

def GetGroups():
    ret = []
    
    for i in Groups.all():
        opt = []
        for j in i.options.all():
            opt.append({
                "name" : j.name
            })
        {
            "name" : i.name,
            "options" : opt
        }

    return ret

