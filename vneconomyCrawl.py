from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from bs4 import BeautifulSoup as BS
from selenium.webdriver.common.by import By
import pandas as pd
from csv import writer
from csv import DictWriter
import schedule

driver = webdriver.Chrome(ChromeDriverManager().install())
def craw_datas_website(url,keyworkQuery,keyworkTab):
    if keyworkTab:
        driver.get(url + keyworkQuery + "&tab=" + keyworkTab)
    else:
        driver.get(url + keyworkQuery)
    sleep(2)
    count_click = 6
    while count_click > 0:
        element = driver.find_element(By.CLASS_NAME, 'page-link')
        sleep(2)
        driver.execute_script("arguments[0].click()", element)
        sleep(2)
        count_click -= 1

    page = driver.page_source
    soup = BS(page, "lxml")
    product_list = []
    products = soup.find_all("article", limit=100)
    for product in products:
        title = product.find('h3', attrs={'class': 'story__title'})
        time = product.find('time')
        text = product.find('div', attrs={'class': 'story__summary'})
        product_list.append([title.get_text(), text.get_text(), time.get_text()])

    def append_list_as_row(file_name, list_of_elem):
        # Open file in append mode
        with open(file_name, 'a+', newline='', encoding="utf-8") as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(list_of_elem)

    for x in product_list:
        append_list_as_row('data.csv', x)

    driver.close()
schedule.every().day.at("07:00").do(lambda: craw_datas_website("https://vneconomy.vn/tim-kiem.htm?q=","cpi",""))
while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    sleep(1)