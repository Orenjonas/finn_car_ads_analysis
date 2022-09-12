# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup

import pandas as pd

# def has_numbers(inputString):
#     return any(char.isdigit() for char in inputString)


def get_data_from_second_line(soup, data_dict):
    """
    Extracts:

    Modellår
    Kilometer
    """

    for part in soup.find_all('div', class_='media__body'):

        # Extract the useful parts
        _, title, content, _ = part.text.split('\n')

        # Add data do dictionary
        if title in ('Modellår', 'Kilometer'):

            # Extract numbers from string
            content = str_to_int(content)

            data_dict[title] = content

    return data_dict


def get_page(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    return soup

def get_price(soup, data_dict):
    """
    Return the text part of price.

    :param soup: Soup object containing price of the car
    :type soup: bs4.BeautifulSoup
    :return:
    """

    price = soup.find('span', class_='u-t3').text.strip()
    data_dict['price'] = str_to_int(price)

    return data_dict

2018


def parse_list_in_car_ad_html(soup, data_dict):
    for lists in soup.find_all('dl'):
        for part in lists:

            if 'Batterikapasitet' in str(part):
                data_dict['batterikapasitet'] = part.text.split('\n')[2]
            if 'Effekt' in str(part):
                data_dict['effekt'] = part.text.split('\n')[2]
            if 'Farge' in str(part):
                data_dict['farge'] = part.text.split('\n')[2]
    return data_dict


def str_to_int(string: str) -> int:
    """
    Join a list of all characters in string that are a digit, then covert to int
    """
    return int("".join([s for s in string.split() if s.isdigit()]))


def extract_data_from_page(url):

    data_dict = {}
    soup = get_page(url)
    data_dict = get_price(soup, data_dict)
    data_dict = get_data_from_second_line(soup, data_dict)
    data_dict = parse_list_in_car_ad_html(soup, data_dict)

    return data_dict


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    data = pd.DataFrame(columns = ['price', 'Modellår', 'Kilometer', 'farge', 'effekt', 'batterikapasitet' ])

    # Get search page
    print('Getting search page')
    soup = get_page(url='https://www.finn.no/car/used/search.html?model=1.749.2000264&price_from=100000&price_to=290000&sort=PUBLISHED_DESC')

    # Get section containing ads
    ad_section = soup.find(id="page-results")

    # Parse links
    for ad in ad_section.find_all('a', class_='ads__unit__link', href=True):
        if 'https://www.finn.no' in ad['href']:
            link = ad['href']
        else:
            link = 'https://www.finn.no' + ad['href']

        # Follow link and extract data
        print('extracting data from page: ' + link)
        data_dict = extract_data_from_page(url=link)

        # Add data to the end of the data frame
        data.loc[len(data)] = data_dict

    print(data)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


def check_feature_model(text, fully_charged, charge_plus, charged):
    fully_charged = fully_charged or 'fully charged' in text
    charge_plus = charge_plus or 'charge plus' in text
    charged = charged or 'charged' in text
    return fully_charged, charge_plus, charged

fully_charged = False
charge_plus = False
charged = False
for result in soup.find_all('div', class_='panel'):
    
    match_p = result.find_all('p')
    if match_p:
        for m in match_p:
            intro_text = m.text.lower()
            fully_charged, charge_plus, charged = check_feature_model(intro_text, fully_charged, charge_plus, charged)


# Check feature model in description
description = soup.find('div', class_='u-position-relative').text.lower()
fully_charged, charge_plus, charged = check_feature_model(description, fully_charged, charge_plus, charged)

# fully charged takes prescedence
# TODO

# TODO: loop through all pages
