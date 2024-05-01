import re

class AuxiliaryHandlers:
    def __init__(self, margin, cst, aliquot):
        self.margin = margin
        self.cst = cst
        self.aliquot = aliquot


    def __clean_product_name(self, text):
        """Limpa o nome do produto, removendo preposições."""
        remove_words = ['A', 'E', 'DA', 'DE', 'DO']
        text = [word for word in text.split(' ') if word not in remove_words]
        text = ' '.join(text)
        return text  
    

    def __check_fixed_margin(self, name):
        """Verifica se o preço é válido."""
        fixed_price_product = {
            'tire': [r'PNEU \d{2} \d{2,}/\d{2,} .+', 30],
            'oil': [r'OLEO MOTOR', 30]
        }
        for product, pattern in fixed_price_product.items():
            if re.match(pattern[0], name):
                return pattern[1]
        return False
    

    def __calculate_margin(self, name, price):
        """Calcula o valor do margem."""
        fixed_margin = self.__check_fixed_margin(name)
        if self.__check_fixed_margin:
            return str(fixed_margin)
        cost_price = float(price) 
        sale_price = cost_price * int(self.margin)
        new_margin = round(((sale_price - cost_price) / cost_price) * 100)
        if int(self.margin) < 10:
            return str(new_margin).replace('.', ',')
        return str(self.margin).replace('.', ',')
        

    def handle_product_values(self, product):
        """Adciona os valores corretos."""
        product['name'] = self.__clean_product_name( product['name'] )
        product['price'] = product['price'].replace('.', ',')
        product['margin'] = self.__calculate_margin( product['name'], product['price'].replace(',', '.') )
        product['cst'] = self.cst
        product['aliquot'] = self.aliquot
        return product