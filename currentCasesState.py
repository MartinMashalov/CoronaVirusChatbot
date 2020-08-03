from selenium import webdriver

stats_dictionary = {}

PATH = "/Users/martinmashalov/Desktop/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://coronavirus.jhu.edu/region/us/new-york")

all_stats = driver.find_elements_by_class_name("RegionOverview_statValue__xtlKt")
trend = driver.find_elements_by_class_name("export-view__chart")
news_stats = driver.find_element_by_class_name("USState_insightContent__2C65N")
news_stats = news_stats.text.split('\n')

stats_dictionary['Total Confirmed Cases'] = all_stats[0].text
stats_dictionary['Total Deaths'] = all_stats[1].text
stats_dictionary['Total Tested'] = all_stats[2].text
stats_dictionary['Postivity Rate'] = all_stats[3].text
stats_dictionary['Daily Cases Trend'] = "".join(list(trend[0].text)[16:20])
stats_dictionary["% Positive Tests Daily"] = "".join(list(trend[2].text)[17:21])
stats_dictionary["Quick News"] = news_stats
print(stats_dictionary)

driver.quit()

