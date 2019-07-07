#!/usr/bin/python

# pdfbooklet.py
#
# Copyright (c) 2014 Mark O. Busby <mark@busbycreations.com>
#
# Licensed under the MIT/X11 license - see LICENSE.txt
#
# Create booklet from selected pdf file, in selected page range
# Depends on pyPDF2

from optparse import OptionParser
import re
from PyPDF2 import pdf, PdfFileWriter, PdfFileReader

def main():
    parser = OptionParser(usage="usage: %prog [options] PDF-file")
    parser.add_option("-o", "--out", dest="pdfOut", help="Name of PDF File to create")
    parser.add_option("-f", "--first", type="int", dest="firstPage", default=1, help="First page of booklet")
    parser.add_option("-l", "--last", type="int", dest="lastPage", default=0, help="Last page of booklet")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False, help="Print debug messages")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("1 and only 1 pdf may be bookletized at a time")

    pdfIn = args[0]
    if options.pdfOut:
        pdfOut = options.pdfOut
    else:
        pdfOut = re.sub('\.[pP][dD][fF]$', '', pdfIn)
        pdfOut = pdfOut + '--booklet.pdf'

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

    numPages = 1 + lastPage - firstPage
    if options.debug: print("numPages: " + str(numPages))
    numSheets = numPages / 4
    if options.debug: print("numSheets: " + str(numSheets))
    if (numPages % 4 > 0):
    #if ((numPages > 4) & ((numPages % 4 > 0) | (numSheets == 0))):
        if options.debug: 
            print("numPages % 4 = " + str(numPages % 4))
            print("Adding extra sheet.")
        numSheets += 1
    if options.debug: print("numSheets: " + str(numSheets))

    pagesToPrint = numSheets * 4
    numBlankPages = pagesToPrint - numPages
    frontOffset = 0
    backOffset = 1

    pagesInOrder = []
    pagesInOrder.append(firstPage + pagesToPrint - 1)
    if options.debug: print("pagesToPrint: " + str(pagesToPrint))
    while len(pagesInOrder) < pagesToPrint:
        pagesInOrder.append(firstPage + frontOffset)
        pagesInOrder.append(firstPage + 1 + frontOffset)
        frontOffset += 2
        pagesInOrder.append(firstPage + pagesToPrint - 1 - backOffset)
        pagesInOrder.append(firstPage + pagesToPrint - 1 - backOffset - 1)
        backOffset += 2
    del(pagesInOrder[len(pagesInOrder) - 1])
    if options.debug: print(pagesInOrder)

    # Create 2-per-page PDF, ready for printing
    # This is done by creating a side-ways page, and overlaying two scaled pages
    # on top.  US Letter is 612 x 792 pts (portrait)
    x = float(pageSize[0])
    y = float(pageSize[1])
    xPrime = 792
    yPrime = 612
    scale = 0.5 * xPrime / x
    scale2 = yPrime / y
    if (scale > scale2): scale = scale2
    yOffset = (yPrime - scale * y) / 2
    yOffsetLeft = yOffset
    xOffsetLeft = (xPrime - 2 * scale * x) / 4
    xOffset = xOffsetLeft + xPrime / 2

    # detecting if pages are already landscape
    landscape = False
    if x > y:
        landscape = True
        xPrime = 612
        yPrime = 792
        scale = 0.5 * yPrime / y
        scale2 = xPrime / x
        if (scale > scale2): scale = scale2
        xOffset = (xPrime - scale * x) / 2
        xOffsetLeft = xOffset
        yOffset = (yPrime - 2 * scale * y) / 4
        yOffsetLeft = yOffset + yPrime / 2

    if options.debug: print('landscape: ', landscape)
    if options.debug: print('x: ', x)
    if options.debug: print('y: ', y)
    if options.debug: print('xPrime: ', xPrime, xPrime / 2)
    if options.debug: print('yPrime: ', yPrime, yPrime / 2)
    if options.debug: print('scale: ', scale, scale * x, scale * y)
    if options.debug: print('xOffset: ', xOffset)
    if options.debug: print('yOffset: ', yOffset)
    if options.debug: print('xOffsetLeft: ', xOffsetLeft)
    if options.debug: print('yOffsetLeft: ', yOffsetLeft)

    writer = PdfFileWriter()
    leftPage = True
    for pageNum in pagesInOrder:
        if pageNum > lastPage:
            page = pdf.PageObject.createBlankPage(width=x, height=y)
        else:
            page = pdfReader.getPage(pageNum - 1)

        if leftPage == True:
            combinedPage = pdf.PageObject.createBlankPage(width=xPrime, height=yPrime)
            combinedPage.mergeScaledTranslatedPage(page, scale, xOffsetLeft, yOffsetLeft)
        else:
            combinedPage.mergeScaledTranslatedPage(page, scale, xOffset, yOffset)
            writer.addPage(combinedPage)

        leftPage = not leftPage

    writer.write(open(pdfOut, 'wb'))
    print("Completed!  Booklet is in " + pdfOut)

if __name__ == "__main__":
    main()
