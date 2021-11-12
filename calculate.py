# -*- coding: utf-8 -*-
import ctypes
from openpyxl import load_workbook
import pandas as pd
import os
import time


class Script():
    lib = ctypes.cdll.LoadLibrary(
        'C:\\Users\\liujiali3\\Desktop\\DS\\C\\2t.so')

    lib.main1.restype = ctypes.c_char_p

    def __init__(self, scriptName):
        try:
            self.obj = Script.lib.test_new()
            tbname, s = Script.getContent(scriptName=scriptName)
            self.tbname = tbname
            self.s = s
            refer = Script.run(self=self)[1:].replace(
                " ", "").strip().split("+")
            Form.append(
                {"spname": scriptName, "tbname": tbname.strip(), "refer": refer})
        except Exception as e:
            Form.append(
                {"spname": scriptName, "tbname": {}, "refer": []})

    def run(self):
        try:
            tt = bytes(self.s, 'utf-8')
            kk = Script.lib.main1(self.obj, tt)
            return str(kk, encoding='ISO-8859-1')
        except Exception as e:
            return ""

    def getContent(scriptName):
        try:
            with open('PY文件\\{}'.format(scriptName), 'rb') as f:
                ff = f.read().decode().lower().replace("\n", " ").replace("\t", " ").replace("inner join",
                                                                                             "join").replace("inner join", "join").replace("left join", "join").replace("full join", "join")
                # 读取tempSql的内容
                s = ff[ff.find('"""')+3:ff.rfind('"""')-3]
                s = s.replace('"""', " ")

                # 读取table名字
                tbname = ff[ff.find(' table ')+6:ff.find(' partition ')]
            return tbname, s
        except Exception as e:
            return {}, {}


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


def getScripts():
    Script = []
    for parent, dirnames, filenames in os.walk(r"PY文件"):
        for filename in filenames:
            if filename.endswith('.py'):
                Script.append(filename)
    return Script


Form = []
Sp = getScripts()
for sp in Sp[100:200]:
    print(sp)
    time.sleep(2)
    S = Script(sp)
writeExcel(pd.DataFrame(Form), r"EXCEL\表依赖.xlsx", "1018上午")
