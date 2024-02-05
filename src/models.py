from typing import Any

from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from database import Base


class UtilsClass(Base):
    __abstract__ = True

    def as_dict(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def stringify(self) -> dict[str, str]:
        dict = self.as_dict()
        for keys in dict:
            dict[keys] = str(dict[keys])
        return dict


class Menu(UtilsClass):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    submenus_count = Column(Integer, nullable=False, default=0)
    dishes_count = Column(Integer, nullable=False, default=0)

    submenus = relationship('Submenu', backref='menu')

    def __str__(self):
        return 'menu'


class Submenu(UtilsClass):
    __tablename__ = 'submenu'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(Integer, ForeignKey('menu.id', ondelete='CASCADE'), nullable=False)
    dishes_count = Column(Integer, nullable=False, default=0)

    dishes = relationship('Dish', backref='submenu')

    def __str__(self):
        return 'submenu'


class Dish(UtilsClass):
    __tablename__ = 'dish'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Numeric(precision=12, scale=2), nullable=False)
    submenu_id = Column(Integer, ForeignKey('submenu.id', ondelete='CASCADE'), nullable=False)

    def __str__(self):
        return 'dish'
