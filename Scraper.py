import requests,os,json,random,time
from pprint import pprint 
from bs4 import BeautifulSoup
url = requests.get("https://www.imdb.com/india/top-rated-indian-movies/")
soup = BeautifulSoup(url.text,"html.parser")
title = soup.title
# print (title)


#task1
def scrape_top_list():
	list1 = soup.find("tbody", class_="lister-list")
	list2=list1.find_all("tr")
	all_movies_details = []
	all_movies = []
	dictionary = {}
	for i in list2:
		trs = i.find("td", class_="titleColumn").getText().strip()
		a = trs.strip()
		list3 = a.split("\n")
		all_movies.append(list3)	
		# print (all_movies)
		for j in all_movies:
			b = j[1].strip()
			c = float(j[0])
			d = j[2][1:5]
			dictionary["name"] = b
			dictionary["year"] = int(d)
			dictionary["position"] = int(c)
		rate = i.find("strong").getText().strip()
		dictionary["Ratings"] = rate
		url1 = i.find("a")
		half_url=url1.get("href")
		half_url = half_url[:17]
		dictionary["url"] = "https://www.imdb.com" + half_url
		all_movies_details.append(dictionary.copy())
	return all_movies_details

top_movies = scrape_top_list()
# pprint(scrape_top_list())		

# task2
def group_by_year():

	movies = scrape_top_list()
	group_by_year = {}
	for i in movies:	 	
		group_by_year[i["year"]] = [j for j in movies if j["year"] == i["year"]]
	return group_by_year
# pprint(group_by_year())

#task3
def decade_by_year():
	decade_by_year = {}
	movies = scrape_top_list()
	for i in movies:
		a=(i["year"])%10
		# print (a)
		b = i["year"] - a
		if b not in decade_by_year:
			decade_by_year[b] = []

	for k in movies:
		c = k["year"] % 10 
		d = k["year"] - c 
		for j in decade_by_year:
			a = decade_by_year[j]
			if d == j:
				a.append(k)
				
	return (decade_by_year)

# pprint (decade_by_year())

 # task12

def scrape_movie_cast(movie_cast_url):
	a = movie_cast_url
	# for i in movie_cast_url:
	movie_url = movie_cast_url[27:36]+"_cast"+".json"
	file = "Webscraping_cast/" + movie_url
	# print (movie_url)
	if os.path.isfile(file):
		# print ("Hello")
		with open (file,"r") as data:
			read = data.read()
			load = json.loads(read)
			return (load)
	else:

		url = requests.get(movie_cast_url)
		soup = BeautifulSoup(url.text,"html.parser")
		url1 = soup.find("div",class_ = "article",id = "titleCast")
		url2 = url1.find("div",class_="see-more") 
		movie_cast_url = url2.find("a")
		a = a + movie_cast_url.get("href")
		# print (a)
		cast_url = requests.get(a)
		beauty = bs4.BeautifulSoup(cast_url.text,"html.parser")
		cast_list = beauty.find("table", class_="cast_list")
		cast = cast_list.find_all("td",class_ = "")
		scrape_movie_cast = []
		for i in cast:			
			actor_id_name = {}
			actor_id = i.find("a").get("href")[6:15]
			actor_name = i.getText().strip()
			actor_id_name["imdb_id"] = actor_id
			actor_id_name["name"] = actor_name
			scrape_movie_cast.append(actor_id_name.copy())
			# print (actor_id_name)
		
		with open (file , "w+") as file_data:
			json.dump(scrape_movie_cast,file_data)
	return (scrape_movie_cast)
			# break

# pprint(scrape_movie_cast(url))

# task4,task8

def scrape_movie_details(movie_url):
	movie_details = {}
	cast = scrape_movie_cast(movie_url)
	file = movie_url[27:36]+ ".json"
	file  = 'Webscraping/' + file
	if os.path.isfile(file):
		with open (file,"r") as data:
			read = data.read()
			load = json.loads(read)
			return (load)
			
	else:
		url1 = requests.get(movie_url)
		soup = bs4.BeautifulSoup(url1.text, "html.parser")

	# name
	movie_name = soup.find("div",class_ = "title_wrapper")
	movie = movie_name.find("h1")
	name = ""
	for i in movie:
		movie_details["name"] = i
		break

	# bio & director
	director = soup.find("div", class_= "credit_summary_item").getText().strip().split("\n")
	text = soup.find("div",class_ = "summary_text").getText().strip()
	for i in director:
		a = i.split(',')
	movie_details["Director"] = a
	movie_details["bio"] = text

	# runtime
	time = soup.find("div",class_="subtext")
	movie_time = time.find("time").getText().strip().split()
	d = 0
	for z in movie_time:
		if "h" in z:
			for i in z:
				if i == "h":
					continue
				else:
					d = int(i)*60
		else:
			for i in z:
				if i == "m" or i == "i" or i == "n":
					continue
				else:
					d = int(i) + d
	movie_details["rumtime"] = d

	# genre
	gen = soup.find_all("div", class_="see-more inline canwrap")
	for e in gen:
		a = e.getText().strip().split()
		if "Genres:" in a:
			movie_details["Genre"] = [i for i in a if i != "|" if i != "Genres:"]

	# country & language
	country = soup.find("div",class_="article",id = "titleDetails")
	country_name = country.find_all("div",class_="txt-block")
	language = country.find_all("div",class_="txt-block")
	for x in language:
		a = x.getText().split()
		if a[0] == "Language:":		
			movie_details["Language"] = [j for j in a if j != "|" if j != "Language:"]		

	for z in country_name:
		b = z.getText().split()
		if b[0] == "Country:":
			movie_details["Country"] = b[1]
	# image
	image = soup.find("div",id = "title-overview-widget",class_ = "heroic-overview")
	poster = image.find("img")
	poster_url = poster.get("src")
	movie_details["poster_image_url"] = poster_url

	movie_details["cast"] = cast

	with open (file,"w+") as bhau:
		json.dump(movie_details,bhau)

		

	return movie_details

# pprint(scrape_movie_details(url))


# task5,task9
def get_movie_list_details(movies_list):
	movie_details = []
	# random_time = random.randint(1,3)
	for i in movies_list:
		# time.sleep(random_time)
		a = i["url"]
		url1 = scrape_movie_details(a)
		movie_details.append(url1)
	return movie_details
top_list = get_movie_list_details(top_movies[:])
# pprint(top_list)

# task6
def analyse_movies_language(movies_list):
	analyse_movies_language = {}
	language_list = []
	movies = get_movie_list_details(movies_list)
	for i in movies:
		# a = json.loads(i)
		for j in i["Language"]:
			language_list.append(j)
			count = 0
			for l in language_list:
				if l == j:
					count += 1
			analyse_movies_language[j] = count
	return (analyse_movies_language)
top_movies = scrape_top_list()
movies_list = top_list
# # pprint (analyse_movies_language(movies_list))

# task7
def analyse_movies_Director(movies_list):
	analyse_movies_Director = {}
	director_list = []
	movies = get_movie_list_details(movies_list)
	for i in movies:
		# a = json.loads(i)
		for j in i["Director"]:
			# print (j)
			director_list.append(j)
			count = 0
			for l in director_list:
				if l == j:
					count += 1
			analyse_movies_Director[j] = count 			
	return (analyse_movies_Director)

top_movies = scrape_top_list()
movies_list = top_list
# pprint (analyse_movies_Director(movies_list))


# # task10
def analyse_language_and_directors(movies_list):
	all_directors = {}
	language_list = []
	movies_list = get_movie_list_details(movies_list)
	for i in movies_list:
		# a = json.loads(i)
		director_name = i["Director"]
		for j in director_name:
			# print (j)
			all_directors[j] = {}
			for x in movies_list:
				# b = json.loads(x)
				for director in all_directors:
					if director in x["Director"]:
						for y in x["Language"]:
							all_directors[director][y] = 0
			for x in movies_list:
				# c = json.loads(x)
				for director in all_directors:
					if director in x["Director"]:
						for y in x["Language"]:
							all_directors[director][y] +=1

	return (all_directors)

movies_list = scrape_top_list()
pprint(analyse_language_and_directors(movies_list))


# task11
def analyse_movies_genre(movies_list):
	analyse_movies_genre = {}
	movies = scrape_movie_details(movies_list)
	for i in movies:
		for j in i["Genre"]:
			if j in i["Genre"]:
				analyse_movies_genre[j] = 0
	for i in movies:
		for j in i["Genre"]:
			if j in i["Genre"]:
				analyse_movies_genre[j] += 1
	return (analyse_movies_genre)
top_list = get_movie_list_details(movies_list)
# analyse_movies_genre(top_list)


# task14


def analyse_co_actors(movies_list):
	main_actors = []
	# top_actors = {}
	for i in movies_list:
		# top_actor = i["cast"][0] 
		main_actors.append(i["cast"][0])
	top_actors = {top_actor["imdb_id"] : {"name":top_actor["name"],"frequent_co_actors":[]} for top_actor in main_actors}
	all_cast = []
	for actor in movies_list:
		b = []
		for j in actor["cast"][:5]:
			j["num_movies"] = 1
			b.append(j)
		all_cast.append(b)
	# return (all_cast)
	for main_actor in main_actors:
		for list in all_cast:
			if main_actor in list:
				id_main_actor = main_actor["imdb_id"]
				list_of_co_actors = top_actors[id_main_actor]["frequent_co_actors"]
				for list_actor in list[1:]:
					if list_actor not in list_of_co_actors:
						list_of_co_actors.append(list_actor)
					else:
						list_of_co_actors[list_of_co_actors.index(list_actor)]["num_movies"] += 1
		for id_of_actor in top_actors:
			for i in top_actors[id_of_actor]["frequent_co_actors"]:
				if id_of_actor == i["imdb_id"]:
					top_actors[id_of_actor]["frequent_co_actors"].pop(top_actors[id_of_actor]["frequent_co_actors"].index(i))
	return top_actors			
# pprint (analyse_co_actors(top_list))



# task15
def analyse_actors(movies_list):
	main_actors = []
	for i in movies_list:
		cast_of_movie = i["cast"]
		for j in cast_of_movie:
			main_actors.append(j)
			cast_dict = {main_actor["imdb_id"]:{"name" : main_actor["name"],"num_movies" : 0} for main_actor in main_actors }

	for cast in cast_dict:
		for actor in main_actors:
			if actor["imdb_id"] == cast:
				cast_dict[cast]["num_movies"] += 1
	analyse_actors = {}
	for one_actor in cast_dict:
		if cast_dict[one_actor]["num_movies"] > 1:
			analyse_actors[one_actor] = cast_dict[one_actor] 
	return (analyse_actors)
# pprint (analyse_actors(top_list))
