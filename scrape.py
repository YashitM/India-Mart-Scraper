import requests
from bs4 import BeautifulSoup

def getCategories():
	soup = BeautifulSoup(requests.get("https://trade.indiamart.com").content, "html.parser")
	categories_dictionary = dict()

	for item in soup.find_all("li", {"class": "dc-mega-li"}):
		if item.find("a").get("href") != "#":
			categories_dictionary[item.text.lstrip().rstrip("\n")] = item.find("a").get("href")
	# do the same for 132 and 133
	for item in soup.find_all("li", {"class": "menu-item-131"}):
		categories_dictionary[item.text.lstrip().rstrip("\n")] = item.find("a").get("href")

	print("[*] Categories found!")
	return categories_dictionary

def getSubcategories(categoryName, categoryURL):
	soup = BeautifulSoup(requests.get(categoryURL).content, "html.parser")
	print ("[+] Finding Sub Categories of " + categoryName)
	subCategories_dictionary = dict()

	for ul in soup.find_all("ul", {"class": "grouplist"}):
		for li in ul.find_all("li"):
			if li.find("a").get("href") != "#":
				text = li.text.lstrip().rstrip("\n")
				subCategories_dictionary[text[:text.find("(")]] = li.find("a").get("href")

	return subCategories_dictionary

def getItems(categoryName, subCategoryName, subCategoryURL):
	soup = BeautifulSoup(requests.get(subCategoryURL).content, "html.parser")
	print ("[+] Getting items in " + categoryName + "->" + subCategoryName)
	# itemDiv = soup.find_all("div", {"class": "blockdiv"})
	itemDiv = soup.find_all("div", {"class": "trade-list"})
	item_dictionary = dict()
	for div in itemDiv:
		location = "-"
		capacity = "-"
		quantity_unit = "-"
		quantity = "-"
		need_for_this = "-"
		usage = "-"
		frequency = "-"
		# itemName = div.find("div",{"class": "d_lm"}).find("p",{"class": "d_f1 mb"}).find("a").text
		itemName = div.find("div",{"class": "d_lm"}).find("p",{"class": "d_f1"}).find("a").text
		# location = div.find("span", {"class": "latestBLBg crdLocation"}).text
		location = div.find("span", {"class": "bl_ccname location"}).text
		date = div.find("span", {"class": "dtt updatedTime"}).text
		print("Name: " + itemName)
		print("Location: " + location)
		print("Date: " + date)
		other_details = dict()

		if div.find("div", {"class": "c15 pt4 fs pl"}) != None:
			for table_row in div.find("div", {"class": "c15 pt4 fs pl"}).find_all("tr"):
				data = table_row.text.replace("\n","").split(":")
				if data[0] == "Quantity":
					quantity = data[1].split(" ")[0].lstrip()
					quantity_unit = data[1].split(" ")[1].lstrip()
				print(data)

			# other_details["lol"] = data

		print(other_details)

if __name__ == '__main__':
	categories = getCategories()
	subCategories = dict()
	j = 0
	for i in categories:
		j += 1
		subCategories[i] = getSubcategories(i, categories[i])
		if j==2:
			break

	for i in subCategories:
		for j in subCategories[i]:
			getItems(i,j,subCategories[i][j])
