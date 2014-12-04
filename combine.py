#!/usr/bin/python

# pdfbooklet.py
#
# Copyright (c) 2014 Mark O. Busby <mark@busbycreations.com>
#
# Licensed under the MIT/X11 license - see LICENSE.txt
#
# Combine 2 PDFs

from optparse import OptionParser
import re
import tempfile
from PyPDF2 import PdfFileMerger

def main():
    parser = OptionParser(usage="usage: %prog [options] PDF1 PDF2")
    parser.add_option("-o", "--out", dest="pdfOut", help="Name of PDF File to create")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False, help="Print debug messages")
    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.error("At least 2 input PDF Files, please.")

    if options.pdfOut == None:
        parser.error("An output file name must be specified")

    merger = PdfFileMerger()
    for fileName in args:
        merger.append(open(fileName, 'rb'))
    
    merger.write(open(options.pdfOut, 'wb'))

if __name__ == "__main__":
    main()
