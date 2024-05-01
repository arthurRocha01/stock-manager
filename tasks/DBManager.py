import json


class DBManager:
    def __init__(self):
        self.database_path = 'resources/database.json'
        self.database = self.__load_database(self.database_path)


    def __load_database(self, database_path):
        """Carrega o banco de dados."""
        try:
            with open(database_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        

    def __save_stock(self, stock):
        """Salva o banco de dados."""
        with open(self.database_path, 'w') as database:
            json.dump(stock, database, indent=4)


    def add_product(self, name, price, margin, cst, ncm, aliquot):
        """Adciona o produto ao banco de dados."""
        self.database[name] = {'price': price, 'margin': margin, 'cst': cst, 'ncm': ncm, 'aliquot': aliquot }
        self.__save_stock(self.database)


    def get_stock(self, name):
        """Obtém o produto do banco de dados."""
        return self.database.get(name, None)


    def delete_product(self, name):
        """Deleta o produto do banco de dados."""
        if name in self.database:
            del self.database[name]
            self.__save_stock(self.database)
            return True
        else:
            return False