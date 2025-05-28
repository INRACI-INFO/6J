"""

Reporting : Ce code utilise les utilisateurs de la table "yassine_usr" de la base de donée "naitotest". Nous avons créer un nouvelle table s'appelant
"nass_jal_frequentation" reprenant les utilisateurs de "yassine_usr" (leurs ID) et nous avons simuler entre 5 et 30 entrées dans la salle de sport.

Le code ouvre une page tkinter où il y à 3 boutons ouvrant 3 graphiques différents : 
1. Entrées par utilisateurs 
2. Entrées par jours
3. Entrées par heures

* Le création de ce code à été grandement aidé par Chat GPT

code by Nassim Chouaf & Jalel El Amouri.
"""

import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


chart_canvas = None # vérifie s'il y  déjà un graphique affiché, le supprime si oui avant d'en afficher un autre

# création des graphiques
def create_all_charts(chart_type):
    try:
        conn = mysql.connector.connect(
            host='infoemb.inraci.be',
            user='NChouaf',
            password='eeZjB3TCvUnE1evW',
            database='naitotest'
        )
        cursor = conn.cursor()

        # 1. Nombre d'entrées par utilisateur
        cursor.execute("""
            SELECT y.prenom, COUNT(f.id)
            FROM nass_jal_frequentation f
            JOIN yassine_usr y ON f.user_id = y.id
            GROUP BY f.user_id
        """)
        users_data = cursor.fetchall()

        # 2. Nombre d'entrées par jour
        cursor.execute("""
            SELECT DATE(date_entree), COUNT(*) 
            FROM nass_jal_frequentation 
            GROUP BY DATE(date_entree)
            ORDER BY DATE(date_entree)
        """)
        day_data = cursor.fetchall()

        # 3. Répartition horaire des entrées
        cursor.execute("""
            SELECT HOUR(date_entree), COUNT(*) 
            FROM nass_jal_frequentation 
            GROUP BY HOUR(date_entree)
            ORDER BY HOUR(date_entree)
        """)
        hour_data = cursor.fetchall()

        cursor.close()
        conn.close()

        if chart_type == "user":
            noms = [row[0] for row in users_data]
            valeurs = [row[1] for row in users_data]
            ax = plt.figure(figsize=(6, 4)).add_subplot()
            ax.bar(noms, valeurs, color='skyblue')
            ax.set_title("Entrées par utilisateur")
            ax.set_ylabel("Entrées")

        elif chart_type == "day":
            dates = [row[0].strftime('%Y-%m-%d') for row in day_data]
            counts = [row[1] for row in day_data]
            ax = plt.figure(figsize=(6, 4)).add_subplot()
            ax.plot(dates, counts, marker='o')
            ax.set_title("Entrées par jour")
            ax.tick_params(axis='x', rotation=45)

        elif chart_type == "hour":
            heures = [str(row[0]) for row in hour_data]
            nombre = [row[1] for row in hour_data]
            ax = plt.figure(figsize=(6, 4)).add_subplot()
            ax.bar(heures, nombre, color='lightcoral')
            ax.set_title("Entrées par heure")
            ax.set_xlabel("Heure")
            ax.set_ylabel("Entrées")

        global chart_canvas
        if chart_canvas:
            chart_canvas.get_tk_widget().destroy()
        chart_canvas = FigureCanvasTkAgg(ax.figure, master=root)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'affichage des graphiques:\n{e}")

# tkinter
root = tk.Tk()
root.title("Reporting Utilisateurs")
root.geometry("900x500")

# Titre centré en haut
title_label = ttk.Label(root, text="Reporting par Nassim et Jalel pour GYMASTER", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

btn_frame = ttk.Frame(root, padding="10")
btn_frame.pack()

user_chart_btn = ttk.Button(btn_frame, text="Entrées par utilisateur", command=lambda: create_all_charts("user"))
user_chart_btn.pack(side=tk.LEFT, padx=5)

day_chart_btn = ttk.Button(btn_frame, text="Entrées par jour", command=lambda: create_all_charts("day"))
day_chart_btn.pack(side=tk.LEFT, padx=5)

hour_chart_btn = ttk.Button(btn_frame, text="Entrées par heure", command=lambda: create_all_charts("hour"))
hour_chart_btn.pack(side=tk.LEFT, padx=5)

root.mainloop()
