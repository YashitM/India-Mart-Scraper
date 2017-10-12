import requests
from bs4 import BeautifulSoup
import sys
import urllib.parse
import json
# Change it to false to run the script completely
testing = False
# FileName of excel file
excelFileName = "Archived_ExcelFile.xlsx"

firstItemsEachCategory = []

baseURL = "https://trade.indiamart.com/buyersearch.mp?ss="

def getItems(categoryName, subCategoryName, subCategoryURL):
	data = readFirstItemFromFile()
	stopSubCat = False
	firstItem = True
	page_number = 0
	# while True:
		# if page_number == 0:
		# 	soup = BeautifulSoup(requests.get(subCategoryURL).content, "html.parser")
		# else:
		# 	if "No Buy Leads" in str(requests.get(subCategoryURL+"/buy"+str(page_number)+".html").content):
		# 		break
	x = urllib.parse.quote_plus(subCategoryName)
	soup = BeautifulSoup(requests.get(baseURL+x).content, "html.parser")
	print ("[+] Getting items in " + categoryName + "->" + subCategoryName + str(page_number))
	itemDiv = soup.find_all("div", {"class": "trade-list"})
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
		other_details["Sub Category"] = subCategoryName
		other_details["Item"] = itemName
		other_details["Location"] = location
		other_details["Capacity"] = "-"
		other_details["Quantity"] = "-"
		other_details["Quantity Unit"] = "-"
		other_details["Need/Usage"] = "-"
		other_details["Frequency"] = "-"

		flag_no_unit_check = False

		if div.find("div", {"class": "c15 pt4 fs pl"}) != None:
			for table_row in div.find("div", {"class": "c15 pt4 fs pl"}).find_all("tr"):
				data = table_row.text.replace("\n","").split(":")
				if "capacity" in data[0].lower():
					capacity = data[1].lstrip()
					other_details["Capacity"] = capacity
				if len(data[0].lower().split(" ")) == 2 and "unit" in data[0].lower():
					quantity_unit = data[1].lstrip()
					flag_no_unit_check = True
					other_details["Quantity Unit"] = quantity_unit
				if "quantity" in data[0].lower() and len(data[0].lower().split(" ")) != 2:
					quantity = data[1].lstrip().split(" ")[0]
					other_details["Quantity"] = quantity
					if not flag_no_unit_check and len(data[1].lstrip().split(" ")) > 1:
						quantity_unit = data[1].lstrip().split(" ")[1]
						other_details["Quantity Unit"] = quantity_unit
				if "need" in data[0].lower() or "usage" in data[0].lower():
					need_for_this = data[1].lstrip()
					other_details["Need/Usage"] = need_for_this
				if "frequency" in data[0].lower():
					frequency = data[1].lstrip()
					other_details["Frequency"] = frequency
				item_dictionary[itemName] = other_details
			if firstItem:
				firstItemsEachCategory.append(itemName)
				firstItem = False
			else:
				if data != []:
					for i in data:
						if itemName == i:
							stopSubCat = True
							break
		if stopSubCat:
			break

	# if testing:
	# 	break
	return item_dictionary
		
def writeToExcel(itemNumber, dictToWrite, row, worksheet):
	# worksheet.write(row, 1, itemNumber)
	ws.cell(row = row, column = 1).value = itemNumber
	j = 2
	for i in dictToWrite.values():
		ws.cell(row = row, column = j).value = i
		j += 1

def writeHeadingToExcel(worksheet):
	heading = ['S.No', 'Date', 'Category', 'Sub Category', 'Item', 'Location', 'Capacity', 'Quantity', 'Quantity Unit', 'Need for this/usage', 'Frequency']
	j = 1
	for i in heading:
		ws.cell(row = 1, column = j).value = i
		j += 1

def writeFirstItemToFile(firstItemList):
	import pickle
	with open("firstItemHelper.txt", "wb") as fp:
		pickle.dump(firstItemList, fp)

def readFirstItemFromFile():
	import pickle
	data = []
	try:
		with open("firstItemHelper.txt", "wb") as fp:
			data = pickle.load(fp)
	except:
		pass
	return data

if __name__ == '__main__':
	subCategories = {}
	with open('subcategories.txt', 'r') as f:
		l = f.readlines()
		s = l[0]
		json_acceptable_string = s.replace("'", "\"")
		subCategories = json.loads(json_acceptable_string)

	# for i in subCategories:
	# 	for j in subCategories[i]:
	# 		toWrite = getItems(i, i, j)
	# 		print (toWrite)


	itemNumber = 1
	from openpyxl import Workbook
	from openpyxl import load_workbook
	wb = Workbook()
	ws = wb.active
	# workbook = xlsxwriter.Workbook(excelFileName)
	# worksheet = workbook.add_worksheet()
	writeHeadingToExcel(ws)
	wb.save(excelFileName)
	try:
		for i in subCategories:
			for j in subCategories[i]:
				dictToWrite = getItems(i, i, j)
				newDictionary = dict()
				for j in dictToWrite:
					wb = load_workbook(filename = excelFileName)
					ws = wb.get_active_sheet()
					# print(dictToWrite[j])
					writeToExcel(itemNumber, dictToWrite[j], itemNumber + 1, ws)
					wb.save(excelFileName)
					itemNumber += 1
					print(itemNumber)
				if testing:
					break
	except KeyboardInterrupt:
		pass
	# except:
	# 	 print ("Unexpected error:", sys.exc_info()[0])
	wb = load_workbook(filename = excelFileName)
	ws = wb.get_active_sheet()
	writeFirstItemToFile(firstItemsEachCategory)
	wb.save(excelFileName)
