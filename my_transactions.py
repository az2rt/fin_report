

class Transactions:

    def __init__(self, query):
        self.name = query['name']
        self.id = query['id']
        self.type = query['type']
        self.category_id = query['categoryId']
        self.date = query['date']
        self.sum = query['sum']
        self.account = query['accountId']
        self.desc = query['description']
        self.source = query['source']
        self.available = query['available']

    def return_list(self):
        return (self.id, self.name, self.type, self.category_id, self.date, self.sum, self.account, self.desc,
                self.source, self.available)



