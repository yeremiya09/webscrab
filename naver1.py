import requests
from bs4 import BeautifulSoup

# 네이버 검색 기본 URL
base_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query="
keyword = input("검색어를 입력해주세요 : ")

# 검색어로 완성된 URL
url = base_url + keyword
req = requests.get(url)

if req.status_code == 200:
    soup = BeautifulSoup(req.text, "html.parser")

    # 뉴스와 블로그 검색 결과
    news_items = soup.select('.news_area')  
    blog_items = soup.select('.sh_blog_top')  

    results = []

    # 뉴스 결과 처리
    for i in news_items:
        results.append({
            'title': i.select_one('.news_tit').text.strip(),
            'link': i.select_one('.news_tit')['href'],
            'writer': i.select_one('.info_group .press').text.strip() if i.select_one('.info_group .press') else '작성자 정보 없음',
            'summary': i.select_one('.dsc_link').text.strip() if i.select_one('.dsc_link') else '요약 정보 없음'
        })

    # 블로그 결과 처리
    for i in blog_items:
        results.append({
            'title': i.select_one('.sh_blog_title').text.strip(),
            'link': i.select_one('.sh_blog_title')['href'],
            'writer': i.select_one('.name').text.strip() if i.select_one('.name') else '작성자 정보 없음',
            'summary': i.select_one('.sh_blog_passage').text.strip() if i.select_one('.sh_blog_passage') else '요약 정보 없음'
        })

    # 결과 출력
    if results:
        for result in results:
            print(f"제목: {result['title']}")
            print(f"작성자: {result['writer']}")
            print(f"링크: {result['link']}")
            print(f"요약: {result['summary']}")
            print()
    else:
        print("검색 결과를 찾을 수 없습니다.")
else:
    print("페이지를 가져오는데 실패했습니다.")
