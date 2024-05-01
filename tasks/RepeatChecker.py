from fuzzywuzzy import fuzz
import re
import json

from .Logger import Logger


class RepeatChecker:
    def __init__(self, pct):
        self.path_db = 'resources/database.json'
        self.database = json.load(open(self.path_db))
        self.pct = pct
        self.logger = Logger()
    
    
    def __clean_text(self, text):
        """Remove pontuações, carecteres especiais e preposições."""
        text = re.sub(r'[^\w\s]', ' ', text)
        text = text.split()
        remove_words = ['A', 'E', 'DA', 'DE', 'DO']
        text = [word for word in text if word not in remove_words]
        return  ' '.join(text)

    
    def __calculate_similarity_name(self, new_product_name, registered_product_name):
        """Calcula a similaridade entre duas palavras."""
        new_product_name = self.__clean_text(new_product_name)
        registered_product_name = self.__clean_text(registered_product_name)
        similarity = fuzz.token_sort_ratio(new_product_name, registered_product_name)
        return similarity
    

    def __calculate_similarity_price(self, new_product_price, registered_product_price):
        """Calcula a similaridade entre os preços do produto."""
        new_product_price = float(new_product_price.replace(',', '.'))
        registered_product_price = float(registered_product_price.replace(',', '.'))
        diference = new_product_price - registered_product_price
        if diference > 20 or diference < (registered_product_price/3):
            return False
        return True
    

    def __get_most_similar_product(self, new_product, registered_products):
        """Retorna o produto coma maior similiaridade."""
        max_similarity = 0
        most_similar_product = None
        print(registered_products)

        for registered_product in registered_products:
            layer_one = new_product['ncm'] == registered_product['ncm']
            layer_two = self.__calculate_similarity_price(new_product['price'], registered_product['price'])
            similarity_name = self.__calculate_similarity_name(new_product['name'], registered_product['name'])

            if layer_one and layer_two and similarity_name > self.pct:
                if similarity_name > max_similarity:
                    max_similarity = similarity_name
                    most_similar_product = [registered_product['name'], max_similarity]
        return most_similar_product
    
    
    def to_check(self, new_product):
        """Verifica se uma palavra está repetida."""
        registered_products = []
        for product in self.database.items():
            registered_products.append({ 'name': product[0], 'price': product[1]['price'], 'ncm': product[1]['ncm'] })
        most_similar_product = self.__get_most_similar_product(new_product, registered_products)

        if most_similar_product is not None:
            if most_similar_product > self.pct:
                self.logger.print(f'''---Produto repetido: {new_product['name']}
                        {most_similar_product[0]}
                        Similiaridade: {most_similar_product[1]}---\n''')
                self.logger.print('*****--*****--*****-*****--*****--*****--*****--*****\n\n')
                return True
        self.logger.print('--Nenhum produto similar encontrado.---')
        return False