data = []

with open('dumpData.txt', 'r') as f:
	for i in f.readlines():
		if i.find("{") != -1:
			i = i.lstrip().rstrip('\n')
			data.append(i)

print (data)
# print (dictToWrite)
import xlsxwriter
workbook = xlsxwriter.Workbook('Expenses01.xlsx')
worksheet = workbook.add_worksheet()

def writeDictToExcel(itemNumber, dictionary, row):
	
	worksheet.write(row, 1, itemNumber)
	j = 2
	for i in dictionary.values():
		worksheet.write(row, j, i)
		j += 1

import json
num = 1
for i in data:
	x = i.replace("'", "\"")
	d = json.loads(x)
	writeDictToExcel(num, d, num)
	num += 1
# writeDictToExcel(1, dictToWrite, 2)
# writeDictToExcel(2, dictToWrite2, 3)
workbook.close()

