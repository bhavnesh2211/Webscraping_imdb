import requests
from pprint import pprint 
from bs4 import BeautifulSoup


def scrape_top_list():
	url = requests.get("https://www.imdb.com/list/ls054840033/")
	soup = BeautifulSoup(url.text,"html.parser")
	div = soup.find("div", class_ = "lister-list")
	items = div.find_all("div",class_="lister-item mode-detail")
	actor_list = []
	for actor in items:
		actor_dic = {}
		actor_details  =actor.find("div", class_ = "lister-item-content")
		# print (actor_details)

		# rank
		rank = actor_details.find("span").getText().strip().split(".")
		actor_dic["rank"] = int(rank[0])

		# name
		name = actor_details.find("a",).getText().strip()
		actor_dic["name"] = name
		
		# url
		url = actor_details.find("a").get("href")
		actor_dic["url"] = "https://www.imdb.com" + url

		# bio
		bio = actor_details.find("p",class_= "").getText().strip()
		actor_dic["bio"] = bio
		
		actor_list.append(actor_dic.copy())
	return (actor_list)
pprint(scrape_top_list())

	
	