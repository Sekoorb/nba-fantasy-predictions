from bs4 import BeautifulSoup
import requests
import urllib
import urllib.request
import re

def scrape_depth():
    url = "http://www.espn.com/nba/depth/_/type/full"

    # We use try-except incase the request was unsuccessful because of 
    # wrong URL
    try:
        page = urllib.request.urlopen(url)
    except:
        print("Error opening the URL")

    htmlSource = page.read()  

    soup = BeautifulSoup(htmlSource, 'html.parser')

    even_rows = []
    for evenrows in soup.select('tr[class*="evenrow player-46"]'):
        even_rows.append(evenrows)

    odd_rows = []
    for oddrows in soup.select('tr[class*="oddrow player-46"]'):
        odd_rows.append(oddrows)

    all_players = even_rows + odd_rows

    position = []
    for i in all_players:
        position.append(re.search(r'td>(.*) - ', str(i)).group(1))

    first_name = []
    for i in all_players:
        first_name.append(re.search(r'\d/(.*?)-', str(i)).group(1))

    last_name = []
    for i, n in zip(all_players, first_name):
        last_name.append(re.search(fr'{n}-(.*?)">', str(i)).group(1))

    injury_status = []
    for i in all_players:
        injury_status.append(re.search(r'(IL)', str(i)))

    injury = []
    for i in injury_status:
        if i == None:
            injury.append("active")
        else: 
            injury.append("injured")

    depth_chart = list(zip(position, first_name, last_name, injury))
