from bs4 import BeautifulSoup
import requests
import pandas as pd

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
            date = cols[0].get_text(strip=True).replace('Today','').replace('.','')
            date = date + " " + years[yearCounter]
            number = cols[1].get_text(strip=True)
            answer = cols[2].get_text(strip=True).replace('Reveal','')
            all_data.append({"Date": date, "Wordle Number": number, "Answer": answer})

    yearCounter += 1

df = pd.DataFrame(all_data)

testDate = df['Date'].iloc[0]

# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
# link to set the format of our date 
# %b = abbreviated month 
# %d = day of the month 0 padded
# %Y = year padded with century 
# not necessary to pass in format however I want to ensure pandas parses date correctly

# strftime to convert pandas datetime object to a string representaiton of desired format
# in my case I want full weekday name (%A)
testDateUpdated = pd.to_datetime(testDate, format = '%b %d %Y').strftime('%A')

# -------------------------------------------------------------------------
# originally used this method work around .strftime not working on series 

# dates = df['Date'].tolist()
# df['Weekday'] = pd.to_datetime(dates, format = '%b %d %Y').strftime('%A')
#--------------------------------------------------------------------------

# this is a cleaner way to apply datetime properties to a series without the need for a list
# https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.html
# by using .dt before .strftime we can apply datetime properties to series values 
# also removed format when converting to datetime object since it causes no issues 
df['Weekday'] = pd.to_datetime(df['Date']).dt.strftime('%A')


# example of how I would get wordles that were released on a monday 
# mondayWordles = df.loc[df['Weekday'] == 'Monday']

# creating a column 'Ends with Y' to check if wordle answer ends with Y
# binary classification (0/1)
 
df['Ends in Y'] = df['Answer'].str.endswith('Y').astype(int)

# check for repeating characters 

test_word = df['Answer'].iloc[1]
print()
print("Word: ", test_word)
print(f"{test_word} has repeating letters: {len(set(test_word)) != len(test_word)}")
print(f"{test_word} has repeating letters: {int(len(set(test_word)) != len(test_word))}")
print()