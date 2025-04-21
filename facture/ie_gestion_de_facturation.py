from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from fpdf import FPDF
import os
import uuid
import logging
import enum

logging.basicConfig(level=logging.INFO)
Base = declarative_base()

class StatutAbonnement(enum.Enum):
    actif = "actif"
    inactif = "inactif"

class StatutFacture(enum.Enum):
    payee = "payee"
    impayee = "impayee"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String)
    email = Column(String, unique=True)
    abonnements = relationship("Abonnement", back_populates="user")
    factures = relationship("Facture", back_populates="user")

class Abonnement(Base):
    __tablename__ = 'abonnements'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date_debut = Column(Date)
    date_fin = Column(Date)
    prix = Column(Float)
    statut = Column(Enum(StatutAbonnement))
    user = relationship("User", back_populates="abonnements")
    facture = relationship("Facture", uselist=False, back_populates="abonnement")

class Facture(Base):
    __tablename__ = 'factures'
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_facture = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    abonnement_id = Column(Integer, ForeignKey('abonnements.id'))
    date_émission = Column(DateTime, default=datetime.utcnow)
    montant = Column(Float)
    statut = Column(Enum(StatutFacture))
    user = relationship("User", back_populates="factures")
    abonnement = relationship("Abonnement", back_populates="facture")

engine = create_engine('sqlite:///facturation.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def creer_utilisateur(nom, email):
    existant = session.query(User).filter_by(email=email).first()
    if existant:
        return existant
    utilisateur = User(nom=nom, email=email)
    session.add(utilisateur)
    session.commit()
    return utilisateur

def souscrire_abonnement(user, duree_mois=1, prix=29.99):
    aujourd_hui = datetime.today().date()
    fin = aujourd_hui + timedelta(days=30 * duree_mois)
    abonnement = Abonnement(
        user_id=user.id,
        date_debut=aujourd_hui,
        date_fin=fin,
        prix=prix,
        statut=StatutAbonnement.actif
    )
    session.add(abonnement)
    session.commit()
    return abonnement

def creer_facture(user, abonnement):
    numero = f"FACT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
    facture = Facture(
        numero_facture=numero,
        user_id=user.id,
        abonnement_id=abonnement.id,
        montant=abonnement.prix,
        statut=StatutFacture.payee
    )
    session.add(facture)
    session.commit()
    return facture

def generer_pdf_facture(facture):
    user = facture.user
    abonnement = facture.abonnement

    pdf = FPDF()
    pdf.add_page()

    # Utilisation de la police par defaut compatible Latin-1
    pdf.set_font("Arial", size=12)

    # Informations de la facture
    pdf.set_title("Facture")
    pdf.set_author("Systeme de facturation")
    pdf.set_subject("Details de la facture")

    pdf.cell(200, 10, txt="FACTURE", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Numero de facture : {facture.numero_facture}", ln=True)
    pdf.cell(200, 10, txt=f"Date d'emission : {facture.date_émission.strftime('%Y-%m-%d')}", ln=True)
    pdf.cell(200, 10, txt=f"Client : {user.nom} ({user.email})", ln=True)
    pdf.cell(200, 10, txt=f"Periode : {abonnement.date_debut} - {abonnement.date_fin}", ln=True)
    pdf.cell(200, 10, txt=f"Montant : {facture.montant:.2f} EUR", ln=True)
    pdf.cell(200, 10, txt=f"Statut : {facture.statut.value}", ln=True)

    # Enregistrement du fichier
    dossier = "factures"
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, f"{facture.numero_facture}.pdf")
    pdf.output(chemin)

    logging.info(f"Facture PDF generee : {chemin}")
    return chemin


if __name__ == "__main__":
    nom = "Jean Dupont"
    email = "jean.dupont@example.com"
    user = creer_utilisateur(nom, email)
    abo = souscrire_abonnement(user, duree_mois=1, prix=29.99)
    facture = creer_facture(user, abo)
    generer_pdf_facture(facture)
