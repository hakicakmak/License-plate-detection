import pytesseract

# OS degiskeni 0 ise Windows, 1 ise diger işletim sistemleri (Unix/Linux/Mac)
OS = 1

if OS == 0:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
else:
    pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
