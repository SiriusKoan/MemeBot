import telebot
from telebot import types
from os import getenv, listdir
from templates import templates
from helper import make_meme, generate_example_text
from db import base, User, TemplateTotalUse, Memes
from messages import help, welcome
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

bot = telebot.TeleBot(getenv("TOKEN"))

engine = create_engine("sqlite:///data.db")
base.metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()

# start
@bot.message_handler(commands=["start", "help"])
def receive_start(message):
    chat_id = message.chat.id
    user = User(chat_id)
    if session.query(User).filter_by(chat_id=chat_id).first() is None:
        session.add(user)
        session.commit()
    bot.send_message(chat_id, welcome)
    bot.send_message(chat_id, help, parse_mode="Markdown")


# make a meme
@bot.message_handler(commands=["make"])
def receive_make_meme(message):
    chat_id = message.chat.id
    msg_id = message.message_id
    template_id, *text = message.text[6:].split(",")
    template_id = int(template_id)
    if template_id in templates:
        if (
            session.query(TemplateTotalUse).filter_by(template_id=template_id).first()
            is None
        ):
            use = TemplateTotalUse(template_id)
            session.add(use)
            session.commit()
        else:
            use = (
                session.query(TemplateTotalUse)
                .filter_by(template_id=template_id)
                .first()
            )
            use.use = TemplateTotalUse.use + 1
            session.commit()

        kb = types.InlineKeyboardMarkup()
        callback_data = "/".join(["store", str(template_id), *text])
        kb.row(
            types.InlineKeyboardButton("Store and publish", callback_data=callback_data)
        )
        bot.send_photo(
            chat_id, make_meme(template_id, text), reply_markup=kb
        )
    else:
        bot.send_message(chat_id, "Template not found.")


# show template usage
@bot.message_handler(commands=["template"])
def receive_get_template(message):
    chat_id = message.chat.id
    try:
        template_id = int(message.text[10:])
        if template_id in templates:
            bot.send_photo(chat_id, make_meme(template_id, generate_example_text(template_id)))
        else:
            bot.send_message(chat_id, "Template not found.")
    except ValueError:
        bot.send_message(chat_id, "Please type an integer.")
        

# get published meme by its ID
@bot.message_handler(commands=["publish"])
def receive_send_published(message):
    chat_id = message.chat.id
    ID = message.text[8:]
    try:
        ID = int(ID)
    except:
        bot.send_message(chat_id, "Please type an integer.")
    else:
        meme = session.query(Memes).filter_by(ID=ID).first()
        if meme is not None:
            template_id = meme.template_id
            text = [meme.text1, meme.text2, meme.text3, meme.text4]
            try:
                text.remove(None)
            except:
                pass
            bot.send_photo(chat_id, make_meme(template_id, text))
        else:
            bot.send_message(chat_id, "Meme not found.")


# store meme callback
@bot.callback_query_handler(func=lambda call: "store" in call.data)
def receive_store_meme(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    meme = Memes(chat_id, *call.data.split("/")[1:])
    session.add(meme)
    session.commit()
    session.refresh(meme)

    # TODO make kb invalid
    # kb = types.InlineKeyboardMarkup()
    # kb.row(types.InlineKeyboardButton("Success"))
    # bot.edit_message_reply_markup(chat_id=chat_id, message_id=msg_id, reply_markup=kb)
    bot.send_message(chat_id, "You can access this by typing `/publish %d`." % meme.ID, parse_mode="Markdown")


bot.polling()