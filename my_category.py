class Category:

    def __init__(self, query):
        self.name = query['name']
        self.id = query['id']
        self.type = query['type']
        self.available = query['available']
        self.order_id = query['orderId']
        self.parent_id = query['parentId']

    def return_list(self):
        return (self.id,self.name,self.type,self.available,self.order_id,self.parent_id)
