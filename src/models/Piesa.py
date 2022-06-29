from src import db
from sqlalchemy.orm import relationship


class Piesa(db.Model):
    __tablename__ = "piesas"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    precios = relationship("Precio", back_populates='piesas')
    pinturageneralpiesas = relationship("Pinturageneralpiesa", back_populates='piesas')

    def __init__(self, name) -> None:
        self.name = name
    def __repr__(self) -> str:
        return  self.name

class Precio(db.Model):
    __tablename__ = "precios"
    id = db.Column(db.Integer, primary_key=True)
    precio = db.Column(db.Integer, nullable=False)
    
    piesa_id = db.Column(db.Integer, db.ForeignKey("piesas.id"), nullable=False)
    piesas = relationship("Piesa", back_populates="precios")


    def __init__(self, precio, piesa_id) -> None:
        self.precio = precio
        self.piesa_id = piesa_id
    def __repr__(self) -> str:
        return self.precio