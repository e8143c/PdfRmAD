#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021-08-31
# @Author  : zhou zhibin
# @github  :

from PyPDF2 import PdfFileReader, PdfFileWriter,PdfFileMerger
import sys
import os
from pathlib import Path

def pageisAD(pageobj):
    # if the last page is AD
    if (pageobj.cropBox.getHeight() == 360) and (pageobj.cropBox.getWidth() == 640):
        return True
    else:
        return False

def argisfloder(argpath):
    if not os.path.exists(argpath):
        print("Given file or folder Not EXIST!")
        exit()
    if os.path.isdir(argpath):
        return True
    else:
        return False


def rmthead(infn):
    infileobj = open(infn, 'rb')
    pdf_input = PdfFileReader(infileobj, 'rb')
    page_count = pdf_input.getNumPages()
    # print(page_count)
    page = pdf_input.getPage(page_count-1)
    if pageisAD(page):
        merger = PdfFileMerger()
        outfn = infn[:-4]+"AA.pdf"
        merger.append(infileobj, pages=(0, page_count-2))
        merger.write(outfn)
        merger.close()
        infileobj.close()
        os.remove(infn)
        os.rename(outfn, infn)
        print("%4d Pages - Book: %s Removed AD in the end of book" % (page_count, os.path.split(infn)[-1].ljust(40)))
    else:
        print("%4d Pages - Book: %s NO AD in the end of book" % (page_count, os.path.split(infn)[-1].ljust(40)))


if __name__ == '__main__':
    file = sys.argv[1]
    if argisfloder(sys.argv[1]):
        pdflist = [f for f in os.listdir(sys.argv[1]) if '.pdf' in f]
        if len(pdflist)>0:
            for f in pdflist:
                rmthead(os.path.join(sys.argv[1], f))
        exit(0)
    rmthead(file)


