# Importações
import sys
import csv
import os
from time import sleep

import pyautogui

from .GPTComunicator import GTPComunictor
from .RepeatChecker import RepeatChecker
from .AuxiliaryHandlers import AuxiliaryHandlers
from .DBManager import DBManager
from .Logger import Logger

    
class Registrar: 
    def __init__(self, note_file, margin, cst, aliquot, safety_time, similarity, quantity_products=None):
        self.note_output_file = self.__get_output_filename(note_file)
        self.margin = margin
        self.cst = cst
        self.aliquot = aliquot
        self.quantity_products = quantity_products
        self.gpt_handler = GTPComunictor(note_file)
        self.repeat_checker = RepeatChecker(similarity)
        self.auxiliares = AuxiliaryHandlers(self.margin, self.cst, self.aliquot)
        self.db_handler = DBManager()
        self.logger = Logger()
        
        # Configuração do RPA
        self.mouse_speed = 0.5
        self.iteration_count = 0
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = safety_time
        

    # Métodos privados
    def __get_output_filename(self, note_file):
        """Obtêm o nome do arquivo de saída."""
        filename = os.path.basename(note_file)
        name, extension = os.path.splitext(filename)
        return  name + '.csv'
    

    def __get_field_positions(self):
        """Obtém as posições dos campos."""
        field_names = [
            'include_btn','confirmation_btn','data_btn',
            'name', 'price', 'margin', 'cst', 'aliquot', 'ncm'
            ]
        positions = {}
        for field_name in field_names:
            positions[field_name] = self.__get_field_position(field_name)
        return positions
        
        
    def __get_field_position(self, field_name):
        """Obtém a posição de um campo."""
        self.logger.print(f'Mova o mouse para o ponto {field_name}...[5s]')
        sleep(0)
        x, y = pyautogui.position()
        self.logger.print(f'{field_name}: {x}, {y}\n')
        return x, y
    
            
    def __read_csv(self):
        """Lê o arquivo CSV."""
        self.logger.print('Lendo csv...')
        try:
            with open(self.note_output_file, 'r', encoding='utf-8') as note:
                products = list(csv.DictReader(note))
                return products 
        except Exception as error:
            self.logger.print(f'Ocorreu um erro ao abrir o CSV para leitura: {error}')
            sys.exit(1)
        
    
    def __handler_database(self, product):
        """Adciona o produto ao banco de dados."""
        self.db_handler.add_product(**product)


    def __move_and_click(self, field, clicks=1):
        """Move o cursor do mouse e clica em um campo."""
        pyautogui.moveTo(self.field_positions[field], duration=self.mouse_speed)
        pyautogui.click(clicks=clicks)


    def __writer(self, field, value):
        """Escreve texto em um campo."""
        self.__move_and_click(field)
        pyautogui.write(value)


    def __save(self):
        """Clica no botão salvar."""
        self.__move_and_click('include_btn')
        self.__move_and_click('confirmation_btn')
        self.logger.print('Produto salvo!')
        self.logger.print('*****--*****--*****-*****--*****--*****--*****--*****\n\n')


    def __writer_values(self, product):
        """Escreve os valores do produto."""
        for field, value in product.items():
            self.__writer(field, value)
            self.logger.print(f'{field}: {value}')
        self.__save()


    def __process_product(self, product):
        """Lida com todos os processamentos do produto."""
        self.__handler_database(product)
        product = self.auxiliares.handle_product_values(product)
        return product


    def __register_product(self, product):
        """Registra o produto."""
        repeated = self.repeat_checker.to_check(product)
        if repeated:
            return
        product = self.__process_product(product)
        self.__writer_values(product)
        
        
    def __start_RPA(self):
        """Inicia o fluxo do RPA."""
        self.field_positions = self.__get_field_positions()
        pyautogui.alert('ATENÇÃO!!: Não use o mouse e teclado, pode atrapalhar o fluxo do RPA.')
        self.logger.print('Iniciando...\n')
        self.__move_and_click('include_btn')
        self.__move_and_click('data_btn')
        
            
    def run(self):
        """Executa o fluxo."""
        self.gpt_handler.comunicate_gpt()
        products = self.__read_csv()
        self.__start_RPA()
        for product in products:
            if (self.quantity_products is not None) and (self.quantity_products == self.iteration_count):
                break
            self.__register_product(product)
            self.iteration_count += 1