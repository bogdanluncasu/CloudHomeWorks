import re
import Controller

class Router(object):

    def __init__(self, server):
        self.get_routes = []
        self.post_routes = []
        self.put_routes = []
        self.delete_routes = []

        self.server = server

    def addGetRoute(self, url, controller, action):
        self.get_routes.append({'url': url, 'controller': controller, 'action': action})
    def addPostRoute(self, url, controller, action):
        self.post_routes.append({'url': url, 'controller': controller, 'action': action})
    def addPutRoute(self, url, controller, action):
        self.put_routes.append({'url': url, 'controller': controller, 'action': action})
    def addDeleteRoute(self, url, controller, action):
        self.delete_routes.append({'url': url, 'controller': controller, 'action': action})
        
    def route(self, path, method):
        if method == "GET":
            routes=self.get_routes
        elif method == "POST":
            routes=self.post_routes
        elif method == "PUT":
            routes=self.put_routes
        elif method == "DELETE":
            routes=self.delete_routes
        else:
            self.server.send_response(500)
            self.server.end_headers()       
        for route in routes:
            print(route['url'], path)
            s=re.search(route['url'], path)
            
            if s:
                
                module=globals()["Controller"].__dict__
                controller_class = module[route['controller']]
                action_function = controller_class.__dict__[route['action']]
                obj = controller_class(self.server)
                try:
                    print s.groups()
                    if method=="POST" or method == "DELETE" or (method=="GET" and len(s.groups())>0):
                        apply(action_function,(obj, s.group(1)))
                    else:
                        apply(action_function,(obj, ))
                except ValueError:
                    self.server.send_response(400)
                    self.server.send_header('Content-type', 'application/json')
                    self.server.end_headers()
                    dict["data"]={"message":"Invalid put data"}
                    self.server.wfile.write(json.dumps(dict,indent=4))
                return

        self.server.send_response(404)
        self.server.end_headers()