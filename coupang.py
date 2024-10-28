

import requests
from bs4 import BeautifulSoup

keyword = input("검색할 상품 :")
url = f"https://www.coupang.com/np/search?component=&q={keyword}"

header_user = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36","accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"}
cookie = {"a":"c"}
req = requests.get(url, timeout=5, headers=header_user)

html = req.text
soup = BeautifulSoup(html, "html.parser")

items = soup.select(".search-product")

#1위부터 10까지의 상품 정보를 보여준다

for rank, item in enumerate(items, 1):
    name = item.select_one(".name").text
    price = item.select_one(".price-value").text
    link = item.a["href"]
    roket = item.select_one(".badge.rocket")

    print(f"[{rank}]위")
    print(f"제품명 : {name}")
    print(f"{price}원")
    if roket:
        print("🚀로켓 배송 가능")
    else :
        print("🚀로켓 배송 불가")
    print(f"제품 링크 : https://www.coupang.com{link}")

    img_src = item.select_one(".search-product-wrap-img")
    if img_src.get("data-img-src"):
        img_url = f"https:{img_src.get('data-img-src')}"
    else:
        img_url = f"https:{img_src.get('src')}"
    img_url = img_url.replace("230x230ex", "600x600ex")
    print(f"이미지 링크 : {img_url}")
    print()

    img_req = requests.get(img_url)
    with open(f"img/{rank}.jpg", "wb") as f:
        f.write(img_req.content)
