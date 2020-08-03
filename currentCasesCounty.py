from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys

df = pd.read_csv("New_York_State_ZIP_Codes.csv", delimiter=',')
df = df.drop(df.columns[[1, 2, 3, 5]], axis=1)

def find_county_by_zip_code(zip_code):
    counties = []
    for index, row in df.iterrows():
        if row['ZIP Code'] == int(zip_code):
            counties.append(row['County Name'])
    if len(counties) > 1:
        print(counties)
        county = input("Which one of these counties do you live in: ")
        while county not in counties:
            print("County is not recognized, perhaps you made a typo?")
            county = input("Which one of these counties do you live in: ")
        return county
    return counties[0]

print(find_county_by_zip_code(10522))
