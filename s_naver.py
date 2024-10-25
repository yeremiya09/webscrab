from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()

url = "https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=손흥민"

driver.get(url)

time.sleep(2)

for i in range(5):

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

time.sleep(2)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

results = soup.select(".view_wrap")

for i in results:
    title = i.select_one(".title_link").text
    link = i.select_one(".title_link")['href']
    writer = i.select_one(".name").text
    dsc = i.select_one(".dsc_link").text

    print(f"제목: {title}")
    print(f"작성자: {writer}")
    print(f"링크: {link}")
    print(f"요약: {dsc}")
    print()