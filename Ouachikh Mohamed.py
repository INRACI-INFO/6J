import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.font as tkFont

''' fenetre '''
gymmaster = tk.Tk()
gymmaster.title("GymMaster Dashboard")
gymmaster.geometry("1152x648")
gymmaster.configure(bg="#ffffff")

''' style pour les widgets TTK '''
style = ttk.Style()
style.theme_use('clam')
style.configure('Sidebar.TFrame', background='#ffffff')
style.configure('Main.TFrame', background='#f5f5f5')
style.configure('CardFrame.TLabelframe', background='#ffffff', borderwidth=1, relief='solid')
style.configure('CardFrame.TLabelframe.Label', background='#ffffff', font=('Arial', 10, 'bold'))

''' sidebar et navigation panel '''
cadre_navigation = tk.Frame(gymmaster, bg="#ffffff", width=180)
cadre_navigation.pack(side="left", fill="y")
cadre_navigation.pack_propagate(False)

''' titre navigation '''
titre_navigation = tk.Label(cadre_navigation, text="Navigation", font=('Arial', 12, 'bold'), 
                     bg="#ffffff", fg="#666666")
titre_navigation.pack(pady=(10, 5), padx=10, anchor="w")

''' bouton de navigation '''
btn_navigation = [
    ("Dashboard", True), 
    ("Tasks", False),
    ("Find Member", False),
    ("Last Visitors", False),
    ("Point of Sale", False),
    ("Communication", False),
    ("Billing", False),
    ("Reports", False),
    ("Settings", False),
    ("Help", False)
]

for bouton_text, selection in btn_navigation:
    frame = tk.Frame(cadre_navigation, bg="#ffffff")
    frame.pack(fill="x", padx=5, pady=1)
    
    if selection:
        ''' bouton selection '''
        btn_selection = tk.Button(frame, text=bouton_text, anchor="w", bg="#e6f3ff", 
                       fg="#3366cc", relief="flat", font=("Arial", 10),
                       borderwidth=0, padx=15, pady=5)
        btn_selection.pack(fill="x")
    else:
        ''' bouton normal '''
        btn_normal = tk.Button(frame, text=bouton_text, anchor="w", bg="#ffffff", 
                       fg="#333333", relief="flat", font=("Arial", 10),
                       borderwidth=0, padx=15, pady=5)
        btn_normal.pack(fill="x")
        ''' effet de survol '''
        btn_normal.bind("<Enter>", lambda e: e.widget.config(bg="#f0f0f0"))
        btn_normal.bind("<Leave>", lambda e: e.widget.config(bg="#ffffff"))

''' bouton quitte '''
frame_quitte = tk.Frame(cadre_navigation, bg="#ffffff")
frame_quitte.pack(side="bottom", fill="x", padx=5, pady=10)
btn_quitte = tk.Button(frame_quitte, text="Quit", bg="#4d79ff", fg="white", 
                    relief="flat", font=("Arial", 10, "bold"), 
                    command=gymmaster.quit, pady=8)
btn_quitte.pack(fill="x")

''' zone principal '''
cadre_principale = tk.Frame(gymmaster, bg="#f5f5f5")
cadre_principale.pack(side="left", fill="both", expand=True)

''' en tete avec logo et titre '''
frame_en_tete = tk.Frame(cadre_principale, bg="#f5f5f5", height=150)
frame_en_tete.pack(fill="x", padx=20, pady=20)
frame_en_tete.pack_propagate(False)

''' logo et titre '''
logo_frame = tk.Frame(frame_en_tete, bg="#f5f5f5")
logo_frame.pack(anchor="center")

''' titre '''
titre_gymmaster = tk.Label(logo_frame, text="GYMMASTER", 
                      font=("Arial", 36, "bold"), 
                      fg="#333333", bg="#f5f5f5")
titre_gymmaster.pack()

''' sous titres '''
label_sous_titre = tk.Label(logo_frame, text="Membership Management Software", 
                         font=("Arial", 16), 
                         fg="#666666", bg="#f5f5f5")
label_sous_titre.pack()

''' configuration des sections avec icones et couleurs '''
sections_data = [
    {
        "title": "Member",
        "desc": "Add and manage members.",
        "button_text": "Add",
        "stats": "49 Members",
        "progress": "100% Retention Rate",
        "icon": "👤",
        "row": 0, "col": 0
    },
    {
        "title": "Booking",
        "desc": "View and manage bookings\nfor trainers and classes.",
        "button_text": "Booking",
        "stats": "No Recent Classes",
        "progress": "11 Members Booked",
        "icon": "📅",
        "row": 0, "col": 1
    },
    {
        "title": "Prospect",
        "desc": "View and manage sales\nprospects.",
        "button_text": "Prospects",
        "stats": "No conversions",
        "progress": "0% Prospects Contacted",
        "icon": "👥",
        "row": 0, "col": 2
    },
    {
        "title": "Tasks",
        "desc": "Action items on your to do list.",
        "button_text": "Last Visitors",
        "stats": "No recent tasks",
        "progress": None,
        "icon": "📋",
        "row": 1, "col": 0
    },
    {
        "title": "Point of Sale",
        "desc": "Sell a product over the\ncounter.",
        "button_text": "Make a Sale",
        "stats": "No recent stocktake",
        "progress": None,
        "icon": "💳",
        "row": 1, "col": 1
    },
    {
        "title": "Reports and Billing",
        "desc": "Financial reports and billing information",
        "button_text": "Billing",
        "stats": "84% Members Paid Up",
        "progress": None,
        "icon": "📊",
        "row": 1, "col": 2
    }
]

''' frame pour les sections '''
sections_frame = tk.Frame(cadre_principale, bg="#f5f5f5")
sections_frame.pack(expand=True, fill="both", padx=20, pady=10)

''' configurer les colonnes et lignes pour qu'elles s'etendent '''
for i in range(3):
    sections_frame.grid_columnconfigure(i, weight=1, uniform="col")
for i in range(2):
    sections_frame.grid_rowconfigure(i, weight=1, uniform="row")

''' creer les sections '''
for section in sections_data:
    ''' frame principale de la section '''
    frame = tk.Frame(sections_frame, bg="#ffffff", relief="solid", borderwidth=1)
    frame.grid(row=section["row"], column=section["col"], 
               padx=8, pady=8, sticky="nsew")
    frame.grid_propagate(False)
    frame.grid_columnconfigure(0, weight=1)
    
    ''' en tete avec icone et titre '''
    en_tete = tk.Frame(frame, bg="#ffffff", height=40)
    en_tete.pack(fill="x", padx=15, pady=(10, 5))
    en_tete.pack_propagate(False)
    
    ''' titre et icon  '''
    titre_frame = tk.Frame(en_tete, bg="#ffffff")
    titre_frame.pack(side="left", fill="both", expand=True)
    
    label_icon = tk.Label(titre_frame, text=section["icon"], 
                         font=("Arial", 16), bg="#ffffff")
    label_icon.pack(side="left", padx=(0, 5))
    
    label_titre = tk.Label(titre_frame, text=section["title"], 
                          font=("Arial", 11, "bold"), 
                          bg="#ffffff", fg="#333333")
    label_titre.pack(side="left", anchor="w")
    
    ''' description '''
    label_description = tk.Label(frame, text=section["desc"], 
                         font=("Arial", 9), 
                         bg="#ffffff", fg="#666666", 
                         justify="left")
    label_description.pack(padx=15, pady=(0, 10), anchor="w")
    
    ''' bouton '''
    btn_frame = tk.Frame(frame, bg="#ffffff")
    btn_frame.pack(padx=15, pady=5)
    
    if section["title"] == "Tasks":
        ''' boutons a coter pour Tasks '''
        btn_task = tk.Button(btn_frame, text="Tasks", 
                        font=("Arial", 9), bg="#e6f3ff", fg="#3366cc",
                        relief="solid", borderwidth=1, padx=20, pady=5)
        btn_task.pack(side="left", padx=(0, 5))
        
        btn_visitors = tk.Button(btn_frame, text="Last Visitors", 
                        font=("Arial", 9), bg="#e6f3ff", fg="#3366cc",
                        relief="solid", borderwidth=1, padx=20, pady=5)
        btn_visitors.pack(side="left")
    else:
        ''' bouton unique pour les autres sections '''
        btn = tk.Button(btn_frame, text=section["button_text"], 
                       font=("Arial", 9), bg="#e6f3ff", fg="#3366cc",
                       relief="solid", borderwidth=1, padx=40, pady=5)
        btn.pack()
    
    ''' statistics '''
    label_stats = tk.Label(frame, text=section["stats"], 
                          font=("Arial", 9), 
                          bg="#ffffff", fg="#666666")
    label_stats.pack(padx=15, pady=5)
    
    ''' progress bar si besoin '''
    if section["progress"]:
        frame_progres = tk.Frame(frame, bg="#ffffff")
        frame_progres.pack(padx=15, pady=5, fill="x")
        
        ''' extraire la valeur pour la progress bar '''
        if "%" in section["progress"]:
            ''' pourcentage '''
            value_str = section["progress"].split("%")[0]
            try:
                value = float(value_str.split()[-1])
            except:
                value = 0
            
            ''' barre de progression '''
            progress = ttk.Progressbar(frame_progres, length=200, value=value, 
                                     maximum=100, mode='determinate')
            progress.pack(pady=2)
            
            ''' label avec pourcentage '''
            label_progres = tk.Label(frame_progres, text=section["progress"], 
                                    font=("Arial", 9), 
                                    bg="#ffffff", fg="#666666")
            label_progres.pack()
        else:
            ''' valeurs simples '''
            label_progres = tk.Label(frame_progres, text=section["progress"], 
                                    font=("Arial", 9), 
                                    bg="#ffffff", fg="#666666")
            label_progres.pack()

''' ajout d'un separateur vertical entre la navigation et le contenu principal '''
separateur = tk.Frame(gymmaster, bg="#e0e0e0", width=1)
separateur.pack(side="left", fill="y")

gymmaster.mainloop()