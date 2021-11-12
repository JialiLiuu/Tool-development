with open('PY文件\\Coding_aimart_app_xz_bot_index.py', 'rb') as f:
    ff = f.read().decode().lower().replace("\n", " ").replace("\t", " ").replace("inner join",
                                                                                 "join").replace("inner join", "join").replace("left join", "join").replace("full join", "join")
    # 读取tempSql的内容
    s = ff[ff.find('"""')+3:ff.rfind('"""')-3]
    s = s.replace('"""', " ")
with open('data.txt', 'w', encoding='utf-8') as f:  # 设置文件对象
    f.write(s)  # 将字符串写入文件中
