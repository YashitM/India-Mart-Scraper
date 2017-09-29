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

def getItems(categoryName, subCategoryName, subCategoryURL):
	r = requests.get(subCategoryURL)
	html = r.content

	soup = BeautifulSoup(html, "html.parser")

	print ("[+] Getting items in " + categoryName + "->" + subCategoryName)

	#get Divs
	itemDiv = soup.find_all("div", {"class": "blockdiv"})
	item_dictionary = dict()

	for div in itemDiv:
		location = "-"
		capacity = "-"
		quantity = "-"
		quantity_unit = "-"
		need_for_this = "-" #along with usage
		usage = "-"
		frequency = "-"


		itemName = div.find("div",{"class": "d_lm"}).find("p",{"class": "d_f1 mb"}).find("a").text
		location = div.find("span", {"class": "latestBLBg crdLocation"}).text
		print(itemName)
		print(location)
		date = div.find("span", {"class": "dtt updatedTime"}).text
		print(date)
		other_details = div.find("div", {"class": "c15 pt4 fs pl"})
		for table_row in div.find_all("tr"):
			print(table_row.text)

		


if __name__ == '__main__':
	categories = getCategories()
	subCategories = dict()
	j = 0
	for i in categories:
		j += 1
		subCategories[i] = getSubcategories(i, categories[i])
		if j==2:
			break

	# for i in subCategories:
	# 	print (i)
	# 	print (subCategories[i])

	for i in subCategories:
		for j in subCategories[i]:
			# print(i + "   i")
			# print(subCategories[i][j])
			getItems(i,j,subCategories[i][j])
