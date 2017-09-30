dictToWrite = {'Date' : '30 Sep, 2017', 'Category' : 'abcdef', 'Name' : 'MyItem', 'Location' : 'Delhi, India', 'Capacity' : '20', 'Quantity' : '', 'Quantity Unit' : 'Nos', 'Need/Usage' : 'Personal Use', 'Frequency' : '20'}
dictToWrite2 = {'Date' : '30 Sep, 2017', 'Category' : 'abcdef', 'Name' : 'MyItem', 'Location' : 'Delhi, India', 'Capacity' : '20', 'Quantity' : '', 'Quantity Unit' : 'Nos', 'Need/Usage' : 'Personal Use', 'Frequency' : '20'}

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


writeDictToExcel(1, dictToWrite, 2)
writeDictToExcel(2, dictToWrite2, 3)
workbook.close()

