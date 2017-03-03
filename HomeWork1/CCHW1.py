import flask
import homework
from flask import request,render_template

app = flask.Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def hello_world():
    if request.method=="POST":
        senderEmail = request.form['senderEmail']
        senderPassword = request.form['senderPassword']
        email = request.form['email']
        return homework.sendemail(senderEmail,senderPassword,email)
        
    else:
        return render_template("index.html")

if __name__ == '__main__':
   app.run()