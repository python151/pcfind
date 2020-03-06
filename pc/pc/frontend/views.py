from django.shortcuts import render, redirect
from PriceCheckerApi.views import amazon, ebay, amazonFill, amazonGPUFill
import json
from database.models import Group, Task, Email, Lesson, PC
from database.views import GetGroups, findPC
from django.views.decorators.csrf import csrf_protect
# functions

def notSeen(request, id):
    if {'id' : id} in request.session.get('q'): return False
    return True

# Static Pages

# index page
def index(request):
    '''
    index page view
    '''
    request.session['page'] = 'Home'
    return render(request, 'index.html', {
        "words" : [# these are that get chosen on the home page
            " smarter",
            " better",
            " brilliant",
            " genius",
            "n amazing",
            " superior",
        ]
    })

# these are the rest of static pages
def statPage(request, name):
    # defining variables
    page = name
    pages = ["about", "privacy-policy", "what-we-do", "cookie-policy", "shout-out", "contact-us"]
    try:
        # check if view allowed
        if page in pages:
            pageAdapted = page.replace('-', ' ')
            request.session['page'] = pageAdapted.title()
            ret = render(request, "static/"+page+'.html')
        else:
            # if not allowed raise error
            raise ValueError("page not allowed")
    except ValueError:
        # except error and return 404 (not found) page
        request.session['page'] = "404"
        ret = render(request, "404.html")
    return ret

# Dynamic Pages

def getPCs(request): 
    '''
        View to get the computers from the database
    '''
    request.session['page'] = 'Choose'
    if request.method == 'GET':
        # making sure they have taken the survey
        if len(request.session.get('q')) == 0:
            return redirect('/survey')
        # running the function to find the pc's and returning it to the template
        return render(request, "pcList.html", findPC(request))

def servey(request):
    '''
        View for survey
    ''' 
    request.session['page'] = 'Servey'
    if request.method == 'GET':
        # checking method is correct and returning the template with the current selected tasks 
        return render(request, "servey.html", {
            'options' : GetGroups(),
            's' : request.session.get('q')
        })


# Input Views
def formJSONAwnser(q):
    ''' useless function for the point of dynamicacy and I didn't want to recode the entire select view '''
    return int(q)
    

@csrf_protect
def select(request):
    '''
        For user to select and unselect tasks
    '''
    # getting request vars
    req = request.POST.dict()
    
    # defining vars for request
    q = int(req["question"])
    a = req["awnser"]
    g = req["group"]

    jsonAwnser = formJSONAwnser(q)

    # checking for failures
    if request.session.get('q') == None:
        request.session['q'] = [jsonAwnser]
    
    if request.session.get('group') == None:
        request.session['group'] = []

    # checking that frontend didn't fail
    try:
        if request.session.get('group')[0] == 'undefined':
            group = request.session.get('group')
            group.pop(0)
            request.session['group'] = group
    except: pass

    # removing or adding var to 'q' variable in session
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
    '''
        View for lessons
    '''
    try: 
        # adjusting name
        lessonName = lessonName.replace("-", " ")
        lessonName = lessonName.title()

        # pulling Lesson object from database
        les = Lesson.objects.filter(name= lessonName ).get()
        
        # Handling home section
        request.session['page'] = "Learn"
        if lessonName == "Home":
            ret = [] 
            lessons=Lesson.objects.all()
            for i, l in enumerate(lessons):
                ret.append({"name":l.name.replace("-", " ").title(), "url":l.name.replace(" ", "-"), "description":l.description})
            ret.pop(1)
            return render(request, "learn/home.html", {
                "lessons" : ret
            })
        
        # returning template
        return render(request, "learn/"+les.htmlFileName)
    except FileNotFoundError:
        # accepting incorrect lesson link and returning 404
        request.session['page'] = "404"
        return render(request, '404.html')

def mailingListSignUp(request):
    '''
        Allows user to sign up for mailing list and return to current page
    '''
    # getting request vars and adapting them to standard vars
    req = request.POST.dict()

    ref = req.get("ref")

    name = req.get("name")
    email = req.get("email")

    # Checking if email is already registered and registering the email
    try: Email.objects.filter(email=email).get()

    except:
        if name != "" and email != "":
            databaseObj = Email.objects.create(name=name.title(), email=email.lower())
            databaseObj.save()
    
    # Redirecting back to current page
    return redirect(ref)

def whyThis(request, id):
    '''
        Will allow users to see what we considered when choosing this computer
    '''
    # getting PC objects from database
    try:
        pc = PC.objects.filter(id=id).get()
    except NotFoundError:
        return render(request, '404.html')
    
    # rendering templage with PC object
    request.session['page'] = "Why This?"
    return render(request, "why-this.html", {
        "pc":pc
    })