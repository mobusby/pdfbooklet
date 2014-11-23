#BusbyCreations pdfbooklet

Create ready-to-print booklets from PDFs

````
Usage: pdfbooklet.py [options] PDF-file

Options:
-h, --help                         show this help message and exit
-o PDFOUT, --out=PDFOUT            Name of PDF File to create
-f FIRSTPAGE, --first=FIRSTPAGE    First page of booklet
-l LASTPAGE, --last=LASTPAGE       Last page of booklet
-d, --debug                        Print debug messages
````

For example: `pdfbooklet.py -f32 -l68 -oChapterIWant.pdf MassiveBook.pdf`
Pages 32-68 of MassiveBook.pdf will be extracted, shuffled, rotated, and scaled and placed, two-per-page, on US Letter size sheets in ChapterIWant.pdf.  One may then print ChapterIWant.pdf, double-sided, using standard means, to create a booklet.

##Project Dependencies

This project depends on [pyPDF2](http://mstamy2.github.io/PyPDF2/). For the convenience of the developer, a copy is maintained with this project.
