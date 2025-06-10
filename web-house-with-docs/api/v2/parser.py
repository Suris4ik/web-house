from flask_restful.reqparse import RequestParser


class ParserUsers(RequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument('email', required=False)
        self.add_argument('login', required=False)
        self.add_argument('password', required=False)
        self.add_argument('is_admin', required=False)


class ParserPosts(RequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument('user_id', required=True)
        self.add_argument('body', required=True)
        self.add_argument('categories', required=False)


class ParserCategories(RequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument('name', required=True)
