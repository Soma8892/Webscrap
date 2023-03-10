import requests
from bs4 import BeautifulSoup
import pandas as pd

# make a request to the webpage
url = 'https://vegetablemarketprice.com/market/bangalore/today'
response = requests.get(url)

# parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# find the table rows with the class 'todayVetableTableRows'
table_rows = soup.find_all('tr', {'class': 'todayVetableTableRows'})

# create a list to store the data
data = []

# loop through the rows to extract the rates for each vegetable
for row in table_rows:
    cols = row.find_all('td')
    vegetable = cols[1].text
    min_price = cols[2].text.replace('₹', '').strip()
    max_price = cols[3].text.replace('₹', '').strip()
    modal_price = cols[4].text.replace('₹', '').strip()
    unit = cols[5].text.strip()
    data.append([vegetable, min_price, max_price, modal_price, unit])
# create a pandas dataframe with the data
df = pd.DataFrame(data, columns=['Vegetable', 'Min Price', 'Max Price', 'Modal Price', 'Unit'])

# print the dataframe
print(df)
import pyodbc
import pandas as pd

# create a connection to the SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=axim-soma;DATABASE=soma;UID=sa;PWD=Soma@8892')

# create a cursor
cursor = conn.cursor()

for index, row in df.iterrows():
    cursor.execute("INSERT INTO vegetable_prices (vegetable, min_price, max_price, modal_price, unit) values (?, ?, ?, ?, ?)",
        row['Vegetable'], row['Min Price'], row['Max Price'], row['Modal Price'], row['Unit'])

# commit the changes to the database and close the connection
cursor.commit()
conn.close()


