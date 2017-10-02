data = {'Teflon sealing Tapes': {'Date': '01 Oct, 2017  ', 'Category': 'Electronics & Electrical', 'Item': 'Teflon sealing Tapes', 'Location': 'Bhubaneswar, India', 'Capacity': '-', 'Quantity': '', 'Quantity Unit': 'Nos', 'Need/Usage': 'Sealing', 'Frequency': '-'}}

# print (dictToWrite)
# import xlsxwriter
# workbook = xlsxwriter.Workbook('lol.xlsx')
# worksheet = workbook.add_worksheet()

# def writeDictToExcel(itemNumber, dictionary, row):
	
# 	worksheet.write(row, 1, itemNumber)
# 	j = 2
# 	for i in dictionary.values():
# 		worksheet.write(row, j, i)
# 		j += 1

# import json
# num = 1
# for i in data:
# 	print(i)
# 	# writeToExcel(itemNumber, i, itemNumber + 1, worksheet)
# 	writeDictToExcel(num, data[i], num)
# 	num += 1
# # writeDictToExcel(1, dictToWrite, 2)
# # writeDictToExcel(2, dictToWrite2, 3)
# workbook.close()
import csv
for i in data:
	with open('mycsvfile.csv', 'w') as f:  # Just use 'w' mode in 3.x
		w = csv.DictWriter(f, data[i].keys())
		w.writeheader()
		w.writerow(data[i])
