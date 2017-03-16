import json
import sqlite3

class HomeController(object):
    def __init__(self,server):
        self.server=server

    def getApi(self):
        dict={}


        dict["data"]={"message":"Api version: 1.0"}
        obj=json.dumps(dict,indent=4)

        self.server.send_response(200)
        self.server.send_header('Content-type', 'application/json')
        self.server.end_headers()
        self.server.wfile.write(obj)

class BooksController(object):
    def __init__(self,server):
        self.server=server


    def getBooks(self):
        dict={}
        conn = sqlite3.connect('cc.db')
        cursor=conn.execute("Select * from book")
        
        data={}

        books=[]
        for row in cursor:
            book={
                "bookId":row[0],
                "author":row[1],
                "name":row[2]
                }

            books.append(book)
        data["message"]=books
        dict["data"]=data

        conn.close()

        self.server.send_response(200)
        self.server.send_header('Content-type', 'application/json')
        self.server.end_headers()
        self.server.wfile.write(json.dumps(dict,indent=4))


    def putBook(self):
        dict={}

        data_string = self.server.rfile.read(int(self.server.headers['Content-Length']))

        book=json.loads(data_string)

        if "author" in book and "name" in book:
            conn = sqlite3.connect('cc.db')
            conn.execute("INSERT INTO BOOK (Author,Name) \
                  VALUES ('"+book["author"]+"','"+book["name"]+"')");
            conn.commit();
            conn.close()
        else:
            raise ValueError()

        dict["data"]={"message":"Book successfully added"}
        self.server.send_response(201)
        self.server.send_header('Content-type', 'application/json')
        self.server.end_headers()
        self.server.wfile.write(json.dumps(dict,indent=4))



    def postBook(self,id):
        dict={}

        data_string = self.server.rfile.read(int(self.server.headers['Content-Length']))

        book=json.loads(data_string)

        if "author" in book and "name" in book:
            conn=sqlite3.connect("cc.db")
            cursor=conn.execute("select name from book where id="+str(id))
            if len(cursor.fetchall())>0:
                conn.execute("update book set author='"+book["author"]+"', name='"+book["name"]+"' where id= "+str(id) )
                conn.commit()
                conn.close()
                dict["data"]={"message":"Book successfully updated"}
                self.server.send_response(200)
                self.server.send_header('Content-type', 'application/json')
                self.server.end_headers()
                self.server.wfile.write(json.dumps(dict,indent=4))
            else:
                conn.close()
                dict["data"]={"message":"No such a book"}
                self.server.send_response(404)
                self.server.send_header('Content-type', 'application/json')
                self.server.end_headers()

                self.server.wfile.write(json.dumps(dict,indent=4))


    def deleteBook(self,id):
        dict={}

        data_string = self.server.rfile.read(int(self.server.headers['Content-Length']))

        book=json.loads(data_string)

        conn=sqlite3.connect("cc.db")
        cursor=conn.execute("select name from book where id="+str(id))

        if len(cursor.fetchall())>0:
            conn.execute("delete from book where id= "+str(id) )
            conn.commit()
            conn.close()
            dict["data"]={"message":"Book successfully deleted"}
            self.server.send_response(204)
            self.server.send_header('Content-type', 'application/json')
            self.server.end_headers()
        else:
            conn.close()
            dict["data"]={"message":"No such a book"}
            self.server.send_response(404)
            self.server.send_header('Content-type', 'application/json')
            self.server.end_headers()

            self.server.wfile.write(json.dumps(dict,indent=4))

    def getBook(self,id):
        dict={}
        conn = sqlite3.connect('cc.db')
        cursor=conn.execute("Select * from book where id="+id)
        
        
        i=0

        for row in cursor:
            i+=1
            book={
                "bookId":row[0],
                "author":row[1],
                "name":row[2]
                }

        if(i>0):
            dict["data"]={"message":book}
            self.server.send_response(200)
            self.server.send_header('Content-type', 'application/json')
            self.server.end_headers()
            self.server.wfile.write(json.dumps(dict,indent=4))
        else:
            dict["data"]={"message":"No such a book"}
            self.server.send_response(404)
            self.server.send_header('Content-type', 'application/json')
            self.server.end_headers()
            self.server.wfile.write(json.dumps(dict,indent=4))


        conn.close()





