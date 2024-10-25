import requests
from bs4 import BeautifulSoup

base_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query="
keyword = input("검색어를 입력해주세요 : ")

url = base_url + keyword
# print(url)
req = requests.get(url)

html = req.text
# print(html)
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