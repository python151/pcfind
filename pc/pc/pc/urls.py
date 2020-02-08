from frontend import views as front
from frontend import admin as ad
"""pc URL Configuration

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

urlpatterns = [
    path('admin/', admin.site.urls), 

    path('ajax/qa/', front.select),

    path('', front.index, name='Home'),
    path('show-me-more', front.showMeMore, name='Show Me More'),

    path('servey', front.servey, name='Servey'),
    path('get-pc', front.getPCs, name='Get PC'),

    path('pourpose', front.pourpose, name='Pourpose'),
    path('presets', front.presets, name='Presets'),
    path('budget', front.budget, name='Budget'),
    path('setups', front.setup, name='Setup'),

    path('pay', front.pay, name='Pay'),
    path('cart', front.cart, name='Cart'),
]
