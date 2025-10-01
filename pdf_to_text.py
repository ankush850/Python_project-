import PyPDF2
import os

if not os.path.isdir("temp"):
    os.mkdir("temp")

pdfpath = input("Enter the name of your pdf file - please use backslash when typing in directory path: ")
txtpath = input("Enter the name of your txt file - please use backslash when typing in directory path: ")

BASEDIR = os.path.realpath("temp")
print(BASEDIR)

if len(txtpath) == 0:
    txtpath = os.path.join(BASEDIR, os.path.basename(os.path.normpath(pdfpath)).replace(".pdf", "") + ".txt")

with open(pdfpath, 'rb') as pdfobj:
    pdfread = PyPDF2.PdfReader(pdfobj)
    num_pages = len(pdfread.pages)

    for i in range(num_pages):
        pageObj = pdfread.pages[i]
        text = pageObj.extract_text()
        with open(txtpath, 'a+', encoding='utf-8') as f:
            f.write(text)
        print(text)
