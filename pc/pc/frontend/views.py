from django.shortcuts import render, redirect
from PriceCheckerApi.views import amazon, ebay, amazonFill, amazonGPUFill
import json
from database.models import Group, Task, Email
from database.views import GetGroups, findPC
from django.views.decorators.csrf import csrf_protect
# functions

def notSeen(request, id):
    if {'id' : id} in request.session.get('q'): return False
    return True

# Static Pages
def index(request):
    '''
    index page view
    '''
    request.session['page'] = 'Home'
    return render(request, 'index.html', {
        "words" : [
            " smarter",
            " better",
            " brilliant",
            " genius",
            "n amazing",
            " superior",
        ]
    })

def statPage(request, name):
    page = name
    pages = ["about", "privacy-policy", "what-we-do", "cookie-policy", "shout-out"]
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

# Dynamic Pages

def getPCs(request):
    request.session['page'] = 'PC Select'
    if request.method == 'GET':
        if len(request.session.get('q')) == 0:
            return redirect('/survey')
        return render(request, "pcList.html", findPC(request))

def servey(request):
    request.session['page'] = 'Servey'
    if request.method == 'GET': 
        return render(request, "servey.html", {
            'options' : GetGroups(),
            's' : request.session.get('q')
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
    return int(q)
    

@csrf_protect
def select(request):
    req = request.POST.dict()

    q = int(req["question"])
    a = req["awnser"]
    g = req["group"]

    jsonAwnser = formJSONAwnser(q)

    if request.session.get('q') == None:
        request.session['q'] = [jsonAwnser]
    
    if request.session.get('group') == None:
        request.session['group'] = []

    try:
        if request.session.get('group')[0] == 'undefined':
            group = request.session.get('group')
            group.pop(0)
            request.session['group'] = group
    except: pass

    if a == 'remove':
        c = request.session.get('q')
        c.pop(c.index(jsonAwnser))
        request.session['q'] = c

        s = request.session.get('group')
        if s != None and s != [None]:
            a1 = s.index(g)
            s.pop(a1)
        request.session['group'] = s
    elif a == 'add':
        c = request.session.get('q')
        if jsonAwnser not in c:
            c.append(jsonAwnser)
            request.session['q'] = c
        c1 = request.session.get('group')
        c1.append(g)
        request.session['group'] = c1

    return render(request, "ok")

def lesson(request, lessonName):
    lessons=["how-do-computers-work"]
    if lessonName in lessons:
        request.session['page'] = "Learn"
        return render(request, "learn/"+lessonName+'.html')
    else:
        request.session['page'] = "404"
        return render(request, '404.html')

def mailingListSignUp(request):
    req = request.POST.dict()

    ref = req.get("ref")

    name = req.get("name")
    email = req.get("email")

    try: Email.objects.filter(email=email).get()

    except:
        if name != "" and email != "":
            databaseObj = Email.objects.create(name=name.title(), email=email.lower())
            databaseObj.save()
    
    return redirect(ref)


