import telebot
from os import getenv
from PIL import Image, ImageDraw, ImageFont
from templates import templates
from io import BytesIO, BufferedReader

bot = telebot.TeleBot(getenv("TOKEN"))

@bot.message_handler(commands=["start"])
def receive_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Welcome. I can help you send memes.")
    
@bot.message_handler(commands=["make"])
def receive_make_meme(message):
    chat_id = message.chat.id
    template_id, *text = message.text[6:].split("/")
    template_id = int(template_id)
    if template_id in templates:
        coordinates = templates[template_id]
        with Image.open("templates/%s.png"%template_id) as template:
            draw = ImageDraw.Draw(template)
            for i in range(min(len(coordinates), len(text))):
                draw.text(coordinates[i], text[i])
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