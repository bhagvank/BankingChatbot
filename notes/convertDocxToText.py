from docx import Document

def convertDocxToText(path):
	document = Document(path)
    #print("doc path")
	return "\n".join([para.text for para in document.paragraphs])


