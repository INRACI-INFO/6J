#zakaria
#tarik
#bgs
#arrête de regader mon code 
client = vonage.Client(key="", secret="")
    sms = vonage.Sms(client)

    responseData = sms.send_message(
        {
            "from": "client",
            "to": DATA_NUMERODETEL,
            "text": f"vous avez rendevous {nombre_aleatoire}. uniquement valide pour depot.",
        }
    )
    
    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")

        db = firestore.client()
        user_data = {
            'nom': DATA_NOM,
            'prenom': DATA_PRENOM,
            'code postal': DATA_POSTAL,
            'numero de telephone' : DATA_NUMERODETEL,
            'code de verification': nombre_aleatoire,
        }
        db.collection('utilisateur').add(user_data)
        print("Données enregistrées avec succès !")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
