#!/usr/bin/python

# pdfbooklet.py
#
# Copyright (c) 2014 Mark O. Busby <mark@busbycreations.com>
#
# Licensed under the MIT/X11 license - see LICENSE.txt
#
# Add a blank page at the beginning or end of a pdf file

from optparse import OptionParser
import re
import tempfile
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger

def main():
    parser = OptionParser(usage="usage: %prog [options] PDF-file")
    parser.add_option("-o", "--out", dest="pdfOut", help="Name of PDF File to create")
    parser.add_option("-b", "--begin", dest="begin", action="store_true", default=False, help="Insert blank page at beginning of file, instead of end")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False, help="Print debug messages")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("1 and only 1 PDF File, please.")

    pdfIn = args[0]
    if options.pdfOut:
        pdfOut = options.pdfOut
    else:
        pdfOut = re.sub('\.[pP][dD][fF]$', '', pdfIn)
        pdfOut = pdfOut + '--blankified.pdf'

    originalPDF = open(pdfIn, 'rb')
    pdfReader = PdfFileReader(originalPDF)
    pageSize = pdfReader.getPage(0).mediaBox.upperRight

    tempPDF = tempfile.TemporaryFile()
    writer = PdfFileWriter()
    writer.addBlankPage(pageSize[0], pageSize[1])
    writer.write(tempPDF)

    merger = PdfFileMerger()
    merger.append(originalPDF)

    if options.begin:
        merger.merge(position=0, fileobj=tempPDF)
    else:
        merger.append(tempPDF)

    merger.write(open(pdfOut, 'wb'))

if __name__ == "__main__":
    main()
