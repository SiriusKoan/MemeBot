from os import getenv
from uuid import uuid4
import telebot
from telebot import types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from templates import templates
from helper import make_meme, generate_example_text
from db import base, User, TemplateTotalUse, Memes
from messages import help_msg, welcome

TOKEN = getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

engine = create_engine("sqlite:///data.db/?check_same_thread=False")
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
    bot.send_message(chat_id, help_msg, parse_mode="Markdown")


# make a meme
@bot.message_handler(commands=["make"])
def receive_make_meme(message):
    chat_id = message.chat.id
    try:
        args = message.text[message.text.index(" ")+1:]
    except IndexError:
        bot.send_message(chat_id, "Please enter the template ID and the text.")
        return
    
    template_id, *text = args.split(",")
    try:
        template_id = int(template_id)
    except ValueError:
        bot.send_message(chat_id, "Template ID should be an integer.")
    else:
        if template_id in templates:
            if (
                session.query(TemplateTotalUse)
                .filter_by(template_id=template_id)
                .first()
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

            if chat_id > 0:
                callback_data = ",".join(["store", str(template_id), *text])
                if len(callback_data.encode("utf-8")) <= 64:
                    kb = types.InlineKeyboardMarkup()
                    kb.row(
                        types.InlineKeyboardButton(
                            "Store and publish", callback_data=callback_data
                        )
                    )
                    bot.send_photo(chat_id, make_meme(template_id, text), reply_markup=kb)
                else:   # size of callback_data exceeds telegram API limit (64 bytes)
                    bot.send_message(chat_id, "Unable to publish: The length of text is too long to store.")
                    bot.send_photo(chat_id, make_meme(template_id, text))
            else:
                bot.send_photo(chat_id, make_meme(template_id, text))
        else:
            bot.send_message(chat_id, "Template not found.")


# show template usage
@bot.message_handler(commands=["template"])
def receive_get_template(message):
    chat_id = message.chat.id
    try:
        template_id = int(message.text.split(" ")[1])
    except ValueError:
        bot.send_message(chat_id, "Please enter a valid template id.")
    except IndexError:
        bot.send_message(chat_id, "Please enter a template ID.")
    else:
        if template_id in templates:
            bot.send_photo(
                chat_id, make_meme(template_id, generate_example_text(template_id))
            )
        else:
            bot.send_message(chat_id, "Template not found.")


# get published meme by its ID
@bot.message_handler(commands=["publish"])
def receive_send_published(message):
    chat_id = message.chat.id
    try:
        ID = message.text.split(" ")[1]
    except IndexError:
        bot.send_message(chat_id, "Please enter a meme ID.")
        return
    
    try:
        ID = int(ID)
    except ValueError:
        bot.send_message(chat_id, "Please enter a valid meme ID.")
    except IndexError:
        bot.send_message(chat_id, "Please enter a meme ID.")
    else:
        meme = session.query(Memes).filter_by(ID=ID).first()
        if meme is not None:
            template_id = meme.template_id
            text = [meme.text1, meme.text2, meme.text3, meme.text4]
            bot.send_photo(chat_id, make_meme(template_id, text))
        else:
            bot.send_message(chat_id, "Meme not found.")


@bot.message_handler(commands=["rank"])
def receive_rank(message):
    chat_id = message.chat.id
    rank = []
    msg = ""
    records = session.query(TemplateTotalUse).all()
    for record in records:
        rank.append((record.template_id, record.use))
    rank = sorted(rank, key=lambda record: record[1])
    rank.reverse()
    for i in range(len(rank)):
        # msg format: 1. template [template_id] is used for [use] times
        msg += " ".join(
            [
                str(i + 1) + ".",
                "template",
                str(rank[i][0]),
                "is used for",
                str(rank[i][1]),
                "times",
            ]
        )
        msg += "\n"
    bot.send_message(chat_id, msg)


# store meme callback, from receive_make_meme function
@bot.callback_query_handler(lambda call: "store" in call.data)
def receive_store_meme(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    meme = Memes(chat_id, *call.data.split(",")[1:])
    session.add(meme)
    session.commit()
    session.refresh(meme)

    kb = types.InlineKeyboardMarkup()
    kb.row(types.InlineKeyboardButton("Success", callback_data="none"))
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=msg_id, reply_markup=kb)
    bot.send_message(
        chat_id,
        "You can access this by typing `/publish %d`." % meme.ID,
        parse_mode="Markdown",
    )


bot.polling()