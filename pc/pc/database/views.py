from django.shortcuts import render
from database.models import Group, PC, Task, Choice

# Create your views here.

def GetGroups():
    ret = []

    for i in Group.objects.order_by('selected')[::-1]:
        opt = []
        for j in i.options.order_by('selected')[::-1]:
            opt.append({
                "name" : j.name,
                "id" : j.id,
            })
        ret.append({
            "name" : i.name,
            "options" : opt,
            "id" : i.id
        })
    return ret

def findPC(request):
    try: q = request.session.get('q')
    except: q = []
    choiceObj = Choice.objects.create()
    qs = []
    try: 
        for i in q:
            iObj = Task.objects.filter(id=i.get('id')).get()
            print(iObj.selected)
            iObj.selected = iObj.selected+1
            iObj.save()
            choiceObj.tasks.add(iObj)
            qs.append(iObj)

    except: return {}

    for i in request.session.get('group'):
        g = Group.objects.filter(id=i).get()
        print(g.selected)
        g.selected = g.selected+1
        g.save()
        

        

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

    print(highest)
        
    pcs = PC.objects.filter(
    cpu=highest.get('cpu'),
      ram=highest.get('ram')).order_by("price")
    
    if pcs != []:
        return {'pcs' : pcs}
    else: return {}
        
        
    

