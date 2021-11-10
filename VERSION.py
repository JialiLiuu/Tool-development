import requests

def scriptDownload(df, cookie_str):
    '''
    下载脚本
    :param df:脚本id及版本号id
    :param cookie_str:发起请求的cookie
    :return answears:
    '''
    cookies = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    for index, row in df.iterrows():
        try:
            url = '下载文件的url?fileId={}&version={}'.format(
                row['fileId'], row['curVersion'])
            temp = requests.get(url, headers=headers,
                                cookies=cookies, stream=True)
            with open("PY文件\\{}".format(row['fileName']), "wb") as f:
                f.write(temp.content)
        except Exception as e:
            print('{}下载错误'.format(row['fileName']))

