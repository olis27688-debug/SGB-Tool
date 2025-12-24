import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

def lade_daten():
    alle_auftraege = []
    with open("sgb_production_data.csv", "r", encoding="utf-8") as datei:
        for zeile in datei:
            # 1. Müll am Ende wegputzen
            saubere_zeile = zeile.strip()
            # 2. Am Komma hacken
            daten_liste = saubere_zeile.split(",")
            alle_auftraege.append(daten_liste)
    return alle_auftraege

def lade_bild(name):
    name = name.strip()
    
    pfad = "bilder/" + name + ".png"
    
    # Debugging Print
    print(f"---> Suche Bild: '{pfad}'")
    
    if os.path.exists(pfad):
        # Bild laden und skalieren
        original = Image.open(pfad)
        resized = original.resize((600, 200))
        bild = ImageTk.PhotoImage(resized)
        return bild
    else: 
        return None

def update_gui(event):
    auswahl = dropdown.get()
    
    for zeile in alle_daten:
        # Index 0 ist die Auftragsnummer
        if zeile[0] == auswahl:
            # Daten extrahieren
            kunde = zeile[5]
            leistung = zeile[2]
            schaltgruppe = zeile[4]

            infos = f"Kunde: {kunde}\nLeistung: {leistung}\nSchaltgruppe: {schaltgruppe}"
            
            # Text auf Label anwenden
            info_label.config(text=infos, font=("Arial", 12))
            
            # Bild laden
            img = lade_bild(schaltgruppe)
            
            # Bild auf Label anwenden
            if img:
                bild_label.config(image=img, text="")
                bild_label.image = img # Garbage Collector Schutz
            else:
                bild_label.config(image="", text="Kein Bild gefunden") 
            
            break
            
# --- HAUPTPROGRAMM ---

# 1. Daten laden

alle_daten = lade_daten()

# Nur Seriennummern extrahieren
sn_only = []
for zeile in alle_daten:
    sn_only.append(zeile[0])

    
# 2. GUI starten
app = tk.Tk()
app.title("SGB-Tool")
app.geometry("600x500")

# Dropdown
tk.Label(app, text="Bitte Auftrag wählen:", font=("Arial", 10, "bold")).pack(pady=10)
dropdown = ttk.Combobox(app, values=sn_only[1:]) # [1:] schneidet 'Auftragsnummer' weg
dropdown.pack()
dropdown.set("Auftrag wählen")
dropdown.bind("<<ComboboxSelected>>", update_gui)

# Labels
info_label = tk.Label(app)
info_label.pack(pady=10)

bild_label = tk.Label(app)
bild_label.pack(pady=10)

app.mainloop()