from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    nazev = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    stav = db.Column(db.String(20), nullable=False, default="dostupná")

    pujcky = db.relationship("Loan", back_populates="kniha", lazy="dynamic")

    @property
    def je_dostupna(self):
        return self.stav == "dostupná"


class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    jmeno = db.Column(db.String(80), nullable=False)
    prijmeni = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

    pujcky = db.relationship("Loan", back_populates="clen", lazy="dynamic")

    @property
    def plne_jmeno(self):
        return f"{self.jmeno} {self.prijmeni}"


class Loan(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    datum_pujceni = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    termin_vraceni = db.Column(db.DateTime, nullable=False)
    datum_skutecneho_vraceni = db.Column(db.DateTime, nullable=True)

    kniha = db.relationship("Book", back_populates="pujcky")
    clen = db.relationship("Member", back_populates="pujcky")

    @property
    def je_aktivni(self):
        return self.datum_skutecneho_vraceni is None

    @property
    def je_po_terminu(self):
        return self.je_aktivni and datetime.utcnow() > self.termin_vraceni
