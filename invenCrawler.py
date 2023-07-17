from bs4 import BeautifulSoup as bs
import requests
import datetime
from konlpy.tag import Okt
import pandas as pd
okt = Okt()

today = str(datetime.date.today()).replace(str(datetime.date.today().year) + "-","")

db = {}
for i in range(100):
	# 여기 인벤사이트 링크
	# url = "https://www.inven.co.kr/board/lostark/4811?my=chu&p="+str(i)
	url = "https://www.inven.co.kr/board/lostark/4811?p="+str(i)
	response =requests.get(url)
	source = response.text
	soup=bs(source,"html.parser")
	list = soup.select("#new-board > form > div > table > tbody > tr")
	for li in list:
		title = li.select_one("td.tit a").contents[2].strip()
		date = li.select_one("td.date").text
		if ':'in date:
			date = today
		nounss = okt.nouns(title)
		tmp = []
		for noun in nounss:
			if(len(noun)>1):
				tmp.append(noun)

		if date in db.keys():
			db[date]+=tmp
		else:
			db[date] = tmp


data = pd.DataFrame.from_dict(db, orient='index')
# print(data)
#여기 컴퓨터에 엑셀 저장할 위치
path="C:/Users/user/Desktop/kang/htmlPr/"+today+".xlsx"
data.to_excel(path)

