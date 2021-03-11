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
    