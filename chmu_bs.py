from bs4 import BeautifulSoup
import urllib3
import pandas as pd
import re

start_urls = ['https://www.chmi.cz/files/portal/docs/meteo/opss/pocasicko_nove/st_11464_cz.html', #milesovka
    "https://www.chmi.cz/files/portal/docs/meteo/opss/pocasicko_nove/st_11520_cz.html", #praha-libus
]

def chmi_scraper(start_url):
    http = urllib3.PoolManager()
    response = http.request('GET', start_url)
    soup = BeautifulSoup(response.data, "lxml")

    #Finds everything inside all html <table> tags
    tables = soup.find_all("table")

    #First table - to get city, date and time
    #########################################
    ## Takes first table from tables
    table1 = tables[0]

    ## Extracts texts from rows - each row becomes an item in a list
    texts1 = []
    for row in table1.find_all("tr"):
        row_texts = [cell.get_text() for cell in row.find_all("td")]
        texts1.append(row_texts)

    ## Prepares the data for conversion into csv. Makes dictionary with keys as column names.
    data1 = {
        "city": texts1[0][0],
        "date_time": texts1[1][0], 
        "GPS": texts1[2][0]
    }

    #Second table - to get all the data
    #########################################
    ## Takes second table from tables
    table2 = tables[1]

    ## Extracts texts from rows - each row becomes an item in a list
    texts2 = []
    for row in table2.find_all("tr"):
        row_texts = [cell.get_text() for cell in row.find_all("td")]
        texts2.append(row_texts)

    ## Strips comments that are not static
    keyss = [texts2[i][0]for i in range(1, len(texts2))]
    x = keyss[8]
    y = re.sub("[\(].*?[\)]", "", x)
    keyss[8] = y

    ## Takes data only from the exact time
    texts2_in_time = [row[2] for row in texts2]

    ## Prepares the data for conversion into csv. Makes dictionary with keys as column names.
    data2 = {
        keyss[i]: texts2_in_time[i] for i in range(1, len(keyss))
    }

    #Third table - klimatické údaje
    #########################################
    ## Takes third table from tables
    table3 = tables[2]

    ## Extracts texts from rows - each row becomes an item in a list
    texts3 = []
    for row in table3.find_all("tr"):
        row_texts = [cell.get_text() for cell in row.find_all("td")]
        texts3.append(row_texts)

    ## Takes data only from the exact date
    texts3_in_date = [row[2] for row in texts3]

    ## Prepares the data for conversion into csv. Makes dictionary with keys as column names.
    data3 = {
        texts3[i][0]: texts3_in_date[i] for i in range(1, len(texts3))
    }

    # Merges dictionaries
    data = data1 | data2 | data3
    df = pd.DataFrame(data, index=[0])
    return df

frames = []
for url in start_urls:
    frames.append(chmi_scraper(url))

result = pd.concat(frames)

result.to_csv("chmu_tab.csv", index=False)
