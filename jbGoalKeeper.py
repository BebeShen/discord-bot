import json
import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from requests import sessions
# 參考：https://github.com/bykiss555/Jable_crawler/blob/main/Jable_crawler.py
# cloud flare -> https://github.com/VeNoMouS/cloudscraper
import cloudscraper 

class goalKeeper:
    def __init__(self) -> None:
        self.httpHeaders = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2372.400 QQBrowser/9.5.10548.400', 
        }
        self.httpHeaders2 = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/96.0.4664.110'
        }
        self.cookies = dict(
            kt_ips="111.255.163.190", 
            kt_tcookie="1",
            __cf_bm="JQJP1eksSp_l7ofspvkeYCNGG3TTLS0Q8PPXv4btIeQ-1641814646-0-AapUT4Bc/oIwvnn0YbVtpddr7Jg/2brRtJUEI7497PxOz5z3ppC+rfWPo0wJLDoM2AvgygQAj/wqbILG78KAdbI="
        )
    
    def testping(self):
        '''
            測試是否能正常使用
        '''
        url = 'https://jable.tv/'
        scraper = cloudscraper.create_scraper(delay = 10)
        response = scraper.get(url)
        try:
            print(response.cookies.get_dict())
            if response.cookies.get_dict()['PHPSESSID'] != None:
                self.cookies['PHPSESSID'] = response.cookies.get_dict()['PHPSESSID']
            print(self.cookies)
            print("===========")

            # html = scraper.get(url, cookies=self.cookies, headers=self.httpHeader2, timeout=1).text
            return True
        except:
            return False

    def getNewest(self):
        print("最近更新")
        filename = "./new.html"
        returnList = []
        scraper = cloudscraper.create_scraper(delay = 10)
        try:
            html = scraper.get('https://jable.tv/latest-updates/', cookies=self.cookies, headers=self.httpHeaders2, timeout=0.5).text
            # print(html)
            soup = BeautifulSoup(html, "html.parser")
            # 用了gb18030進行編碼會出現亂碼，而utf-8不會出現亂碼
            soup.encoding = "utf-8"
            section = soup.find('section', class_="pb-3 pb-e-lg-40")
            videos = section.find_all('div', class_="video-img-box mb-e-20")
            for video in videos:
                # [9:-1] remove `data-src="`
                imageURL = str(video.select('img')).split(' ')[3][10:-1]
                print("圖片", imageURL)
                link = video.select('a')
                print("連結", link[1].get("href"))
                number = link[1].getText().split()[0]
                print("番號", number)
                info = link[1].getText()
                info = info[info.find(' ')+1:]
                returnList.append({
                    "image": imageURL,
                    "url": link[1].get("href"),
                    "number": number,
                    "description": info
                })
            with open(filename, 'w',encoding="utf-8") as f:
                f.write(str(soup.html))
            lastModifyTime = os.path.getmtime(filename)
            lastModifyTime = datetime.fromtimestamp(lastModifyTime).strftime('%Y/%m/%d %H:%M:%S')
            return lastModifyTime, returnList
        except:
            lastModifyTime = os.path.getmtime(filename)
            lastModifyTime = datetime.fromtimestamp(lastModifyTime).strftime('%Y/%m/%d %H:%M:%S')
            print(f"OOPS！好像腳斷了找不到欸。以下為{lastModifyTime}時儲存的紀錄，如欲查詢最新，請稍後重試")
            with open(filename, 'r',encoding="utf-8") as f:
                print(f.read())
                soup = BeautifulSoup(f, "html.parser")
            section = soup.find('section', class_="pb-3 pb-e-lg-40")
            videos = section.find_all('div', class_="video-img-box mb-e-20")
            for video in videos:
                imageURL = str(video.select('img')).split(' ')[4][10:-1]
                print("圖片", imageURL)
                link = video.select('a')
                print("連結", link[1].get("href"))
                number = link[1].getText().split()[0]
                print("番號", number)
                info = link[1].getText()
                info = info[info.find(' ')+1:]
                returnList.append({
                    "image": imageURL,
                    "url": link[1].get("href"),
                    "number": number,
                    "description": info
                })
            print(json.dumps(returnList, indent=4, ensure_ascii=False))
            return lastModifyTime, returnList

    def getAll(self):
        scraper = cloudscraper.create_scraper()
        try:
            html = scraper.get('https://jable.tv/hot/', headers=self.httpHeaders, timeout=0.5).text
            print(html)
            soup = BeautifulSoup(html, "html.parser")
            # 用了gb18030進行編碼會出現亂碼，而utf-8不會出現亂碼
            soup.encoding = "utf-8"
            with open("hot.html", 'w',encoding="utf-8") as f:
                f.write(str(soup.html))
            
            # print(soup.prettify())  #輸出排版後的HTML內容
        except:
            print("爬蟲失敗，請稍後再試一次，若仍無法使用，請聯絡開發者:Bebeshen")
        
        # result = soup.find_all("a")
        # print(result)

if __name__ == '__main__':
    g = goalKeeper()
    if not g.testping():
        print("Fail")
    j = g.getNewest()
