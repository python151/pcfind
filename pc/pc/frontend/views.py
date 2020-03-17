from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login as lin, logout as lout
from django.contrib.auth.models import User, Group

from random import choice as rchoice

from database.models import Group, Task, Email, Lesson, PC, SurveyResults, SavedPcs

from PriceCheckerApi.views import amazon, ebay, amazonFill, amazonGPUFill
from database.views import GetGroups, findPC, userFindPc

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
    possibleWords = [# these are that get chosen on the home page
            " smarter",
            " better",
            " brilliant",
            " genius",
            "n amazing",
            " superior",
        ]
    # checking if word has already been chosen
    if request.session.get("homepageWord") in [None, "", "None"]:
        # choosing word and setting session var
        request.session["homepageWord"] = rchoice(possibleWords)

    # rendering index page
    request.session['page'] = 'Home'
    return render(request, 'index.html')

# these are the rest of static pages
def statPage(request, name):
    # defining variables
    page = name
    pages = ["about", "privacy-policy", "what-we-do", "cookie-policy", "shout-out", "contact-us"]
    try:
        # check if view allowed
        if page in pages:
            # replacing encoded characters in name
            pageAdapted = page.replace('-', ' ')
            pageAdapted = pageAdapted.replace('!', ".")

            # ensuring name is less than 8 chars
            retPageName = []
            for i, char in enumerate(pageAdapted):
                if i <= 8:
                    retPageName.append(char)
                else:
                    retPageName[i-3] = "."
                    retPageName[i-2] = "."
                    retPageName[i-1] = "."
                    break
            retPageName = "".join(retPageName)

            # setting ret var and changing 'page' session var
            request.session['page'] = retPageName.title()
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
        try:
            if len(request.session.get('q')) == 0:
                raise TypeError('No Awnsers Selected')
        except TypeError:
            return redirect("/survey")
        # running the function to find the pc's and returning it to the template
        if request.user.is_authenticated:
            ret = userFindPc(request)
        else:
            ret = findPC(request)
        return render(request, "pcList.html", ret)

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
    c = request.session.get('q')
    c1 = request.session.get('group')
    if a == 'remove':
        # removing input task
        c.pop(c.index(jsonAwnser))
        request.session['q'] = c
        
        # removing input group
        if c1 != None and c1 != [None] and g in c1:
            a1 = c1.index(g)
            c1.pop(a1)
        request.session['group'] = c1
    elif a == 'add':
        if jsonAwnser not in c:
            c.append(jsonAwnser)
            request.session['q'] = c
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

def signUp(request):
    if request.method == 'GET':
        return render(request, "users/signup.html")
    elif request.method == 'POST':
        data = request.POST.dict()
        
        username, email, password = data.get("username"), data.get("email"), data.get("password")
        
        try:
            User.objects.filter(email=email).get()
            return redirect("/login")
        except:
            user = User.objects.create_user(username, email, password)
            user.save()
            sResults = SurveyResults.objects.create(user=user)
            sResults.save()
            request.session['surveyResults'] = sResults
        return redirect('/user/dashboard')

def login(request):
    if request.method == 'GET':
        return render(request, "users/login.html")
    elif request.method == 'POST':
        data = request.POST.dict()
        username, password = data.get("username"), data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            lin(request, user)
            try:
                sr = SurveyResults.objects.filter(user=user).get()
            except:
                s = SurveyResults.objects.create(user=user)
                s.save()
                return redirect('/survey')
            try:
                sr = SavedPcs.objects.filter(user=user).get()
            except:
                sResults = SavedPcs.objects.create(user=user)
                sResults.save()
                return redirect('/survey')
            return redirect('/user/dashboard')
        else:
            return redirect('/login') 

def dashboard(request):
    if request.user.is_authenticated:
        try: 
            request.user.savedpcs
        except:
            saved = SavedPcs.objects.create(user=request.user)
            saved.save()
        
        request.session['savedPCs'] = []
        for d in request.user.savedpcs.saved.all():
            savedPCs = request.session.get('savedPCs')
            savedPCs.append(d.id)
            request.session['savedPCs'] = savedPCs

        return render(request, 'users/dashboard.html')
    else:
        return redirect('/login')

def logout(request):
    lout(request)
    return redirect('/')

@csrf_protect
def savePC(request, id):
    '''
        Veiw for user to save a computer
    '''
    if not request.user.is_authenticated:
        return redirect('/login')

    request.user.savedpcs.saved.add(PC.objects.filter(id=id).get())
    request.user.save()

    request.session['savedPCs'] = []

    for d in request.user.savedpcs.saved.all():
        savedPCs = request.session.get('savedPCs')
        savedPCs.append(d.id)
        request.session['savedPCs'] = savedPCs

    return redirect('/user/dashboard')

@csrf_protect
def unsavePC(request, id):
    '''
        Veiw for user to unsave a computer
    ''' 
    if not request.user.is_authenticated:
        return redirect('/login')

    request.user.savedpcs.saved.remove(PC.objects.filter(id=id).get())
    request.user.save()

    request.session['savedPCs'] = []

    for d in request.user.savedpcs.saved.all():
        savedPCs = request.session.get('savedPCs')
        savedPCs.append(d.id)
        request.session['savedPCs'] = savedPCs

    return redirect('/user/dashboard')

def makePCExplanation(pc):
    ret = "This computer should be good at "

    if pc.ram > 2:
        ret += "multitasking (running multiple programs at once)"
    else:
        ret += "running spreadsheet software, buisiness software, etc."
    if pc.cpu >= 1:
        verb = "decently fast"
        if pc.cpu >= 2: verb = "fast"
        elif pc.cpu >= 3: verb = "light speed"
        ret += " and making calculations "+verb+" (useful for web browsing, buisiness software, etc.)"
    if pc.gpu > 1:
        verb = "ok"
        if pc.gpu > 2: verb = "good"
        if pc.gpu > 3:  verb = "great"
        elif pc.gpu > 4: verb = "god level"
        ret += ". Finally finally it should be excellent at displaying "+verb+" graphics"
    return ret

def comparePC(request, id):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    pc = PC.objects.filter(id=id).get()

    return render(request, 'users/compare.html', {
        'pc' : pc,
        'explanation' : makePCExplanation(pc)
    })