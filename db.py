from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class User(base):
    __tablename__ = "users"
    ID = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True, nullable=False)
    
    def __init__(self, chat_id):
        self.chat_id = chat_id
        
class TemplateTotalUse(base):     # record total use
    __tablename__ = "templates_use"
    ID = Column(Integer, primary_key=True)
    template_id = Column(Integer, unique=True, nullable=False)
    use = Column(Integer, default=1)
    
    def __init__(self, template_id):
        self.template_id = template_id
        
class Memes(base):
    __tablename__ = "memes"
    ID = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    template_id = Column(Integer, nullable=False)
    text1 = Column(String)
    text2 = Column(String)
    text3 = Column(String)
    
    def __init__(self, chat_id, template_id, text1, text2, text3):
        self.chat_id = chat_id
        self.template_id = template_id
        self.text1 = text1
        self.text2 = text2
        self.text3 = text3
    