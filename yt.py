import os
import requests
from dotenv import load_dotenv
class ytSearcher():
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        print(self.api_key)

    def getIdByName(self, name):
        response = requests.get(f"https://www.googleapis.com/youtube/v3/channels?key={self.api_key}&forUsername={name}&part=id")
        print(response.json())

    def searchNewest(self):
        response = requests.get(f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId=UCXOBLGJdYA1mfhOrDwQESTg&part=snippet,id&order=date&maxResults=5")
        data = response.json()
        videos = data['items']
        for v in videos:
            print(v['snippet']['channelTitle'])
            print("影片連結：", v['id']['videoId'])
            print("標題：", v['snippet']['title'])
            print("縮圖：", v['snippet']['thumbnails']['high']['url'])
            print("時間：",v['snippet']['publishTime'])
            print("======================================")

        return videos

if __name__ == "__main__":
    y = ytSearcher()
    # y.searchNewest()
    y.getIdByName("Dinterlolz")
    y.getIdByName("Dinter")