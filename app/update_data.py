"""                                     DOCS

    Collects data about railway tickets from the website and records them in the database           """


import requests  #библа для запросов к сайтам
from bs4 import BeautifulSoup

st_accept = "text/html" # говорим веб-серверу, 
                        # что хотим получить html
# имитируем подключение через браузер Mozilla на macOS
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
# формируем хеш заголовков
headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}
req = requests.get("https://xn----btbhgbpv1d7d.xn--80aswg/kupit-rzhd-bilety/#/moskva/sankt-peterburg?oldDate=true", headers)
# считываем текст HTML-документа
src = req.text
print(src)
soup = BeautifulSoup(src, 'lxml')
# считываем заголовок страницы
title = soup.title.string
print(title)