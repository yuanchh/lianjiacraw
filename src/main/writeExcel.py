#!/usr/bin/python

import xlwt

def readFile(filepath):
    houses=list()
    f = open(filepath,encoding='utf8')
    line = f.readline()
    while line:
        house = line.strip('\n').lstrip('\ufeff').split('###$$$')
        line = f.readline()
        houses.append(house)
    return houses

def writeExcel(houses):
    book = xlwt.Workbook()
    sheet = book.add_sheet('test')
    row=0
    for house in houses:
        col=0
        for s in house:
            sheet.write(row,col,s)
            col+=1
        row+=1
    book.save('d:/123.xls')

def main():
    houses = readFile('d:/房源1.txt')
    # houses.sort(key=lambda x:(x[2],x[1]))
    # for house in houses:
    #     print(house)
    writeExcel(houses)

if __name__=='__main__':
    main()