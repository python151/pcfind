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
    return soup.find_all('a', attrs={'class' : 'a-link-normal a-text-normal'})

def amazon(search):
    pages = getAmazonResults(search)
    for i in pages:
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
            for ss in s1:
                try:
                    s2 = ss.find('th')
                    s3 = ss.find('td')
                except:
                    break

                base = s2.text.replace(' ', '')
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
            try: 
                val = PC.objects.create(name=soup.find('span', attrs={'id':'productTitle'}).text,
                link = quote_page,
                price =int(soup.find('span', attrs={'id':'priceblock_ourprice'}).text.replace('$', '').split('.')[0].replace(',', '')),
                cpu = cpuV,
                gpu = gpuV,
                ram = ramV
                )
                val.save()
            except: pass
        except: pass
    return None

class options:
    options = [
        {
            "base" : "Processor",
            "max-1" : 2.1,
            "max-2" : 3.1,
            "max-3" : 4.3,
            "max-4" : 5,
        },
        {
            "base" : "RAM",
            "max-1" : 5,
            "max-2" : 9,
            "max-3" : 17,
            "max-4" : 65,
        },
        {
            "base" : "Graphics Card Ram Size",
            "max-1" : 3,
            "max-2" : 5,
            "max-3" : 8,
            "max-4" : 12,
        },
    ]

def convertToInt(text):
    ret = text.split("G")
    ret = ret[0].replace(" ", "")
    ret = ret.replace("\n", "")
    try: return float(ret)
    except: return 0

def amazonFill(id):
    get = PC.objects.get(id=id)
    if get == None:
        raise ValueError("id not found")
    elif get.cpu != 0:
        raise ValueError("PC specs already filled")
    
    quote_page = get.link
    headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
    r = requests.get(quote_page, headers=headers)
    soup = BeautifulSoup(r.content)

    table = soup.find('table', attrs={'id' : 'productDetails_techSpec_section_1'})
    try: rows = table.find_all('tr')
    except AttributeError: print("fail"); return None

    for row in rows:
        base = row.find("th")
        value = row.find("td")
        baseText = base.text
        valueText = value.text

        integratedGPU = False
        GPURam = 0

        for option in options.options:
            optionBase = option.get("base").replace(" ", "").replace("\n", "")
            if optionBase == "Card Description":
                if valueText != "Dedicated":
                    integratedGPU = True
            elif optionBase == baseText.replace(" ", "").replace("\n", ""):
                highest = -1
                intVal = convertToInt(valueText)
                
                if intVal > option.get("max-3"):
                    highest = 4
                if intVal <= option.get("max-3"):
                    highest = 3
                if intVal <= option.get("max-2"):
                    highest = 2
                if intVal <= option.get("max-1"):
                    highest = 1
                if optionBase == "Processor":
                    get.cpu = highest
                elif optionBase == "RAM":
                    get.ram = highest
                elif integratedGPU:
                    get.gpu = 1
                elif optionBase == "Graphics Card Ram Size":
                    get.gpu = highest+1 
                get.save()
            else:
                pass

def amazonGPUFill(id):
    try: get = PC.objects.get(id=id)
    except: return None
    if get == None:
        raise ValueError("id not found")
    elif get.gpu != 0:
        raise ValueError("GPU specs already filled")
    link = get.link

    quote_page = link
    headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
    r = requests.get(quote_page, headers=headers)
    soup = BeautifulSoup(r.content)

    table = soup.find("table", attrs={'id':'productDetails_techSpec_section_1'})
    try:rows = table.find_all("tr")
    except AttributeError: print("failed"); return None
    for r in rows:
        base = r.find("th").text.replace(" ", "").replace("\n", "")
        val = r.find("td").text.replace(" ", "").replace("\n", "")
        print(base, val)

        if base == "CardDescription":
            print("tested")
            if val == "Integrated":
                print('igpu')
                get.gpu = 1
                get.save()
                break
        
        if base.replace(" ", "") == "GraphicsCardRamSize":
            print('dedicated')
            highest = -1
            intVal = convertToInt(val)
            option = options.options[2]
            if intVal > option.get("max-3"):
                highest = 5
            if intVal <= option.get("max-3"):
                highest = 4
            if intVal <= option.get("max-2"):
                highest = 3
            if intVal <= option.get("max-1"):
                highest = 2
            get.gpu = highest
            get.save()
            break