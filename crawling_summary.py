# import pandas as pd
import glob
import csv
from xlsxwriter.workbook import Workbook


# Export to Excel using pandas
# df1 = pd.read_csv("data/crawledData_refined.csv")
# writer = pd.ExcelWriter("data/crawledData.xlsx", engine="xlsxwriter")
# df1.to_excel(writer, "Sheet1")
# writer.save()

workbook = Workbook("data/crawledData.xlsx")
for csvfile in glob.glob("data/*.csv"):
    csv_name = csvfile[5:-4]
    worksheet = workbook.add_worksheet(csv_name.replace("_refined", ""))
    with open(csvfile, 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
workbook.close()
