import random

import requests
import csv
from bs4 import BeautifulSoup
from string import ascii_lowercase
import time

user_agent = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'}

def brojanjeStranica(url):
    response = requests.get(url, headers=user_agent )
    print(response.status_code)
    soup = BeautifulSoup(response.text,"html.parser")
    try:
        broj_stranica = soup.findAll('a', {"class": "page-numbers"})
        najveca_stranica = int(broj_stranica[len(broj_stranica) - 2].text)
    except:
        najveca_stranica = 1
    return najveca_stranica

def writeToFile(tr):
    csvFile = open("Result.csv", 'a', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)
    try:
        for cell in tr:
            th = cell.find_all('th')
            th_data = [col.text.strip('\n').strip() for col in th]
            td = cell.find_all('td')
            row = [i.text.replace('\n', '').strip() for i in td]
            writer.writerow(th_data + row)
    finally:
        csvFile.close()

def prolazakPoStranicama(slovo, najveca_stranica):
    for i in range(najveca_stranica + 1):
        url = "https://www.world-airport-codes.com/alphabetical/country-name/" + slovo + ".html?page=" + str(i)
        response = requests.get(url, headers=user_agent)
        if response.status_code != 200:
            print("Pogreska: " + str(response.status_code))
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            for i in range(len(soup.findAll('table', {"class": "stack2"}))):
                table = soup.findAll('table', {"class": "stack2"})[i]
                tr = table.findAll("tr", {"class": ["light-row", "dark-row"]})
                writeToFile(tr)
        except:
            continue

def prolazakPoSlovima():
    for slovo in ascii_lowercase:
        # if slovo >= 'v': #pocni od slova..
            temp = random.randint(5, 24)  # random cekanje iz razloga da stranica nema konstantan promet i blokira ga
            print("Cekanje " + str(temp) + " sec")
            time.sleep(temp)
            najveca_stranica = brojanjeStranica("https://www.world-airport-codes.com/alphabetical/country-name/" + slovo + ".html?page=1")
            print("Pocinjem raditi slovo: " + slovo + ". Broj stranica:  " + str(najveca_stranica))
            prolazakPoStranicama(slovo, najveca_stranica)

if __name__ == "__main__":
    prolazakPoSlovima()
