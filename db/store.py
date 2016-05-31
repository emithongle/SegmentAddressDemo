__author__ = 'Thong_Le'

import csv, xlrd, xlsxwriter
import json
import pickle

def readFile(file):
    strList = []
    infile = open(file, encoding="utf-8")
    for line in infile:
        strList.append(line)
    return strList

def saveJson(data, file):
    with open(file, 'w', encoding='utf8') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

def loadJson(file):
    try:
        return json.loads(''.join(readFile(file)))
    except:
        return None

def saveCSV(data, file):
    with open(file, 'w', newline='', encoding="utf-8") as f:
    # with open(file + '.csv', 'w', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(data)
        # for row in data:
        #     writer.writerow(row)

def loadCSV(file):
    data = []
    with open(file, newline='', encoding="utf-8") as f:
    # with open(file + '.csv', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            data.append(row)

    return data

def loadPKL(filepath):
    with open(filepath, 'rb') as f:
        try:
            model = pickle.load(f, encoding='latin1')
        except:
            model = pickle.load(f)
    return model


def saveXLSX(data, filepath):

    def writeSheet(sheet, data):
        for i in range(len(data)):
            for j in range(len(data[i])):
                sheet.write(i, j, data[i][j])

    workbook = xlsxwriter.Workbook(filepath)
    for shName, sh in data.items():
        writeSheet(workbook.add_worksheet(shName), sh)
    workbook.close()


def loadXLSX(filepath, sheet_Ids=[0]):
    data = []

    for sid in sheet_Ids:
        tmpsheet = xlrd.open_workbook(filepath).sheet_by_index(0)
        for i in range(tmpsheet.nrows):
            data.append(tmpsheet.row_values(i))

    return data