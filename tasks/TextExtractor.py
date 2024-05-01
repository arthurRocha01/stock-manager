import pdfplumber
import xml.etree.ElementTree as ET
import openpyxl


class TextExtractor:
    def __extract_pdf_text(self, file):
        """Extrai o texto do PDF."""
        print('Extraindo texto do PDF...')
        text = ''
        try:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text()
            return text
        except Exception as error:
            print(f'Ocorreu um erro durante a conversão do PDF para texto: {error}')
            
    
    def __extract_xml_text(self, file):
        """Extrai o texto de um arquivo XML."""
        print('Extraindo texto do XML...')
        text = ''
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            for element in root.iter():
                if element.text:
                    text += element.text.strip() + ' '
            return text
        except Exception as error:
            print(f'Ocorreu um erro durante a conversão do XML para texto: {error}')
            
            
    def __extract_xls_text(self, file):
        """Extrai o texto de um arquivo XLS."""
        print('Extraindo texto do XLS...')
        text = ''
        try:
            wb = openpyxl.open_workbook(file)
            for sheet in wb.sheetnames:
                ws = wb[sheet]
                for row in ws.iter_rows():
                    for cell in row:
                        if cell:
                            text += cell.value + ' '
            return text
        except Exception as error:
            print(f'Ocorreu um erro durante a conversão do XLS para texto: {error}')
            
            
    def extract_to_text(self, file):
        """Extrai o texto de um arquivo."""
        if file.endswith('.pdf'):
            return self.__extract_pdf_text(file)
        elif file.endswith('.xml'):
            return self.__extract_xml_text(file)
        elif file.endswith('.xls'):
            return self.__extract_xls_text(file)
        else:
            print(f'O arquivo {file} não é um arquivo PDF, XML ou XLS.')
            return None
                