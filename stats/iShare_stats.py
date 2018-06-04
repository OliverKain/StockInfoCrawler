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
        return

    # Get older date info
    # res = requests.get('https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/1467271812595.ajax'
    #                    + '?tab=average&asOfDate=20180331')

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
    print("\n")


def get_cumulative(mode):
    # Get response
    if mode == 'core500':
        res = requests.get('https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/1467271812595.ajax'
                           + '?tab=cumulative')
    elif mode == 'frontier100':
        res = requests.get('https://www.ishares.com/us/products/239649/ishares-msci-frontier-100-etf/1467271812595.ajax'
                           + '?tab=cumulative')
    else:
        return

    # Get older date info
    # res = requests.get('https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/1467271812595.ajax'
    #                    + '?tab=cumulative&asOfDate=20180331')

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
    print("\n")


def get_holdings(mode):
    # Get response
    if mode == 'core500':
        request = urllib.request.Request(
            'https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/1467271812596.ajax'
            + '?fileType=csv&fileName=IVV_holdings&dataType=fund')
        remove_column_list = [1, 2, 7, 9, 10, 11]
    elif mode == 'frontier100':
        request = urllib.request.Request(
            'https://www.ishares.com/us/products/239649/ishares-msci-frontier-100-etf/1467271812596.ajax'
            + '?fileType=csv&fileName=FM_holdings&dataType=fund')
        remove_column_list = [1, 2, 7, 9, 10, 11, 13, 14]
    else:
        return
    opener = urllib.request.build_opener()
    response = opener.open(request)
    with open('holding.csv', 'wb+') as f:
        # Get holding info only
        if mode == 'core500':
            # Only get top 10
            lines = response.read().splitlines(True)[10:21]
        else:
            lines = response.read().splitlines(True)[10:]
        for line in lines:
            f.write(line)

    df = pd.read_csv('holding.csv')
    filtered_df = df.drop(df.columns[remove_column_list], axis=1)
    if mode == 'frontier100':
        # Filter for Vietnam
        filtered_df = filtered_df.loc[df['Country'] == 'Vietnam']
    print(tabulate(filtered_df, headers='keys', tablefmt='psql'))
    print("\n")


def get_keyfact(mode):
    # Get response
    if mode == 'core500':
        request = requests.get("https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/")
        keyfact_soup = BeautifulSoup(request.content, "html.parser")
        keyfact_item_list = keyfact_soup.find("div", {"id": "c1467271812603"}) \
                                        .find("div", {"class": "mobile-collapse"}) \
                                        .find("div").find("div", {"class": "product-data-list data-points-en_US"}) \
                                        .find_all("div")
    elif mode == 'frontier100':
        request = requests.get("https://www.ishares.com/us/products/239649/ishares-msci-frontier-100-etf#/")
        keyfact_soup = BeautifulSoup(request.content, "html.parser")
        keyfact_item_list = keyfact_soup.find("div", {"id": "c1467271812603"}) \
                                        .find("div", {"class": "mobile-collapse"}) \
                                        .find("div").find("div", {"class": "product-data-list data-points-en_US"}) \
                                        .find_all("div")
    else:
        return
    del keyfact_item_list[len(keyfact_item_list) - 1]
    exported_keyfact_list = []
    for factor in keyfact_item_list:
        caption_span = factor.find("span", {"class": "caption"})
        factor_name = caption_span.contents[0].strip()
        as_of_date_str = caption_span.find("span", {"class": "as-of-date"}).text.strip()
        if as_of_date_str:
            factor_name += " (" + as_of_date_str + ")"
        exported_keyfact_list.append(
            {"Factor": factor_name, "Value": factor.find("span", {"class": "data"}).text.strip()})
    df = pd.DataFrame(exported_keyfact_list)
    print(tabulate(df, headers='keys', tablefmt='psql'))
    print("\n")


print('------------------------------------------------------------------------------------------------------------')
print('iShares Core S&P 500 ETF')
print('------------------------------------------------------------------------------------------------------------')
print('Average Annual:')
get_average_annual('core500')
print('Cumulative:')
get_cumulative('core500')
print('Holdings:')
get_holdings('core500')
print('Key Facts:')
get_keyfact('core500')


print('------------------------------------------------------------------------------------------------------------')
print('iShares MSCI Frontier 100 ETF')
print('------------------------------------------------------------------------------------------------------------')
print('Average Annual:')
get_average_annual('frontier100')
print('Cumulative:')
get_cumulative('frontier100')
print('Holdings:')
get_holdings('frontier100')
print('Key Facts:')
get_keyfact('frontier100')
