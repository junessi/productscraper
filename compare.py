import sys
from openpyxl.workbook import Workbook
from openpyxl.styles import Font

wb = Workbook()
ws = wb.active

deleted_font = Font(color = 'FF0000')
added_font = Font(color = '339966')

filename_a = sys.argv[1]
filename_b = sys.argv[2]
lines_a = set()
lines_b = set()

with open(filename_a, 'r') as fa, open(filename_b, 'r') as fb:
    for l in fa.readlines():
        lines_a.add(l)

    for l in fb.readlines():
        try:
            lines_a.remove(l)
        except:
            lines_b.add(l)

def change_row_font(min_row, max_row, min_col, max_col, font):
    for new_rows in ws.iter_rows(min_row = min_row, max_row = max_row, min_col = min_col, max_col = max_col):
        for new_cell in new_rows:
            new_cell.font = font

current_row = 1
for l in lines_a:
    cells = l.split(';')
    ws.append(cells)
    change_row_font(current_row, current_row, 1, len(cells), deleted_font)

    current_row += 1

for l in lines_b:
    cells = l.split(';')
    ws.append(cells)
    change_row_font(current_row, current_row, 1, len(cells), added_font)

    current_row += 1

wb.save('report.xlsx')
