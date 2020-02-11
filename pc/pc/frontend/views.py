from django.shortcuts import render, redirect
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
    g = req["group"]

    jsonAwnser = formJSONAwnser(q)

    if request.session.get('q') == None:
        request.session['q'] = [jsonAwnser]
    
    if request.session.get('group') == None:
        request.session['group'] = []

    try:
        if request.session.get('group')[0] == 'undefined':
            ww = request.session.get('group')
            ww.pop(0)
            request.session['group'] = ww
    except: pass

    if a == 'remove':
        c = request.session.get('q')
        c.pop(c.index(jsonAwnser))
        request.session['q'] = c

        s = request.session.get('group')
        if s != None and s != [None]:
            print(s)
            a1 = s.index(g)
            s.pop(a1)
        request.session['group'] = s
    elif a == 'add':
        c = request.session.get('q')
        if jsonAwnser not in c:
            c.append(jsonAwnser)
            request.session['q'] = c
        print(g)
        c1 = request.session.get('group')
        c1.append(g)
        request.session['group'] = c1
    print(request.session.get('q'), request.session.get('group'))

    return render(request, "ok")

def statPage(request):
    page = request.GET.get('page', None)
    pages = ["about", "privacy-policy", "what-we-do", "cookie-policy"]
    try:
        if page in pages:
            pageAdapted = page.replace('-', ' ')
            request.session['page'] = pageAdapted.title()
            ret = render(request, "static/"+page+'.html')
        else:
            raise ValueError("page not allowed")
    except ValueError:
        request.session['page'] = "404"
        ret = render(request, "404.html")
    return ret

