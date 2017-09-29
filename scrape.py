import requests
from bs4 import BeautifulSoup

def getCategories():
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

	return categories_dictionary
	# for i in categories_dictionary:
	# 	print(i + ": " + categories_dictionary[i])

def getSubcategories(categoryName, categoryURL):
	r = requests.get(categoryURL)
	html = r.content

	soup = BeautifulSoup(html, "html.parser")

	print ("[+] Finding subCategories of " + categoryName)
	ulOfSubCategories = soup.find_all("ul", {"class": "grouplist"})
	subCategories_dictionary = dict()

	for ul in ulOfSubCategories:
		for li in ul.find_all("li"):
			if li.find("a").get("href") != "#":
				text = li.text.lstrip().rstrip("\n")
				# print (text[:text.find("(")])
				subCategories_dictionary[text[:text.find("(")]] = li.find("a").get("href")

	return subCategories_dictionary
	# for item in subCategories:
	# 	pass

	for i in subCategories_dictionary:
		print (i + ": " + subCategories_dictionary[i])

if __name__ == '__main__':
	categories = getCategories()
	subCategories = dict()
	j = 0
	for i in categories:
		# j += 1
		subCategories[i] = getSubcategories(i, categories[i])

	for i in subCategories:
		print (i)
		print (subCategories[i])