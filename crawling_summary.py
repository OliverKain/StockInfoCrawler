# -*- coding: utf-8 -*-

import glob
import csv
import operator
from xlsxwriter.workbook import Workbook


workbook = Workbook("data/_crawledData.xlsx")
for csvfile in glob.glob("data/*.csv"):
    csv_name = csvfile[5:-4]
    worksheet = workbook.add_worksheet(csv_name.replace("_refined", ""))
    with open(csvfile, 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        data = list(reader)
        if len(data) > 0:
            header = data.pop(0)
            # sort
            data.sort(key=operator.itemgetter(1), reverse=True)
            data.insert(0, header)
        for r, row in enumerate(data):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
try:
    workbook.close()
except OSError as err:
    print("OS error: {0}".format(err))
