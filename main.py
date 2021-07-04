from bs4 import BeautifulSoup
import requests
import random
import time  #used time.sleep() to avoid getting blocked by the website for sending too many requests in a given amount of time ("rate limiting")
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

#using different user agents to avoid considering as a bot by the website
def getheader():
    lines = open('user-agents.txt').read().splitlines()
    return random.choice(lines)

#this function extracts the data and writes it under .csv file
def func(url, headers):
    soup = getsoup(url, headers)
    time.sleep(3)

    page_table = soup.find('table', class_ = 'table persist-area SearchResultsTable')
    time.sleep(3)

    rows = page_table.find_all('tr')
    for row in rows:
        try:
            part = row.find('td', class_ = 'column part-column hide-xsmall')
            time.sleep(0.2)
            div_prt = part.find('div', class_ = '')
            time.sleep(0.2)
            txt = div_prt.find('label').getText()
            print(txt)
            time.sleep(0.1)

            msp = row.find('td', class_ = 'column mfr-column hide-xsmall').getText()
            print(msp)
            time.sleep(0.1)

            last = row.find('td', class_ = 'column text-center hide-xsmall')
            time.sleep(0.2)
            stockno = last.find('span', class_ = 'available-amount').getText()
            time.sleep(0.2)
            print(stockno)
            writer.writerow([remove(str(txt)), remove(str(msp)), remove(str(stockno))])
        except:
            time.sleep(0.5)
    return soup
            
#this is the start function
def main_func(url):
    while True:
        headers = {"User-agent": getheader()}
        soup = func(url, headers)
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
    main_func(url)
