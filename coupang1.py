import requests  # or any other module you need
from bs4 import BeautifulSoup

keyword = input('Enter the keyword: ')
url = f'https://www.coupang.com/np/search?component=&q={keyword}'
header_user = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36","accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"}
cookie = {"a": "c"}
req = requests.get(url, timeout=4, headers=header_user)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

items = soup.select('.search-product')

# 1위부터 10위까지 상품 정보를 보여준다

for rank, item in enumerate(items[:10], 1):
    name = item.select_one('.name').text.strip()
    price = item.select_one('.price-value').text.strip()
    link = item.select_one('.search-product-link')['href']
    img_src = item.select_one('.search-product-wrap-img')['src']
    rocket = item.select_one('.badge.rocket')
    print(f'[{rank}]위') 
    print(f"제품명: {name}") 
    print(f'{price}원')
    print(f'link: https://www.coupang.com{link}')
    if img_src.get("data-img-src"):
        img_url = img_src.get("data-img-src")
    else:
        img_src = img_src.get("src")
    
    print(f'로켓배송: {rocket is not None}')
    if rocket:
        print('로켓배송 가능')
    else:
        print('로켓배송 불가능')
    print()
