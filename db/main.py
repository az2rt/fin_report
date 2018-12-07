#-*- coding: utf-8 -*-
from sqlalchemy import create_engine
#from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PreStage(Base):
    """
    Класс для подготовки бд перед заливкой из json
    """

    pass