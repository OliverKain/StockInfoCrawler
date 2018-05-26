import requests
import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
import urllib.request


def get_average_annual(mode):
    # Get response
    if mode == 'core500':
        res = requests.get('https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/1467271812595.ajax'
                           + '?tab=average')
    elif mode == 'frontier100':
        res = requests.get('https://www.ishares.com/us/products/239649/ishares-msci-frontier-100-etf/1467271812595.ajax'
                           + '?tab=average')
    else:
        pass

    # TODO Get older date
    # res = requests.get('https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/1467271812595.ajax'
    #                    + '?tab=average&asOfDate=20180331')

    # Remove CDATA
    res_html = str(res.content).replace('<![CDATA[', '')
    res_html = res_html.replace(']]>', '')

    # Parse into BS
    soup = BeautifulSoup(res.content, 'lxml')

    # Remove comments
    for div in soup.find_all('a'):
        div.decompose()

    # Get table
    table = soup.find_all('table')[0]
    th1 = table.find('th')
    th1.string = 'Stats'

    # Display info as table
    df = pd.read_html(str(table))
    print(tabulate(df[0], headers='keys', tablefmt='psql'))


def get_cumulative(mode):
    # Get response
    if mode == 'core500':
        res = requests.get('https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/1467271812595.ajax'
                           + '?tab=cumulative')
    elif mode == 'frontier100':
        res = requests.get('https://www.ishares.com/us/products/239649/ishares-msci-frontier-100-etf/1467271812595.ajax'
                           + '?tab=cumulative')
    else:
        pass

    # TODO Get older date
    # res = requests.get('https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/1467271812595.ajax'
    #                    + '?tab=cumulative&asOfDate=20180331')

    # Remove CDATA
    res_html = str(res.content).replace('<![CDATA[', '')
    res_html = res_html.replace(']]>', '')

    # Parse into BS
    soup = BeautifulSoup(res.content, 'lxml')

    # Remove comments
    for div in soup.find_all('a'):
        div.decompose()

    # Get table
    table = soup.find_all('table')[0]
    th1 = table.find('th')
    th1.string = 'Stats'

    # Display info as table
    df = pd.read_html(str(table))
    print(tabulate(df[0], headers='keys', tablefmt='psql'))


def get_holdings(mode):
    # Get response
    if mode == 'core500':
        request = urllib.request.Request(
            'https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/1467271812596.ajax'
            + '?fileType=csv&fileName=IVV_holdings&dataType=fund')
    elif mode == 'frontier100':
        request = urllib.request.Request(
            'https://www.ishares.com/us/products/239649/ishares-msci-frontier-100-etf/1467271812596.ajax'
            + '?fileType=csv&fileName=FM_holdings&dataType=fund')
    else:
        pass
    opener = urllib.request.build_opener()
    response = opener.open(request)
    with open('holding.csv', 'wb+') as f:
        # Get holding info only
        lines = response.read().splitlines(True)[10:]
        for line in lines:
            f.write(line)

    # Print top 10 holdings
    df = pd.read_csv('holding.csv')[:10]
    print(tabulate(df, headers='keys', tablefmt='psql'))


print('iShares Core S&P 500 ETF')
print('Average Annual:')
get_average_annual('core500')
print('Cumulative:')
get_cumulative('core500')
print('Cumulative:')
get_cumulative('core500')
print('Holdings:')
get_holdings('core500')

print('iShares MSCI Frontier 100 ETF')
print('Average Annual:')
get_average_annual('frontier100')
print('Cumulative:')
get_cumulative('frontier100')
print('Holdings:')
get_holdings('frontier100')
