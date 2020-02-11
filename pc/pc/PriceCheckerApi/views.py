from django.shortcuts import render
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.request import FancyURLopener

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
        version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
    myopener = MyOpener()
    page = myopener.open(quote_page)
    soup = BeautifulSoup(page)
    return soup.find('a', attrs={'class' : 'a-link-normal a-text-normal'}).get('href')

def amazon(search):
    pages = getAmazonResults(search)
    print(pages)
    ret = []
    for i in pages:
        quote_page = 'https://amazon.com'+i
        class MyOpener(FancyURLopener):
            version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
        myopener = MyOpener()
        page = myopener.open(quote_page)
        soup = BeautifulSoup(page)
        s = soup.find('div', attrs={'id' : 'HLCXComparisonTable'})
        ret.append(s)
    print(ret)
    return ret 


    
        




