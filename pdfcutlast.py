#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021-08-31
# @Author  : zhou zhibin
# @github  :
# TODO: MP3的切片功能,界面,logging
import argparse
import os
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter


def page_is_ad(page_obj):
    """
    whether the page is advertisement of 调研君
    :param page_obj: page object get by PdfFileReader
    :return: is AD return True, otherwise return False
    """
    if (page_obj.cropBox.getHeight() == 360) and (page_obj.cropBox.getWidth() == 640):
        return True
    else:
        return False


def arg_is_folder(path):
    """
    determine the param indicate a path of folder
    :param path: path for folder or file
    :return: True for folder, False for file. exit if the path not exist
    """
    if not os.path.exists(path):
        print("Given file or folder Not EXIST!")
        exit()
    if os.path.isdir(path):
        return True
    else:
        return False


def navi_and_del_ad_page(origin_name):
    """
        check the ad one by one and join a new PDF
        :param origin_name: pdf file path
        :return: None
        """
    if ' ' in origin_name:
        os.rename(origin_name, origin_name.replace(' ', ''))
        origin_name = origin_name.replace(' ', '')
    origin_pdf = open(origin_name, 'rb')
    # print align debug code, wid_gap is mean the gap between GBK output with ASII
    # print("%d+%d" % (len(os.path.split(origin_name)[-1]), len(os.path.split(origin_name)[-1].encode('GBK'))))
    try:
        wid_gap = len(origin_name.encode('GBK')) - len(origin_name)
    except UnicodeEncodeError:
        wid_gap = len(origin_name)
    try:
        out_file = out_filename = origin_pdf.name[:-4] + "tmp.pdf"
        pdf_file_writer = PdfFileWriter()
        pdf_file_reader = PdfFileReader(origin_pdf)
        page_count = pdf_file_reader.getNumPages()
        for index in range(0, page_count):
            page_obj = pdf_file_reader.getPage(index)
            if not page_is_ad(page_obj):
                pdf_file_writer.addPage(page_obj)
            else:
                print("Page %4d in Book: %s is AD page, SKIP!" % (
                    index, os.path.split(origin_name)[-1].ljust(50 - wid_gap)))

        tmp_pdf = open(out_file, 'wb')
        pdf_file_writer.write(tmp_pdf)
        tmp_pdf.close()
        origin_pdf.close()
        os.remove(origin_name)
        os.rename(out_filename, origin_name)
    except Exception as e:
        print("ERROR！！！ while writing " + os.path.split(origin_name)[-1])
        print(e)


def cut_last_page(origin_name):
    """
    delete the last page if it is the AD of 调研君
    :param origin_name: pdf file path
    :return: None
    """
    if ' ' in origin_name:
        os.rename(origin_name, origin_name.replace(' ', ''))
        origin_name = origin_name.replace(' ', '')
    origin_pdf = open(origin_name, 'rb')
    # print align debug code, wid_gap is mean the gap between GBK output with ASII
    # print("%d+%d" % (len(os.path.split(origin_name)[-1]), len(os.path.split(origin_name)[-1].encode('GBK'))))
    try:
        wid_gap = len(origin_name.encode('GBK')) - len(origin_name)
    except UnicodeEncodeError:
        wid_gap = len(origin_name)
    try:
        pdf_input = PdfFileReader(origin_pdf, strict=False)
        if pdf_input.isEncrypted:
            # pdf_input.decrypt(False)
            pass
        page_count = pdf_input.getNumPages()
    except Exception as e:
        print("ERROR！！！ while reading " + os.path.split(origin_name)[-1])
        print(e)
        return
    # 广告页面有可能存在于倒数第一页，或者倒数第二页，判断广告页的位置，并赋值下标
    last_page_1 = pdf_input.getPage(page_count-1)
    last_page_2 = pdf_input.getPage(page_count-2)
    if page_is_ad(last_page_2):
        last_index = page_count-3
    elif page_is_ad(last_page_1):
        last_index = page_count - 2
    else:
        last_index = 0

    if last_index:
        merger = PdfFileMerger()
        out_filename = origin_pdf.name[:-4] + "tmp.pdf"
        try:
            merger.append(origin_pdf, pages=(0, last_index))
        except KeyError:
            wid_gap = len(origin_name)
        try:
            merger.write(out_filename)
            origin_pdf.close()
            os.remove(origin_name)
            os.rename(out_filename, origin_name)
            print("%4d Pages - Book: %s Removed AD in the end of book" % (
                page_count, os.path.split(origin_name)[-1].ljust(50 - wid_gap)))
        except Exception as e:
            print("ERROR！！！ while writing " + os.path.split(origin_name)[-1])
            print(e)
        finally:
            merger.close()

    else:
        print("%4d Pages - Book: %s NO AD in the end of book" % (
            page_count, os.path.split(origin_name)[-1].ljust(50-wid_gap)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A great PDF tool for me')
    parser.add_argument('-d', '--dir', nargs='?', metavar='RootDir', required=True, dest='workdir',
                        help='the folder tree to operate, PDF file can be compatible')
    parser.add_argument('-m', '--mix', nargs='+', metavar='operate',
                        help='multiple operates, can be extend by the option')
    args = vars(parser.parse_args())

    if arg_is_folder(args['workdir']):
        list_pdf = [f for f in os.listdir(args['workdir']) if '.pdf' in f]
        if len(list_pdf) > 0:
            for f in list_pdf:
                navi_and_del_ad_page(os.path.join(args['workdir'], f))
        exit(0)
    # cut_last_page(args['workdir'])
    navi_and_del_ad_page(args['workdir'])
