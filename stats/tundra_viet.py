import pandas as pd
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from lxml import html


def tundraviet():
    page = requests.get('https://www.bloomberg.com/quote/TUNDVIE:SS')
    soup = html.fromstring(page.content)
    ytd = soup.xpath('//*[@id="content"]/div/div[1]/div[1]/div/div[6]/div/div[4]/div[2]')
    ytd = ytd[0]
    ytd = ytd.text

    return ytd


def tundranav():
    page = requests.get('https://www.bloomberg.com/quote/TUNDVIE:SS')
    soup = html.fromstring(page.content)
    nav = soup.xpath('//*[@id="content"]/div/div[1]/div[8]/div/div/div[9]/div[2]')
    date = soup.xpath('//*[@id="content"]/div/div[1]/div[8]/div/div/div[9]/div[1]')
    nav = nav[0]
    nav = nav.text
    date = date[0]
    date = date.text

    print('NAV hiện tại                         : ', date, nav)


def tundraviet_aum():
    page = requests.get('https://www.bloomberg.com/quote/TUNDVIE:SS')
    soup = html.fromstring(page.content)
    aum = soup.xpath('//*[@id="content"]/div/div[1]/div[8]/div/div/div[10]/div[2]')
    aum = aum[0]
    aum = aum.text

    return aum


def holding():
    res = requests.get('https://www.bloomberg.com/quote/TUNDVIE:SS')
    soup = BeautifulSoup(res.content, 'lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))
    print(tabulate(df[0], headers='keys', tablefmt='psql'))


print('YTD Performance Tundra Frontier Fund : ', tundraviet(), '%')
tundranav()
print('AUM của Tundra Frontier fund SEK Bil : ', tundraviet_aum())
print('Khoảng 83-87 mil USD')
print('TOP FUND HOLDINGS')
holding()
