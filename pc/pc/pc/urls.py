from frontend import views as front

"""
    pc URL Configuration

    The `urlpatterns` list routes URLs to views. For more information please see:
        https://docs.djangoproject.com/en/2.2/topics/http/urls/
    Examples:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), 

    path('ajax/qa/', front.select),

    path('', front.index, name='Home'),

    path('survey', front.servey, name='Servey'),
    path('get-pc', front.getPCs, name='Get PC'),
    path('why-this/<int:id>', front.whyThis, name="Why this"),

    path('learn/<slug:lessonName>', front.lesson, name='Learn'),
    path('stat/<slug:name>', front.statPage, name='Static Page'),

    path('join/mailing-list', front.mailingListSignUp, name="Join Mailing List"),

    path('sign-up', front.signUp, name="Sign Up"),
    path('login', front.login, name="Login"),
    path('logout', front.logout, name="Logout"),

    path('user/dashboard', front.dashboard, name="Dashboard"),
    path('user/pc/save/<int:id>', front.savePC, name="Save PC"),
    path('user/pc/unsave/<int:id>', front.unsavePC, name="Unsave PC"),
    path('user/pc/compare/<int:id>', front.comparePC, name="Compare PC")

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
