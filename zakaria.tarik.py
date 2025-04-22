import mysql.connector
from datetime import datetime, timedelta
import vonage

# --- Configurations ---

# Vonage API credentials (remplace par les tiens)
vonage_api_key = 'b8b31a19'
vonage_api_secret = 'BU8PUSKtdt3i66JC'
vonage_from = 'CoachSport'  # Le nom ou numéro expéditeur

# DB configuration 
db_config = {
    'host': 'infoemb.inraci.be',
    'user': 'ZTarik',
    'password': 'vc2zsF93ViBzztVO',
    'database': 'ZTarik'
}

# --- Envoi du SMS ---
def envoyer_sms(numero, message):
    client = vonage.Client(key=vonage_api_key, secret=vonage_api_secret)
    sms = vonage.Sms(client)

    response = sms.send_message({
        "from": vonage_from,
        "to": numero,
        "text": message,
    })

    if response["messages"][0]["status"] == "0":
        print(f"SMS envoyé à {numero}")
    else:
        print(f"Erreur SMS : {response['messages'][0]['error-text']}")

# --- Connexion et récupération des séances ---
def main():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        maintenant = datetime.now()
        dans_24h = maintenant + timedelta(hours=24)

        query = """
            SELECT * FROM seances
            WHERE date_heure_seance BETWEEN %s AND %s
        """
        cursor.execute(query, (maintenant, dans_24h))
        seances = cursor.fetchall()

        for seance in seances:
            message = (f"Bonjour {seance['prenom_client']} {seance['nom_client']}, "
                       f"vous avez une séance avec {seance['nom_entraineur']} le "
                       f"{seance['date_heure_seance'].strftime('%d/%m/%Y à %H:%M')}.")
            envoyer_sms(seance['telephone_client'], message)

    except mysql.connector.Error as err:
        print(f"Erreur de connexion à la BDD : {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    main()
