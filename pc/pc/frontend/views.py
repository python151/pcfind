from django.shortcuts import render, redirect
from parts.models import Part
from PriceCheckerApi.views import amazon, ebay
import json
from database.models import Group, Task
from database.views import GetGroups, findPC

# functions

def notSeen(request, id):
    if {'id' : id} in request.session.get('q'): return False
    return True

# Static Pages
def index(request):
    request.session.flush()
    request.session['page'] = 'Home'
    return render(request, 'index.html')

def pay(request):
    request.session['page'] = 'Pay'
    return render(request, 'pay.html')

def pourpose(request):
    request.session['page'] = 'Pourpose Builds'
    return render(request, 'pourpose.html')

def cart(request):
    request.session['page'] = 'Cart'
    return render(request, 'pourpose.html')

def budget(request):
    request.session['page'] = 'Budget Computers'
    if request.method == 'GET':
        return render(request, 'budget.html')

def setup(request):
    request.session['page'] = 'Full setups'
    if request.method ==  'GET':
        return render(request, 'setup.html')

def showMeMore(request):
    request.session['page'] = 'Show Me More'
    if request.method == 'GET':
        return render(request, 'showMeMore.html')


# Dynamic Pages

def getPCs(request):
    request.session['page'] = 'PC Select'
    if request.method == 'GET':
        return render(request, "pcList.html", findPC(request))

def servey(request):
    request.session['page'] = 'Servey'
    if request.method == 'GET': 
        return render(request, "servey.html", {
            'options' : GetGroups(),
            'notSeen' : notSeen
        })


# Input Views

def presets(request):
    request.session['page'] = 'Presets'
    if request.method == 'GET':
        return render(request, 'presets.html')
    else:
        data = request.POST.getdict()
        try: preset = models.Presets.get(id=data.get('selected'))
        except:
            return redirect('')
        request.session['cart_items'].append(models.Part.get(id=data.get('selected')))
        return redirect('cart')

def formJSONAwnser(q):
    return dict({
        'id' : q
    })

def select(request):
    req = request.POST.dict()

    q = req["question"]
    a = req["awnser"]

    jsonAwnser = formJSONAwnser(q)

    if request.session.get('q') == None:
        request.session['q'] = [jsonAwnser]

    if a == 'remove':
        c = request.session.get('q')
        c.pop(c.index(jsonAwnser))
        request.session['q'] = c
    elif a == 'add':
        c = request.session.get('q')
        if jsonAwnser not in c:
            c.append(jsonAwnser)
            request.session['q'] = c
    print(request.session.get('q'))

    return render(request, "ok")


