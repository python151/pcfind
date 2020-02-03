from django.shortcuts import render
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

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
    print(quote_page)
    page = urllib.request.urlopen(quote_page)
    soup = BeautifulSoup(page)
    return soup.findAll('div', attrs={'class' : 'a-link-normal a-text-normal'})['href']

def amazon(search):
    pages = getAmazonResults(search)
    ret = []
    for i in page:
        quote_page = 'https://www.amazon.com/s?k='+search
        page = urllib.request.urlopen(quote_page)
        soup = BeautifulSoup(page)
        s = soup.find('div', attrs={'id' : 'HLCXComparisonTable'})
        ret.append(s)
    return ret 


    
        




