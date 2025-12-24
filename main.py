import tkinter as tk
from tkinter import ttk, messagebox
import SGB_library as sgb

# --- GUI LOGIK ---
def update_gui(event):
    auswahl = dropdown.get()
    
    for zeile in alle_daten:
        if zeile[0] == auswahl:
            # 1. Text Update
            infos = f"Kunde: {zeile[5]}\nLeistung: {zeile[2]}\nSchaltgruppe: {zeile[4]}"
            info_label.config(text=infos)
            
            # 2. Bild laden (über die Library!) Vorschau
            img = sgb.lade_bild(zeile[4])
            
            if img:
                bild_label.config(image=img, text="")
                bild_label.image = img 
            else:
                bild_label.config(image="", text="Kein Bild gefunden")
            break

def button_pdf_klick():
    auswahl = dropdown.get()
    if auswahl == "Auftrag wählen" or auswahl == "":
        return messagebox.showwarning("","Auftrag zuerst auswählen") 
    
    # Daten suchen //BUGFIX: PDF wird generiert bei "Auftragsnummer"(leeres PDF) --> Mit Slicing [1:] behoben
    gewaehlte_daten = []
    for zeile in alle_daten[1:]:
        if zeile[0] == auswahl:
            gewaehlte_daten = zeile
            break
    
    # PDF Generieren (über die Library!)
    if gewaehlte_daten:
        dateiname = sgb.generiere_pdf(gewaehlte_daten)
        messagebox.showinfo("Erfolg", f"PDF erstellt:\n{dateiname}")
    else:
        messagebox.showwarning("","Auftrag zuerst auswählen") 

# --- HAUPTPROGRAMM ---
app = tk.Tk()
app.title("SGB Schaltschild Manager")
app.geometry("600x600")

# Daten einmalig laden
alle_daten = sgb.lade_daten()
sn_only = [z[0] for z in alle_daten]

# UI Elemente
tk.Label(app, text="Produktionsauftrag wählen:", font=("Arial", 14, "bold")).pack(pady=10)

dropdown = ttk.Combobox(app, values=sn_only[:], width=30)
dropdown.pack()
dropdown.set("Auftrag wählen")
dropdown.bind("<<ComboboxSelected>>", update_gui)

info_label = tk.Label(app, text="---", font=("Arial", 11))
info_label.pack(pady=10)

bild_label = tk.Label(app, text="Vorschau")
bild_label.pack(pady=5)

# PDF Button
pdf_btn = tk.Button(app, text="📄 PDF Schaltschild generieren", command=button_pdf_klick, bg="lightblue", height=2)
pdf_btn.pack(pady=20, fill="x", padx=50)

app.mainloop()