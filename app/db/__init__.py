from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

db = create_engine('sqlite:///sleepy.db')
Base = declarative_base()
Session = sessionmaker(bind=db)

class Source(Base):
	__tablename__ = 'sources'

	id = Column(Integer, primary_key=True)
	name = Column(String(255), nullable=False)
	type = Column(String(32), nullable=False)

	url = Column(String(255))
	username = Column(String(255), nullable=False)
	password = Column(String(255), nullable=False)

	playlists = relationship('SourcePlaylist', backref='source', cascade='all, delete, delete-orphan')

class SourcePlaylist(Base):
	__tablename__ = 'source_playlists'

	id = Column(Integer, primary_key=True)
	source_id = Column(Integer, ForeignKey('sources.id'))
	name = Column(String(255), nullable=False)