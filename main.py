import telebot
from os import getenv, listdir
from PIL import Image, ImageDraw, ImageFont
from templates import templates
from io import BytesIO
from helper import measure_font_size
from db import base, User, TemplateUse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

bot = telebot.TeleBot(getenv("TOKEN"))

engine = create_engine("sqlite:///data.db")
base.metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()

@bot.message_handler(commands=["start"])
def receive_start(message):
    chat_id = message.chat.id
    user = User(chat_id)
    if session.query(User).filter_by(chat_id=chat_id).first() is None:
        session.add(user)
        session.commit()
    bot.send_message(chat_id, "Welcome. I can help you send memes.")
    
@bot.message_handler(commands=["make"])
def receive_make_meme(message):
    chat_id = message.chat.id
    template_id, *text = message.text[6:].split(",")
    template_id = int(template_id)
    if template_id in templates:
        template_info = templates[template_id]
        coordinates = template_info["position"]
        color = template_info["color"]
        with Image.open("templates/%s.png"%template_id) as template:
            draw = ImageDraw.Draw(template)
            for i in range(min(len(coordinates), len(text))):
                font = ImageFont.truetype("fonts/impact.ttf", measure_font_size(text[i]))
                width, _ = draw.textsize(text[i], font)
                x = coordinates[i][0] - (width / 2)
                y = coordinates[i][1]
                draw.text((x, y), text[i].upper(), font=font, fill=color)
            f = BytesIO()
            template.save(f, "PNG")
            bot.send_photo(chat_id, f.getvalue())
    else:
        bot.send_message(chat_id, "Template not found.")
    
    
@bot.message_handler(commands=["template"])
def receive_get_template(message):
    chat_id = message.chat.id
    try:
        template_id = int(message.text[10:])
        if template_id in templates:
            with open("templates/%s.png"%template_id, "rb") as template:
                bot.send_photo(chat_id, template)
        else:
            bot.send_message(chat_id, "Template not found.")
    except ValueError:
        bot.send_message(chat_id, "Please type an integer.")
        
bot.polling()