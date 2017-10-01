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
	itemDiv = soup.find_all("div", {"class": "blockdiv"})
	# itemDiv = soup.find_all("div", {"class": "trade-list"})
	item_dictionary = dict()
	for div in itemDiv:
		location = "-"
		capacity = "-"
		quantity_unit = "-"
		quantity = "-"
		need_for_this = "-"
		frequency = "-"

		itemName = div.find("div",{"class": "d_lm"}).find("p",{"class": "d_f1"}).find("a").text
		location = div.find("span", {"class": "bl_ccname location"}).text.lstrip()
		date = div.find("span", {"class": "dtt updatedTime"}).text.lstrip()
		
		other_details = dict()

		other_details["Date"] = date
		other_details["Category"] = categoryName
		other_details["Item"] = itemName
		other_details["Location"] = location
		other_details["Capacity"] = "-"
		other_details["Quantity"] = "-"
		other_details["Quantity Unit"] = "-"
		other_details["Need/Usage"] = "-"
		other_details["Frequency"] = "-"
		j = 0
		if div.find("div", {"class": "c15 pt4 fs pl"}) != None:
			for table_row in div.find("div", {"class": "c15 pt4 fs pl"}).find_all("tr"):
				j+=1
				data = table_row.text.replace("\n","").split(":")
				if j==3:
					break
				if "capacity" in data[0].lower():
					capacity = data[1].lstrip()
					other_details["Capacity"] = capacity
				if "unit" in data[0].lower():
					quantity_unit = data[1].lstrip()
					other_details["Quantity Unit"] = quantity_unit
				if "quantity" in data[0].lower():
					if len(data[1].split(" ")) == 2:
						print(data[1].split(" "))
						quantity = data[1].split(" ")[0].lstrip()
						quantity_unit = data[1].split(" ")[1].lstrip()
						other_details["Quantity"] = quantity
						other_details["Quantity Unit"] = quantity_unit
					else:
						quantity = data[1].lstrip()
						other_details["Quantity"] = quantity
				if "need" in data[0].lower() or "usage" in data[0].lower():
					need_for_this = data[1].lstrip()
					other_details["Need/Usage"] = need_for_this
				if "frequency" in data[0].lower():
					frequency = data[1].lstrip()
					other_details["Frequency"] = frequency
		return other_details
		
def writeToExcel(itemNumber, dictToWrite, row, worksheet):
	worksheet.write(row, 1, itemNumber)
	j = 2
	for i in dictToWrite.values():
		worksheet.write(row, j, i)
		j += 1

if __name__ == '__main__':
	categories = getCategories()
	subCategories = dict()
	j = 0
	for i in categories:
		j += 1
		subCategories[i] = getSubcategories(i, categories[i])
		if j==2:
			break

	itemNumber = 1
	import xlsxwriter
	workbook = xlsxwriter.Workbook('Expenses01.xlsx')
	worksheet = workbook.add_worksheet()
	for i in subCategories:
		for j in subCategories[i]:
			dictToWrite = getItems(i,j,subCategories[i][j])
			print(dictToWrite)
			writeToExcel(itemNumber, dictToWrite, itemNumber + 1, worksheet)
			break
	workbook.close()
