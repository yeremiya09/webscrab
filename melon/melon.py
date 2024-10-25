import requests
from bs4 import BeautifulSoup

header_user = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"}

url = "https://www.melon.com/chart/index.htm"
req = requests.get(url, headers=header_user)

if req.status_code == 200:
    html = req.text
    soup = BeautifulSoup(html, "html.parser")

    lst50 = soup.select(".lst50")
    lst100 = soup.select(".lst100")
    lst_all = lst50 + lst100

    for i in lst_all:
        rank = i.select_one(".rank").text.strip() if i.select_one(".rank") else "정보 없음"
        title = i.select_one(".ellipsis.rank01 a").text.strip() if i.select_one(".ellipsis.rank01 a") else "정보 없음"
        singer = i.select_one(".ellipsis.rank02 a").text.strip() if i.select_one(".ellipsis.rank02 a") else "정보 없음"
        album = i.select_one(".ellipsis.rank03 a").text.strip() if i.select_one(".ellipsis.rank03 a") else "정보 없음"

        # 결과 출력
        print(f"순위: {rank}")
        print(f"노래제목: {title}")
        print(f"가수: {singer}")
        print(f"앨범제목: {album}")
        print()
else:
    print("페이지를 가져오는데 실패했습니다.")
