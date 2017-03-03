import requests
import os 
import base64
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import textwrap
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import mimetypes
import smtplib


API_KEY_WEATHER="4ac183658c2f42eb860183553172502"



def get_weather():

    r=requests.get("http://ip-api.com/json")
    ip=r.json()

    if(ip["status"]=="fail"):
        print("ERROR")
        raise SystemExit
    else:
       city=ip["city"]
       country=ip["country"]

       r=requests.get("http://api.apixu.com/v1/current.json?key="+API_KEY_WEATHER+"&q="+city)
       return r.json()["current"],city,country

def save_random_image():
    r=requests.get("http://lorempixel.com/640/480/",stream=True)
    if r.status_code == 200:
        with open("image.jpg", 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

def get_joke():
    r=requests.get("https://api.chucknorris.io/jokes/random")
    return r.json()["value"]


def save_meme(joke):
    img = Image.open("image.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("opensans.ttf", 16)

    lines = textwrap.wrap(joke, width=40)
    i=30
    for line in lines:
        draw.text((10, i),line,(0,255,100),font=font)
        i+=30
    
    img.save('meme.jpg')

def create_email(to,password,sender,subject,message_text,file):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'image':
        fp = open(file, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()

    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    {'raw': base64.urlsafe_b64encode(message.as_bytes())}
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()

    server.login(sender,password)

    server.sendmail(sender, to, message.as_string())


def get_service(sender,password,receiver):
    weather,city,country=get_weather()


    if weather["is_day"]:
        t="Day"
    else:
        t="Night"

    msg=city+","+country+"  \n Temperature: "+ str(weather["temp_c"])+" celsium degrees \n Time of the day: "+t


    save_random_image()
    save_meme(get_joke())
    create_email(receiver,password,sender,"Get your daily infos",msg,"meme.jpg")

def sendemail(sender,password,receiver):
    try:
        get_service(sender,password,receiver)
        return "SUCCESFULLY SENT"
    except smtplib.SMTPAuthenticationError:
        return "Wrong user and password"
    
