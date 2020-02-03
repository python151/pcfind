from django.shortcuts import render, redirect
from parts.models import Part
from PriceCheckerApi.views import amazon


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

def select(request):
    req = request.POST.getdict()

    question = req["question"]
    awnser = req["awnser"]

    jsonAwnser = formJSONAwnser(question, awnser)

    if a == 'remove':
        request.session['q'].pop(request.session['q'].index(jsonAwnser))
    elif a == 'add':
        request.session['q'].append(jsonAwnser)

    return "ok"

def getPCs(request):
    request.session['page'] = 'PC Select'
    if request.method == 'GET':
        return render(request, "pcList.html", findPC(request))

def servey(request):
    request.session['page'] = 'Servey'
    if request.method == 'GET':
        return render(request, "servey.html")




