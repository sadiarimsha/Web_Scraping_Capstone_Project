from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import csv
import json

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.timeanddate.com/weather/")

# Scraping weather forecast for cities

weather = driver.find_elements(By.CSS_SELECTOR,'div.my-city__item')
if len(weather) > 0:
    print(len(weather))

# Data scraping
results = []

for w in weather:
    weather_dict = {}

    try:
        city_name = w.find_element(By.CLASS_NAME,'my-city__city')
        weather_dict ['Title'] = city_name.text
    except NoSuchElementException:
        weather_dict['Title'] = 'N/A'

    try:
        city_weather = w.find_element(By.CLASS_NAME,'my-city__temp')
        weather_dict['Temperature'] = city_weather.text
    except NoSuchElementException:
        weather_dict['Temperature'] = 'N/A'

    try:
        description = w.find_element(By.CLASS_NAME,'my-city__wtdesc')
        weather_dict['Description'] = description.text
    except NoSuchElementException:
        weather_dict['Description'] = 'N/A'

    try:
        city_link = w.find_element(By.CSS_SELECTOR,'a[href^="/weather/"]')
        weather_dict['Link'] = city_link.get_attribute("href")
    except NoSuchElementException:
        weather_dict['Link'] = 'N/A'

    results.append(weather_dict)

print(results)

# Loading raw data into a Pandas DataFrame
df = pd.DataFrame(results)
print(df)

driver.quit()
 
# Writing to CSV
df.to_csv('weather.csv', sep=',', index=False, header=True, encoding=None)

# Shows before stage of cleaning 
print('Before cleaning:')
print(df)

# Cleaning missing, duplicate, or malformed entries effectively
# Dropping duplicates
df_clean= df.drop_duplicates()
print(df_clean)

# Dropping empty rows
df_clean = df_clean[(df_clean['Title'] != 'N/A') & (df_clean['Temperature'] != 'N/A')].copy()

# Changing temperature into float
df_clean['Temperature']= df_clean['Temperature'].str.extract(r'(-?\d+)').astype(float)

# Removing whitespace from title and description
df_clean['Title'] = df_clean['Title'].str.strip()
df_clean['Description'] = df_clean['Description'].str.strip()

# Shows after stages of cleaning
print('After cleaning:')
print(df_clean)

df_clean.to_csv('weather_clean.csv', sep=',', index=False, header=True, encoding=None)

# Saving CSV files into a Sqlite database
import sqlite3

try:
    with  sqlite3.connect('db/weather.db') as conn:
        print("Database created and connected successfully.")

        # Importing raw csv in SQLite 
        df_raw_csv = pd.read_csv('weather.csv')
        df_raw_csv.to_sql('weather_raw', conn, if_exists='replace', index=False)

        # Importing clean csv in SQLite 
        df_clean_csv = pd.read_csv('weather_clean.csv')
        df_clean_csv.to_sql('weather_clean', conn, if_exists='replace', index=False)

except sqlite3.Error as e:
    print(f"An error occurred: {e}")









