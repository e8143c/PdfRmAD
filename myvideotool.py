#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021-08-31
# @Author  : zhou zhibin
# @github  :
#
import argparse
import sys
import os


def rm_file_in_folder(folder_name, rm_file_list):
    if not os.path.exists(folder_name):
        print("Given file or folder Not EXIST!")
        exit()
    os.chdir(folder_name)
    file_list = [os.path.join(folder_name, f) for f in os.listdir(path=folder_name) if os.path.isfile(f)]
    for file in file_list:
        for rm_file in rm_file_list:
            if rm_file_list in file:
                os.remove(file)
    sub_dir_list = [os.path.join(folder_name, d) for d in os.listdir(path=folder_name) if os.path.isdir(d)]
    if len(sub_dir_list) > 0:
        # print(os.getcwd())
        for subdir in sub_dir_list:
            rm_file_in_folder(subdir, rm_file_list)

def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False


def rename_folder_by_filename(root_dir):
    # 判断没有中文名字的文件夹，如果里面的文件有汉语MP4则将目录名称以文件名称命名
    parent_path, folder = os.path.split(root_dir)
    new_name = folder
    mp4_list = [n for n in os.listdir(root_dir) if 'mp4' in n]
    subfoler_list = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
    # 如果一个目录下MP4和folder都没有了
    if not mp4_list and not subfoler_list:
        return
    # 目录中如果有子目录，先判断子目录
    elif subfoler_list:
        for subdir in subfoler_list:
            rename_folder_by_filename(os.path.join(root_dir, subdir))
    # 对前目录中的MP4和父目录比对
    for n in mp4_list:
        if len(n)-4 > len(new_name):
            new_name = n[:-4]

    if not is_chinese(folder) and is_chinese(new_name) and len(new_name) > 15:
        new_name = os.path.join(parent_path, new_name)
        os.rename(root_dir, new_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='自己做的牛逼无比的文件管理工具包')
    parser.add_argument('-r', '--remove', nargs='+', metavar='file',
                        help='Remove all the same file from give dir by -d')
    parser.add_argument('-d', '--dir', nargs='?', metavar='RootDir', required=True,
                        help='the folder tree to operate')
    parser.add_argument('-m', '--mix', nargs='+', metavar='operate', choices=['rnf'],
                        help='multiple operates, can be extend by the option')

    args = vars(parser.parse_args())

    folder_path = args['dir']
    filename = args['remove']
    mix_opt = args['mix']

    # rm useless file
    if filename:
        rm_file_in_folder(folder_path, filename)

    # rename folder if it is not identical with the mp3 in it.
    if 'rnf' in mix_opt:
        rename_folder_by_filename(folder_path)
    pass
