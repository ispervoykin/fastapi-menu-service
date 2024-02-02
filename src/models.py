from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from database import Base

class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    submenus_count = Column(Integer, nullable=False, default=0)
    dishes_count = Column(Integer, nullable=False, default=0)

    submenus = relationship('Submenu', backref='menu')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def stringify(self):
        self = self.as_dict()
        for keys in self:
            self[keys] = str(self[keys])
        return self
        

class Submenu(Base):
    __tablename__ = "submenu"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(Integer, ForeignKey("menu.id", ondelete="CASCADE"), nullable=False)
    dishes_count = Column(Integer, nullable=False, default=0)

    dishes = relationship('Dish', backref='submenu')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def stringify(self):
        self = self.as_dict()
        for keys in self:
            self[keys] = str(self[keys])
        return self


class Dish(Base):
    __tablename__ = "dish"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Numeric(precision=12, scale=2), nullable=False)
    submenu_id = Column(Integer, ForeignKey("submenu.id", ondelete="CASCADE"), nullable=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def stringify(self):
        self = self.as_dict()
        for keys in self:
            self[keys] = str(self[keys])
        return self