from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from fpdf import FPDF
import os

Base = declarative_base()

# ---------------------
# Modèles de données
# ---------------------
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    email = Column(String)
    abonnements = relationship("Abonnement", back_populates="user")
    factures = relationship("Facture", back_populates="user")


class Abonnement(Base):
    __tablename__ = 'abonnements'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date_debut = Column(Date)
    date_fin = Column(Date)
    prix = Column(Float)
    statut = Column(String)
    user = relationship("User", back_populates="abonnements")
    facture = relationship("Facture", uselist=False, back_populates="abonnement")


class Facture(Base):
    __tablename__ = 'factures'
    id = Column(Integer, primary_key=True)
    numero_facture = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    abonnement_id = Column(Integer, ForeignKey('abonnements.id'))
    date_émission = Column(DateTime, default=datetime.utcnow)
    montant = Column(Float)
    statut = Column(String)
    user = relationship("User", back_populates="factures")
    abonnement = relationship("Abonnement", back_populates="facture")

# ---------------------
# Initialisation de la base
# ---------------------
engine = create_engine('sqlite:///facturation.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# ---------------------
# Fonctions principales
# ---------------------
def creer_utilisateur(nom, email):
    utilisateur = User(nom=nom, email=email)
    session.add(utilisateur)
    session.commit()
    return utilisateur

def souscrire_abonnement(user, duree_mois=1, prix=29.99):
    aujourd_hui = datetime.today().date()
    fin = aujourd_hui + timedelta(days=30*duree_mois)
    abonnement = Abonnement(user_id=user.id, date_debut=aujourd_hui, date_fin=fin, prix=prix, statut="actif")
    session.add(abonnement)
    session.commit()
    return abonnement

def creer_facture(user, abonnement):
    numero = f"FACT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    facture = Facture(
        numero_facture=numero,
        user_id=user.id,
        abonnement_id=abonnement.id,
        montant=abonnement.prix,
        statut="payée"
    )
    session.add(facture)
    session.commit()
    return facture

def generer_pdf_facture(facture):
    user = facture.user
    abonnement = facture.abonnement

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="FACTURE", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Numéro de facture : {facture.numero_facture}", ln=True)
    pdf.cell(200, 10, txt=f"Date d’émission : {facture.date_émission.strftime('%Y-%m-%d')}", ln=True)
    pdf.cell(200, 10, txt=f"Client : {user.nom} ({user.email})", ln=True)
    pdf.cell(200, 10, txt=f"Période : {abonnement.date_debut} → {abonnement.date_fin}", ln=True)
    pdf.cell(200, 10, txt=f"Montant : {facture.montant:.2f} €", ln=True)
    pdf.cell(200, 10, txt=f"Statut : {facture.statut}", ln=True)

    dossier = "factures"
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, f"{facture.numero_facture}.pdf")
    pdf.output(chemin)

    print(f"Facture PDF générée : {chemin}")
    return chemin

# ---------------------
# Simulation d’utilisation
# ---------------------
if __name__ == "__main__":
    nom = "Jean Dupont"
    email = "jean.dupont@example.com"

    user = creer_utilisateur(nom, email)
    abo = souscrire_abonnement(user, duree_mois=1, prix=29.99)
    facture = creer_facture(user, abo)
    generer_pdf_facture(facture)
