#!/usr/bin/python

# pdfshrink.py
#
# Copyright (c) 2014 Mark O. Busby <mark@busbycreations.com>
#
# Licensed under the MIT/X11 license - see LICENSE.txt
#
# Shrink pages in a PDF to half size (i.e. Letter pages become half-letter)

from optparse import OptionParser
import re
from PyPDF2 import pdf, PdfFileWriter, PdfFileReader

def main():
    parser = OptionParser(usage="usage: %prog [options] PDF-file")
    parser.add_option("-o", "--out", dest="pdfOut", help="Name of PDF File to create")
    parser.add_option("-f", "--first", type="int", dest="firstPage", default=1, help="First page of booklet")
    parser.add_option("-l", "--last", type="int", dest="lastPage", default=0, help="Last page of booklet")
    parser.add_option("-n", "--nocenter", action="store_false", dest="center", default=True, help="Do not center the output")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False, help="Print debug messages")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("1 and only 1 pdf may be shrunk at a time")

    pdfIn = args[0]
    if options.pdfOut:
        pdfOut = options.pdfOut
    else:
        pdfOut = re.sub('\.[pP][dD][fF]$', '', pdfIn)
        pdfOut = pdfOut + '--shrunk.pdf'

    firstPage = options.firstPage

    # Get numPagesInFile using PyPDF
    pdfReader = PdfFileReader(open(pdfIn, 'rb'))
    numPagesInFile = pdfReader.getNumPages()
    pageSize = pdfReader.getPage(firstPage).mediaBox.upperRight
    if options.debug: print("numPagesInFile: " + str(numPagesInFile))

    if options.lastPage <= 0:
        lastPage = numPagesInFile
    else:
        lastPage = options.lastPage

    if lastPage > numPagesInFile:
        lastPage = numPagesInFile

    x = float(pageSize[0])
    y = float(pageSize[1])

    if x > y:
        xPrime = y
        yPrime = x / 2.0
    else:
        xPrime = y / 2.0
        yPrime = x

    xScale = xPrime / x
    yScale = yPrime / y

    if xScale < yScale:
        scale = xScale
    else:
        scale = yScale

    xTranslate = (xPrime - scale * x)
    yTranslate = (yPrime - scale * y)

    if options.center:
        xTranslate = xTranslate / 2.0
        yTranslate = yTranslate / 2.0

    i = 0
    writer = PdfFileWriter()
    while i < numPagesInFile:
        page = pdf.PageObject.createBlankPage(width=xPrime, height=yPrime)
        page.mergeScaledTranslatedPage(pdfReader.getPage(i), scale, xTranslate, yTranslate)
        writer.addPage(page)
        i += 1

    writer.write(open(pdfOut, 'wb'))

    print("Completed!  Shrunk PDF is in " + pdfOut)

if __name__ == "__main__":
    main()
