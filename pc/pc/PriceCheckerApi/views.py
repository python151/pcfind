from django.shortcuts import render
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.request import FancyURLopener
from database.models import PC
import requests
from user_agent import generate_user_agent

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
    headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
    r = requests.get(quote_page, headers=headers)
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

        try: 
            s1 = s.find_all('tr')
            cpuV, ramV, gpuV = 0, 0, 0
            print(s1)
            for ss in s1:
                try:
                    s2 = ss.find('th')
                    s3 = ss.find('td')
                except:
                    break

                print("for 1 started \n\n\n\n\n\n\n\n\n\n")
                print(s2, s3)
                base = s2.text.replace(' ', '')
                print(base)
                if base == 'Processor':
                    cpuV = int(s3.text.split(' G')[0].replace(' ', ''))
                if base == 'RAM':
                    ramV =int(s3.text.split(' G')[0].replace(' ', ''))
                if base == 'CardDescription':
                    if s3.text != 'Dedicated':
                        iGpu = True
                        gpuV = 1
                if base == 'GraphicsCardRamSize' and not iGpu:
                    v = s3.text
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
            try: 
                val = PC.objects.create(name=soup.find('span', attrs={'id':'productTitle'}).text,
                link = quote_page,
                price =int(soup.find('span', attrs={'id':'priceblock_ourprice'}).text.replace('$', '').split('.')[0].replace(',', '')),
                cpu = cpuV,
                gpu = gpuV,
                ram = ramV
                )
                val.save()
                print(cpuV, ramV, gpuV)
            except: print("problem")
        except: print("prob1")
    return 'h'


    
        




