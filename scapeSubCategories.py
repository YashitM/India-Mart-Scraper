import requests
from bs4 import BeautifulSoup

# for i in categories_dictionary:
# r = requests.get("https://trade.indiamart.com")
# html = r.content

# soup = BeautifulSoup(html, "html.parser")

# categories = soup.find_all("li", {"class": "dc-mega-li"})

# print (categories)



r = requests.get("https://trade.indiamart.com/offer/electronic-goods/")
html = r.content

soup = BeautifulSoup(html, "html.parser")

print ("[+] Finding subCategories")
ulOfSubCategories = soup.find_all("ul", {"class": "grouplist"})
subCategories_dictionary = dict()

for ul in ulOfSubCategories:
	for li in ul.find_all("li"):
		if li.find("a").get("href") != "#":
			text = li.text.lstrip().rstrip("\n")
			# print (text[:text.find("(")])
			subCategories_dictionary[text[:text.find("(")]] = li.find("a").get("href")


# for item in subCategories:
# 	pass

for i in subCategories_dictionary:
	print (i + ": " + subCategories_dictionary[i])