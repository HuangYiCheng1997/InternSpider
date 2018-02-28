from fontTools.ttLib import TTFont
import time
import os
import requests
import base64
import re


class FontProcesster(object):

    def __init__(self):
        super().__init__()
        font = self.get_font()
        self.code_to_name = font['cmap'].tables[0].cmap  # 字典 key = code value = name

    def get_font(self):
        today = time.strftime('%Y_%m_%d', time.localtime())
        filename = today + '.woff'
        if not os.path.exists(filename):
            print('缺少字体文件,准备下载......')
            url = 'https://www.shixiseng.com/interns?k=python&p=1'
            html = requests.get(url).content.decode('utf-8')
            fake_font = re.search(r'octet-stream;base64,(.*?)"', html).groups()[0]
            real_font = base64.b64decode(fake_font)
            with open(filename, 'wb') as f:
                f.write(real_font)
            print('下载完毕')

        return TTFont(filename)

    def process(self, data):
        data = repr(data)
        codes = re.findall(r'\\u(\w{4})', data)  # 从数据中找出 code
        codes_dec = [eval('0x' + each) for each in codes]  # 把16进制code 转成 10进制code
        chars = []
        for code in codes_dec:
            name = self.code_to_name[code]
            char = name[-1]  # 投机取巧
            chars.append(char)
        data = re.sub(r'\\u\w{4}', lambda match: chars.pop(), data)
        return data.strip("'")


if __name__ == '__main__':
    FP = FontProcesster()
    test = TTFont('./intern.woff')
    test.saveXML('./intern.xml')