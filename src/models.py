from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from database import Base

class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)

    submenus = relationship('Submenu', backref='menu')

class Submenu(Base):
    __tablename__ = "submenu"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    menu_id = Column(Integer, ForeignKey("menu.id", ondelete="CASCADE"), nullable=False)

    dishes = relationship('Dish', backref='submenu')


class Dish(Base):
    __tablename__ = "dish"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    price = Column(Numeric(precision=12, scale=2))
    submenu_id = Column(Integer, ForeignKey("submenu.id", ondelete="CASCADE"), nullable=False)