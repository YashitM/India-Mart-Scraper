import requests
from bs4 import BeautifulSoup

r = requests.get("https://trade.indiamart.com")
html = r.content

soup = BeautifulSoup(html, "html.parser")

categories = soup.find_all("li", {"class": "dc-mega-li"})

categories_dictionary = dict()

for item in categories:
	if item.find("a").get("href") != "#":
		categories_dictionary[item.text.lstrip().rstrip("\n")] = item.find("a").get("href")

print("[*] categories done")

other_categories = soup.find_all("li", {"class": "menu-item-131"})

for item in other_categories:
	categories_dictionary[item.text.lstrip().rstrip("\n")] = item.find("a").get("href")

for i in categories_dictionary:
	print(i + ": " + categories_dictionary[i])