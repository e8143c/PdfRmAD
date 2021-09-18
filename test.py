#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021-09-17
# @Author  : zhou zhibin
# @github  :
#

import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='自己做的牛逼无比的文件管理工具包')
    parser.add_argument('-r', '--remove', nargs='+', metavar='file',
                        help='Remove all the same file from give dir by -d')
    parser.add_argument('-d', '--dir', nargs='?', metavar='RootDir', required=True,
                        help='the folder tree to operate')
    parser.add_argument('-m', '--mix', nargs='+', metavar='operate',
                        help='multiple operates, can be extend by the option')
    args = vars(parser.parse_args())
    print(args)


