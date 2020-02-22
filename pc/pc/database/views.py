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
    print(q)
    choiceObj = Choice.objects.create()
    qs = []
    try: 
        for i in q:
            iObj = Task.objects.filter(id=i).get()
            iObj.selected = iObj.selected+1
            iObj.save()
            choiceObj.tasks.add(iObj)
            qs.append(iObj)

    except:
        return {}

    for i in request.session.get('group'):
        g = Group.objects.filter(id=i).get()
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
    cpu__range=(highest.get('cpu'), 4),
    gpu__range=(highest.get('gpu'), 5),
      ram__range=(highest.get('ram'), 4)).order_by("price")
    
    for pc in pcs:
        if pcs.filter(name=pc.name, price=pc.price).all().count() != 1:
            pc.delete()

    if pcs.count() != 0:
        return {'pcs' : pcs, 'pcCount' : pcs.count()}
    else: return {}
        
        
    

