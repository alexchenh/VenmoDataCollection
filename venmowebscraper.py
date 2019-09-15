# import libraries
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

# Create a csv file to write to, add headers row
f = csv.writer(open('venmo-names.csv', 'w'))
f.writerow(['Name1', 'Link1', 'Name2', 'Link2', 'Comment', 'Date'])

# Instantiate list of pages
pages = []
pages.append('https://venmo.com/USERNAME_HERE') # Seed URL

for item in pages:

    # Specify the seed url
    page = requests.get(item)

    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    # Pull all text from the BodyText div
    payment_name_list = soup.find(class_='stories-wrapper')

    # Pull text from all instances of <a> tag within BodyText div
    payment_name_list_items = payment_name_list.find_all('a')
    payment_comment_list_items = payment_name_list.find_all(class_='paymentpage-text m_five_t')
    payment_date_list_items = payment_name_list.find_all(class_='date')

    names = []
    links = []

    for x in range(len(payment_name_list_items)):
        time.sleep(0.3) 
        name = payment_name_list_items[x].contents[0]
        link = 'https://venmo.com/' + payment_name_list_items[x].get('href')
        
        if not (link in pages):
            pages.append(link)

        if x % 2 == 0:
            names.insert(0, name)
            links.insert(0, link)

        if x % 2 == 1:
            names.insert(1, name)
            links.insert(1, link)
            comment = payment_comment_list_items[x//2].contents[0]
            date = payment_date_list_items[x//2].contents[0]
            f.writerow([names[0], links[0], names[1], links[1], comment, date])
