import requests
from bs4 import BeautifulSoup
import pandas as pd

# Get the page url info
page = requests.get('https://www.carpages.ca/used-cars/search/?fueltype_id%5B0%5D=3&fueltype_id%5B1%5D=7')
# Get soup object
soup = BeautifulSoup(page.text, 'lxml')
# Create the data frame and name its columns
df = pd.DataFrame(columns=['Links', 'Name', 'Price', 'Colors'])
# Set a variable to count the pages
page_num = 1
while page_num <= 15:
    # Get all de tags with each car information
    items = soup.find_all('div', class_ = 'media soft push-none rule')
    # Loop through each car tag
    for item in items:
        # Get link, name, price and color
        link = 'https://www.carpages.ca'+item.find('a', class_ = 'media__img media__img--thumb').get('href')
        name = item.find('h4', class_ = 'hN' ).text.strip()
        price = item.find('strong', class_ = 'delta').text.strip()
        color = item.find_all('div', class_ = 'grey l-column l-column--small-6 l-column--medium-4')[1].text.strip()
        # Put all the information of each car tag in a dictinary and create a dataframe with it
        df_2 = pd.DataFrame({'Links':link,'Name': name,'Price': price,'Colors': color}, index=[0])
        # Concatenate the series object with the created data frame
        df = pd.concat([df, df_2])
    # Get the next page link from the soup object
    next_url = soup.find('a', {'title': 'Next Page'}).get('href')
    # Complete the link with the missing part
    next_url_full = 'https://www.carpages.ca'+next_url
    # Get the requests object
    page = requests.get(next_url_full)
    # Get the new soup object
    soup = BeautifulSoup(page.text, 'lxml')
    # Update the counter variable by adding one to it
    page_num += 1
