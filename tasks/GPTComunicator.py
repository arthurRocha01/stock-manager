import requests
import sys
import os

from .TextExtractor import TextExtractor

class GTPComunictor:
    def __init__(self, note_file):
        self.note_file = note_file
        self.note_output_file = ''
        self.text_handler = TextExtractor()
        
        
    def __read_gpt_prompt(self):
        """Lê o prompt do GPT."""
        print('Lendo prompt...')
        path = '/home/nmqvl/Code/stock_manager/resources/prompt_gpt.txt'
        try:
            with open(path, 'r', encoding='utf-8') as file:
                prompt = file.read()
                return prompt
        except Exception as error:
            print(f'Ocorreu um erro ao ler o prompt para leitura: {error}')
            return sys.exit(1)
    
    
    def __get_gpt_response(self, prompt, text):
        """Obtém a resposta do modelo GPT-4."""
        apikey_gpt = os.getenv('OPENAI')    
        url = 'https://api.openai.com/v1/chat/completions'
        id_model = 'gpt-3.5-turbo'
        message = prompt + f'\n{text}'
        
        body_message = {
            'model': id_model,
            'messages': [{ 'role': 'user', 'content': message }]
        }
        headers = {'Authorization': f'Bearer {apikey_gpt}', 'Content-Type': 'application/json'}
        
        print('Esperando resposta...')
        try:
            request = requests.post(url, headers=headers, json=body_message)
            response_json = request.json()
            response = response_json['choices'][0]['message']['content']
            return response
        except requests.RequestException as error:
            print(f'Ocorreu um erro durante a solicitação HTTP: {error}')
            sys.exit(1)
        except Exception as error:
            print(f'Ocorreu um erro inesperado: {error}')
            sys.exit(1)
            
            
    def __get_output_filename(self):
        """Obtêm o nome do arquivo de saída."""
        filename = os.path.basename(self.note_file)
        name, extension = os.path.splitext(filename)
        self.note_output_file = name + '.csv'


    def __writer_response(self, response):
        self.__get_output_filename()
        print(f'{response}\n')
        try:
            with open(self.note_output_file, 'w', encoding='utf-8') as nfs:
                nfs.write(response)
        except Exception as error:
            print(f'Ocorreu um erro durante a conversão do PDF para CSV: {error}')
    
    
    def __convert_to_csv(self):
        """Monta estrutura da nota em CSV."""
        print('Montando csv...')
        prompt = self.__read_gpt_prompt()
        pdf_text = self.text_handler.extract_to_text(self.note_file)
        response = self.__get_gpt_response(prompt, pdf_text)
        self.__writer_response(response)
            
            
            
    def comunicate_gpt(self):
        """Comunicação com o GPT."""
        self.__convert_to_csv()