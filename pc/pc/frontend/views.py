from django.shortcuts import render, redirect
from parts.models import Part
from PriceCheckerApi.views import amazon
import json

# Create your views here.
def index(request):
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

def formJSONAwnser(question, awnser):
    return str({
        'q' : question,
        'a' : awnser
    })

def select(request):
    req = request.POST.dict()

    question = req["question"]
    a = req["awnser"]

    jsonAwnser = formJSONAwnser(question, a)

    if not request.session.get('q'):
        request.session['q'] = []

    if a == 'remove':
        pass#request.session['q'] = request.session.get('q').pop(request.session.get('q').index(jsonAwnser))
    elif a == 'add':
        request.session['q'] = request.session.get('q').append(jsonAwnser)

    return render(request, "ok")

def getPCs(request):
    request.session['page'] = 'PC Select'
    if request.method == 'GET':
        return render(request, "pcList.html", findPC(request))

def servey(request):
    request.session['page'] = 'Servey'
    if request.method == 'GET':
        return render(request, "servey.html", {
            'options' : [
                {
                    "name" : "Productivity",
                    "options" : [
                        {
                            "name" : "video editing"
                        },
                        {
                            "name" : "photo editing"
                        },
                    ]
                },
                {
                    "name" : "Gaming",
                    "options" : [
                        {
                            "name" : "1080p gaming"
                        },
                        {
                            "name" : "1440p gaming"
                        },
                        {
                            "name" : "4k gaming"
                        },
                        {
                            "name" : "triple monitor gaming"
                        },
                        {
                            "name" : "streaming"
                        },
                    ]
                },
            ]
        })




