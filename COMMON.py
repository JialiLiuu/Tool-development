import os
from openpyxl import load_workbook
import pandas as pd


# cookie_str转成cookie
def strToCookie(cookie_str):
    cookies = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    return cookies

# df写入excel


def writeExcel(df, filename, sheetname):
    if not os.path.exists(filename):
        tt = pd.DataFrame()
        tt.to_excel(filename)
    book = load_workbook(filename)
    writer = pd.ExcelWriter(filename, engine='openpyxl')
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    df.to_excel(writer, sheetname)
    writer.save()
    return True

# 读excel返回df


def readExcel(filename, sheetname):
    df = pd.read_excel(filename, sheetname)
    return df
