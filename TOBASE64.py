import base64
f = open(r'C:\Users\liujiali3\Pictures\Screenshots\屏幕截图(38).png',
         'rb')  # 二进制方式打开图文件
ls_f = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
f.close()
print(ls_f)
