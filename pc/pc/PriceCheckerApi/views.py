from django.shortcuts import render
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.request import FancyURLopener
from database.models import PC
import requests

def getEbayResults(search):
    search = urllib.parse.quote_plus(search)
    quote_page = 'https://www.ebay.com/sch/i.html?_nkw='+search
    page = urllib.request.urlopen(quote_page)
    soup = BeautifulSoup(page)
    return soup.findAll('div', attrs={'class' : 's-item__info clearfix'})

def ebay(q):
    results = getEbayResults(q)
    cheapest = results[0]
    for i in results:
        cost = i.find('span', {'class': 's-item__price'}).text
        try: cost = float(cost.replace('$', '').replace(',', ''))
        except: 
            cost = [float(cost.replace('$',
             '').replace(',',
             '').split(' ')[0]),
             float(cost.replace('$',
              '').replace(',',
             '').split(' ')[2])]
        if type(cost) == float and float(cheapest.find('span', {'class': 's-item__price'}).text.replace('$', '')) > cost:
            cheapest = i
    return cheapest.find('a', {'class': 's-item__link'}, href=True)['href']

def getAmazonResults(search):
    search = urllib.parse.quote_plus(search)
    quote_page = 'https://www.amazon.com/s?k='+search

    class MyOpener(FancyURLopener):
        version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Firefox/2.0.0.11'
    myopener = MyOpener()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    r = requests.get(quote_page, headers=headers)
    page = myopener.open(quote_page)
    soup = BeautifulSoup(r.content)
    print(soup.prettify())
    return soup.find_all('a', attrs={'class' : 'a-link-normal a-text-normal'})

def amazon(search):
    pages = getAmazonResults(search)
    print(pages)
    for i in pages:
        print(i['href'])
        quote_page = 'https://amazon.com'+i['href']
        class MyOpener(FancyURLopener):
            version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
        myopener = MyOpener()
        page = myopener.open(quote_page)
        soup = BeautifulSoup(page)
        s = soup.find('table', attrs={'id' : 'productDetails_techSpec_section_1'})

        s1 = s.find_all('tr')
        for s in s1:
            s2 = s.find_all('th')
            base = s2[0].value
            if base == 'Processor':
                cpuV = s2[1].value
            if base == 'RAM':
                ramV = s2[1].value
            if base == 'Card Description':
                if s2[1].value != 'Dedicated':
                    iGpu = True
                    gpuV = 1
            if base == 'Graphics Card Ram Size' and not iGpu:
                v = s2[1].value
                v1 = int(v.replace(' GB', ''))
                if v1 <= 3:
                    gpuV = 2
                elif v1 <= 5:
                    gpuV = 3
                elif v1 <= 8:
                    gpuV = 4
                else:
                    gpuV = 5
        #print(s)
        val = PC.objects.create(name=soup.find('span', attrs={'id':'title'}).value,
        link = quote_page,
        price = soup.find('span', attrs={'id':'price-large'}),
        cpu = cpuV,
        gpu = gpuV,
        ram = ramV
        )
        val.save()
        print(cpuV, ramV, gpuV)
    return 'h'


    
        




