from bs4 import BeautifulSoup
import requests

# get html from the website
html_text = requests.get('https://wordfinder.yourdictionary.com/wordle/answers/').text

# create instance of BS4 object using extracted html data
soup = BeautifulSoup(html_text, 'lxml')

# pull the years from html
years_raw = soup.find_all('h2', class_ = 'text-headline-4-mobile leading-6.5 text-bold text-black mb-3.5 md:mb-4')

years = []
# remove everything except for the years ('All august 2025 wordle answers' -> '2025')
for line in years_raw: 
    year = line.get_text().split()[-3]
    years.append(year)

tables = soup.find_all('table')

all_data = []

yearCounter = 0

for table in tables:
    for row in table.find('tbody').find_all('tr'):
        cols = row.find_all('td')

        if len(cols) == 3:
            date = cols[0].get_text(strip=True).replace('Today','')
            date = date + " " + years[yearCounter]
            number = cols[1].get_text(strip=True)
            answer = cols[2].get_text(strip=True).replace('Reveal','')
            all_data.append({"Date": date, "Wordle Number": number, "Answer": answer})

    yearCounter += 1

for item in all_data: 
    print(item)