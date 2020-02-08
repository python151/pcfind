from django.shortcuts import render
from database.models import Group, PC, Task

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
                "name" : j.name,
                "id" : j.id,
            })
        ret.append({
            "name" : i.name,
            "options" : opt
        })

    return ret

def findPC(request):
    q = request.session.get('q')
    qs = []
    for i in q:
        qs.append(Task.objects.filter(id=i.get('id')).get())
    highest = {
        'cpu' :  qs[0].cpu,
        'gpu' : qs[0].gpu,
        'ram' : qs[0].ram,
    }
    for i in qs:
        if i.cpu > highest.get('cpu'):
            highest['cpu'] = i.cpu
        if i.gpu > highest.get('gpu'):
            highest['gpu'] = i.gpu
        if i.ram > highest.get('ram'):
            highest['ram'] = i.ram
    return {'pcs' : PC.objects.filter(cpu=highest.get('cpu'), gpu=highest.get('gpu'), ram=highest.get('ram')).all()}
        
        
    

