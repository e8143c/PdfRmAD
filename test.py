#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021-09-17
# @Author  : zhou zhibin
# @github  :
#

import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter

if __name__ == "__main__":
    newf = open('2.txt', 'ab')  # 在后面加上b，表示以字节码方式写入
    with open('1.txt', 'r', encoding='UTF-8') as f:  # 打开新的文本
        s = f.readline()
        while s:
            #if not (s[-3] == '。' or s[-2] == '。'):
            if ('。' not in s[-4:]) and (len(s) > 2) and '】' not in s:
                if s[-2] == ' ':
                    s = s[:-2]
                else:
                    s = s[:-1]
                if s.isdigit():
                    s = f.readline()
                    continue
            newf.write(s.encode('utf-8'))
            print(s)
            s = f.readline()
        newf.close()
        f.close()
