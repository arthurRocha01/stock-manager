import pyautogui
import pyperclip
import sys
from time import sleep

from .DBManager import DBManager
   
class Scraper:
    def __init__(self, quantity_products, wait_time):
        self.output_file = 'database.json'
        self.quantity_products = quantity_products
        self.wait_time = wait_time
        self.speed_mouse = 0.5
        self.iteration_count = 0
        self.field_positions = {}
        self.db_handler = DBManager()
        
        
    def __start_RPA(self):
        """Inicia o fluxo do RPA."""
        self.field_positions = self.__get_field_positions()
        pyautogui.alert('ATENÇÃO!!: Não use o mouse e teclado, pode atrapalhar o fluxo do RPA.')
        self.__move_and_click('start_btn')


    def __alert_user(self, message):
        """Exibe uma mensagem para o usuário."""
        print(message)
        
        
    def __get_field_position(self, field_name):
        """Obtém a posição de um campo."""
        self.__alert_user(f'Mova o mouse para o ponto {field_name}...[5s]')
        sleep(3)
        x, y = pyautogui.position()
        self.__alert_user(f'{field_name}: {x}, {y}\n')
        return x, y
    
    
    def __get_field_positions(self):
        """Obtém as posições de todos os campos."""
        self.fields_name = [
            'start_btn', 'next_btn',
            'name', 'price', 'margin', 'cst', 'aliquot', 'ncm'
            ]
        for field_name in self.fields_name:
            self.field_positions[field_name] = self.__get_field_position(field_name)
        return self.field_positions
            
            
    def __move_and_click(self, field, clicks=1):
        """Move o mouse para o campo e clica."""
        pyautogui.moveTo(self.field_positions[field], duration=self.speed_mouse)
        pyautogui.click(clicks=clicks)


    def __select_field(self, field):
        x, y = self.field_positions[field]
        end_fields = {'name': x + (10 * 30), 'aliquot': x + (10 * 5)}
        self.__move_and_click(field, 0)
        pyautogui.dragTo(end_fields[field], y, 1, button='left')
        pyautogui.hotkey('ctrl', 'c')
        value = pyperclip.paste()
        return value
        
        
    def __scraper_values(self):
        """Extrai os valores do produto."""
        for field in self.fields_name[2:]:
            if field in ['name', 'aliquot']:
                self.__select_field(field)
            else:
                self.__move_and_click(field, clicks=2)
            pyautogui.hotkey('ctrl', 'c')
            value = pyperclip.paste()
            self.product[field] = value
        
        
    def __save(self, product):
        """Salva os dados do produto no banco de dados."""
        self.db_handler.add_product(**product)
        self.__alert_user(f'''Produto {self.iteration_count} armazenado!\n
                    {product['name']}
                    Preço: {product['price']}
                    Margin: {product['margin']}
                    CST: {product['cst']}
                    Aliquot: {product['aliquot']}
                    NCM: {product['ncm']}\n\n''')
        
        
    def __fields_scraper(self):
        """Obtém os dados do produto."""
        self.product = {}
        self.__scraper_values()
        self.__save(self.product)
    
    
    def run(self):
        """Executa."""
        self.__start_RPA()
        while True:
            self.__fields_scraper()
            self.iteration_count += 1
            if self.iteration_count == self.quantity_products:
                print('\n\nScraping finalizado!')
                sys.exit(0)