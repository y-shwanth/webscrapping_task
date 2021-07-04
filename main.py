from bs4 import BeautifulSoup
import requests
import random
import time  
import csv

def remove(string):
    return "".join(string.split())

def getsoup(url, headers):
    r = requests.get(url, headers=headers)
    print(r.status_code)
    if r.status_code == 429:
        print(r.headers["Retry-After"])
    print('over')
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

def getnextpage(common_url, soup):
    return common_url + soup.find('a', id = 'lnkPager_lnkNext')['href']
    
def getheader():
    lines = open('user-agents.txt').read().splitlines()
    return random.choice(lines)

#this function extracts the data and writes it under .csv file
def func(url, headers, writer):
    soup = getsoup(url, headers)
    page_table = soup.find('table', class_ = 'table persist-area SearchResultsTable')

    rows = page_table.find_all('tr')
    for row in rows:
        try:
            part = row.find('td', class_ = 'column part-column hide-xsmall')
            div_prt = part.find('div', class_ = '')
            txt = div_prt.find('label').getText()
            print(txt)

            msp = row.find('td', class_ = 'column mfr-column hide-xsmall').getText()
            print(msp)
            
            last = row.find('td', class_ = 'column text-center hide-xsmall')
            stockno = last.find('span', class_ = 'available-amount').getText()
            
            print(stockno)
            writer.writerow([remove(str(txt)), remove(str(msp)), remove(str(stockno))])
        except:
            time.sleep(0.5)
    return soup
            
#this is the start function
def main_func(url, writer):
    while True:
        headers = {"User-agent": getheader()}
        soup = func(url, headers, writer)
        url = getnextpage(common_url, soup)
        if(url == common_url):
            break


common_url = 'https://www.mouser.com'
kws = ['Decoder', 'I2C', 'SPI', 'UART', '2D+Graphics']

for kw in kws:
    url = 'https://www.mouser.com/Search/Refine?Keyword=' + kw
    file = open(str(kw)+'.csv', 'w')
    writer = csv.writer(file)
    writer.writerow(['Manufacturer', 'Mouse part', 'Availability'])
    main_func(url, writer)
    file.close()
