from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from bs4 import BeautifulSoup as BS
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://vn.investing.com/search/?q=cpi&tab=news")
sleep(3)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(3)
page = driver.page_source
soup = BS(page,"lxml")
product_list = []
products = soup.find_all("div",attrs={'class':'articleItem'},limit=100)
for product in products:
    if product.find('p',attrs={'class':'js-news-item-content'}):
        text = product.find('p', attrs={'class': 'js-news-item-content'})
        time = product.find('time', attrs={'class': 'date'})
        title = product.find('a', attrs={'class': 'title'})
        product_list.append([title.get_text(),text.get_text(),time.get_text()])




df = pd.DataFrame(product_list,columns=['Title','Text','Date'])
df.to_csv('data.csv',index=False)

driver.close()
