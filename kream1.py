from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sys

# 검색어를 터미널에서 입력받습니다
if len(sys.argv) > 1:
    search_term = sys.argv[1]
else:
    search_term = input("검색어를 입력하세요: ")

user = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"

options_ = Options()
options_.add_argument(f"User_Agent={user}")
options_.add_experimental_option("detach", True)
options_.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options_)

# 검색 결과 페이지로 직접 이동
url = f"https://kream.co.kr/search?keyword={search_term}"
driver.get(url)
time.sleep(5)  # 페이지 로딩을 위해 대기 시간 증가

# 페이지 스크롤
for i in range(20):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

items = soup.select(".product_card")

# 확장된 카테고리 목록
categories = {
    "신발": ["스니커즈", "구두", "샌들", "슬리퍼", "부츠", "힐"],
    "상의": ["티셔츠", "셔츠", "맨투맨", "후드", "니트", "스웨터"],
    "하의": ["청바지", "팬츠", "반바지", "스커트", "레깅스"],
    "아우터": ["자켓", "코트", "패딩", "점퍼", "가디건"],
    "가방": ["백팩", "숄더백", "토트백", "클러치", "크로스백"],
    "액세서리": ["모자", "벨트", "지갑", "시계", "주얼리"],
    "기타": ["양말", "언더웨어", "홈웨어", "스포츠웨어"]
}

for item in items:
    product_name = item.select_one(".translated_name").text
    
    # 카테고리 결정 로직
    category = "기타"
    subcategory = "기타"
    for main_category, subcategories in categories.items():
        for sub in subcategories:
            if sub.lower() in product_name.lower():
                category = main_category
                subcategory = sub
                break
        if category != "기타":
            break

    product_brand = item.select_one(".product_info_brand.brand").text
    product_price = item.select_one(".amount").text

    print(f"메인 카테고리 : {category}")
    print(f"서브 카테고리 : {subcategory}")
    print(f"브랜드 : {product_brand}")
    print(f"제품명 : {product_name}")
    print(f"가격 : {product_price}")
    print()

driver.quit()