from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from Router import Router

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):        
        get_routes = [
            {'url': '/api/?$', 'controller': 'HomeController', 'action': 'getApi'},
            {'url': '/api/books/?$', 'controller': 'BooksController', 'action': 'getBooks'},
            {'url': '/api/books/([1-9]+d*)$', 'controller': 'BooksController', 'action': 'getBook'}

        ]

        post_routes = [
            {'url': '/api/books/([1-9]+d*)$', 'controller': 'BooksController', 'action': 'postBook'}
        ]
        put_routes = [
            {'url': '/api/books/?$', 'controller': 'BooksController', 'action': 'putBook'}
        ]
        delete_routes = [
            {'url': '/api/books/([1-9]+d*)$', 'controller': 'BooksController', 'action': 'deleteBook'}
        ]
        self.router = Router(self)

        for route in get_routes:
            self.router.addGetRoute(route['url'], route['controller'], route['action'])
        for route in post_routes:
            self.router.addPostRoute(route['url'], route['controller'], route['action'])
        for route in put_routes:
            self.router.addPutRoute(route['url'], route['controller'], route['action'])
        for route in delete_routes:
            self.router.addDeleteRoute(route['url'], route['controller'], route['action'])

        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
    
    def do_GET(self):
        self.router.route(self.path,"GET")
    def do_POST(self):
        self.router.route(self.path,"POST")
    def do_PUT(self):
        self.router.route(self.path,"PUT")
    def do_DELETE(self):
        self.router.route(self.path,"DELETE")


def main():
    try:
         httpd = HTTPServer(('', 8000), RequestHandler)
         print('Server started...')
         httpd.serve_forever()
    except:
         print('Server shutting down')
         httpd.socket.close()

if __name__ == '__main__':
    main()