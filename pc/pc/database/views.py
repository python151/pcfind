from django.shortcuts import render

# Create your views here.
def findPC(request):
    activities = request.session.get('q')
    for i in activities:
        print(i.get('q'))