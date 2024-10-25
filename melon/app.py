from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging
import re
import time

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/')
def index():
    base_url = "https://www.melon.com/chart/index.htm"
    
    # Selenium 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        logging.info("멜론 차트 페이지 로딩 시작")
        driver.get(base_url)
        
        # 페이지가 완전히 로드될 때까지 대기
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "lst50"))
        )
        
        # 추가 대기 시간
        time.sleep(5)
        
        logging.info("페이지 로딩 완료")
        
        # JavaScript 실행 후 HTML 가져오기
        html = driver.execute_script("return document.documentElement.outerHTML;")
        
        # BeautifulSoup으로 파싱
        soup = BeautifulSoup(html, "html.parser")
        
        # 차트 데이터 추출
        list_all = soup.select("tr.lst50, tr.lst100")
        
        results = []
        for i, item in enumerate(list_all, 1):
            try:
                rank = str(i)
                title_element = item.select_one(".ellipsis.rank01 a")
                title = title_element.text.strip() if title_element else "제목 없음"
                
                # 노래 ID 추출 방식 변경
                song_id = item.get('data-song-no')
                if not song_id:
                    href = title_element.get('href', '')
                    song_id_match = re.search(r"goSongDetail\('(\d+)'\)", href)
                    song_id = song_id_match.group(1) if song_id_match else None
                
                singer_element = item.select_one(".ellipsis.rank02 a")
                singer = singer_element.text.strip() if singer_element else "가수 정보 없음"
                
                album_element = item.select_one(".ellipsis.rank03 a")
                album = album_element.text.strip() if album_element else "앨범 정보 없음"
                
                logging.info(f"순위: {rank}, 제목: {title}, 가수: {singer}, 앨범: {album}, 노래 ID: {song_id}")
                
                results.append({
                    'rank': rank,
                    'title': title,
                    'singer': singer,
                    'album': album,
                    'song_id': song_id
                })
            except Exception as e:
                logging.error(f"항목 처리 중 오류 발생: {e}")
        
        logging.info(f"총 {len(results)}개의 항목을 가져왔습니다.")
        return render_template('index.html', results=results)
    
    except Exception as e:
        logging.error(f"데이터 추출 중 오류 발생: {e}")
        return "차트 데이터를 가져오는데 실패했습니다."
    
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)