# import xlwt
# from xlwt import Workbook

import xlsxwriter
# pip install xlsxWriter

# wb = Workbook()

# sheet1= wb.add_sheet('Seeder')

# sheet1.write(1,0, 12345)


workbook = xlsxwriter.Workbook('seeder.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Hello')
workbook.close()
