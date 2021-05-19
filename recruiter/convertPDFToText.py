import PyPDF2 
import textract
#from nltk.tokenize import word_tokenize
#from nltk.corpus import stopwords

def convertPDFToText(path):

    filename = path #open allows you to read the file
    pdfFileObj = open(filename,'rb')#The pdfReader variable is a readable object that will be parsed
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)#discerning the number of pages will allow us to parse through all #the pages
    num_pages = pdfReader.numPages
    count = 0
    text = ""#The while loop will read each page
    while count < num_pages:
          pageObj = pdfReader.getPage(count)
          count +=1
          text += pageObj.extractText()#This if statement exists to check if the above library returned #words. It's done because PyPDF2 cannot read scanned files.
            
    #print(text)        
    return text