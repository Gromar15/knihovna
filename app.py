# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from models import db, Book, Member, Loan

app = Flask(__name__)
app.config["SECRET_KEY"] = "knihovna-tajny-klic-2024"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///knihovna.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def _init_demo_data():
    if Book.query.count() == 0:
        books = [
            Book(nazev="Maly princ", autor="Antoine de Saint-Exupery", isbn="978-80-00-01234-5"),
            Book(nazev="Babicka", autor="Bozena Nemcova", isbn="978-80-00-02345-6"),
            Book(nazev="Krakatit", autor="Karel Capek", isbn="978-80-00-03456-7"),
            Book(nazev="Osudy Svejka", autor="Jaroslav Hasek", isbn="978-80-00-04567-8"),
        ]
        members = [
            Member(jmeno="Jana", prijmeni="Novakova", email="jana.novakova@email.cz"),
            Member(jmeno="Petr", prijmeni="Svoboda", email="petr.svoboda@email.cz"),
        ]
        db.session.add_all(books + members)
        db.session.commit()


@app.route("/")
def index():
    knihy = Book.query.order_by(Book.nazev).all()
    return render_template("index.html", knihy=knihy)


@app.route("/clenove")
def clenove():
    clenove_list = Member.query.order_by(Member.prijmeni).all()
    return render_template("clenove.html", clenove=clenove_list)


@app.route("/clenove/pridat", methods=["GET", "POST"])
def pridat_clena():
    if request.method == "POST":
        jmeno = request.form.get("jmeno", "").strip()
        prijmeni = request.form.get("prijmeni", "").strip()
        email = request.form.get("email", "").strip()
        if not jmeno or not prijmeni or not email:
            flash("Vyplnte prosim vsechna pole.", "danger")
            return redirect(url_for("pridat_clena"))
        if Member.query.filter_by(email=email).first():
            flash("Clen s timto e-mailem jiz existuje.", "warning")
            return redirect(url_for("pridat_clena"))
        clen = Member(jmeno=jmeno, prijmeni=prijmeni, email=email)
        db.session.add(clen)
        db.session.commit()
        flash("Clen " + clen.plne_jmeno + " byl uspesne pridan.", "success")
        return redirect(url_for("clenove"))
    return render_template("pridat_clena.html")


@app.route("/pujcka/nova", methods=["GET", "POST"])
def nova_pujcka():
    dostupne_knihy = Book.query.filter_by(stav="dostupna").order_by(Book.nazev).all()
    vsichni_clenove = Member.query.order_by(Member.prijmeni).all()
    if request.method == "POST":
        book_id = request.form.get("book_id", type=int)
        member_id = request.form.get("member_id", type=int)
        dny = request.form.get("dny", 14, type=int)
        kniha = Book.query.get(book_id)
        clen = Member.query.get(member_id)
        if not kniha or not clen:
            flash("Neplatna kniha nebo clen.", "danger")
            return redirect(url_for("nova_pujcka"))
        if not kniha.je_dostupna:
            flash("Kniha " + kniha.nazev + " neni momentalne dostupna.", "warning")
            return redirect(url_for("nova_pujcka"))
        pujcka = Loan(
            book_id=kniha.id,
            member_id=clen.id,
            datum_pujceni=datetime.utcnow(),
            termin_vraceni=datetime.utcnow() + timedelta(days=dny),
        )
        kniha.stav = "pujcena"
        db.session.add(pujcka)
        db.session.commit()
        flash("Kniha " + kniha.nazev + " byla pujcena clenu " + clen.plne_jmeno + ".", "success")
        return redirect(url_for("index"))
    return render_template("nova_pujcka.html", dostupne_knihy=dostupne_knihy, vsichni_clenove=vsichni_clenove)


@app.route("/pujcka/<int:loan_id>/vratit", methods=["POST"])
def vratit_knihu(loan_id):
    pujcka = Loan.query.get_or_404(loan_id)
    if not pujcka.je_aktivni:
        flash("Tato vypujcka jiz byla vracena.", "warning")
        return redirect(url_for("index"))
    pujcka.datum_skutecneho_vraceni = datetime.utcnow()
    pujcka.kniha.stav = "dostupna"
    db.session.commit()
    flash("Kniha " + pujcka.kniha.nazev + " byla uspesne vracena.", "success")
    return redirect(url_for("index"))


@app.route("/pujcky")
def pujcky():
    aktivni = Loan.query.filter_by(datum_skutecneho_vraceni=None).order_by(Loan.termin_vraceni).all()
    vracene = (
        Loan.query.filter(Loan.datum_skutecneho_vraceni.isnot(None))
        .order_by(Loan.datum_skutecneho_vraceni.desc())
        .limit(20)
        .all()
    )
    return render_template("pujcky.html", aktivni=aktivni, vracene=vracene)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        _init_demo_data()
    app.run(debug=True)