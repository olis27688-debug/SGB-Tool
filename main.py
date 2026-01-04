import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import SGB_library as sgb
import os

# --- GLOBALE VARIABLEN ---
letzter_datei_zeitstempel = 0
aktueller_datensatz = None  # WICHTIG: Hier merken wir uns, was gerade angezeigt wird

# --- GUI LOGIK (ANZEIGE) ---

def zeige_datensatz(zeile):
    """
    Zentrale Funktion: Aktualisiert Text und Bild in der GUI.
    Kann vom Dropdown ODER vom MATLAB-Import aufgerufen werden.
    """
    global aktueller_datensatz
    aktueller_datensatz = zeile # Merken für später (PDF Button)

    # Daten auspacken [Auftrag, Typ, Leistung, Spannung, Gruppe, Kunde]
    try:
        # Sicherstellen, dass genug Daten da sind
        if len(zeile) < 6:
            print("Fehler: Datensatz unvollständig")
            return

        infos = f"Kunde: {zeile[5]}\nTyp: {zeile[1]}\nLeistung: {zeile[2]}\nSpannung: {zeile[3]}\nSchaltgruppe: {zeile[4]}"
        
        # Text Update (ohne explizite Farbe, damit es Systemstandard bleibt)
        info_label.config(text=infos)
        
        # Bild laden
        img = sgb.lade_bild(zeile[4])
        if img:
            bild_label.config(image=img, text="")
            bild_label.image = img # Wichtig: Referenz halten!
        else:
            bild_label.config(image="", text="Kein Bild gefunden")
            
    except IndexError:
        print("Fehler beim Anzeigen der Daten")

# --- EVENTS ---

def update_gui(event):
    """Wird ausgeführt, wenn man das Dropdown benutzt"""
    auswahl = dropdown.get()
    
    # Suche in der geladenen CSV-Liste
    for zeile in alle_daten:
        if zeile[0] == auswahl:
            zeige_datensatz(zeile)
            break

def lade_daten_aus_matlab():
    """Wird vom Watchdog aufgerufen"""
    daten = sgb.lade_matlab_export()
    
    if daten:
        # WICHTIG: Wir übergeben die Daten DIREKT an die Anzeige
        # Wir suchen NICHT in der alten Liste (alle_daten)
        zeige_datensatz(daten)
        
        # Dropdown Text ändern
        dropdown.set(f"MATLAB: {daten[0]}")
    else:
        messagebox.showerror("Fehler", "Konnte MATLAB-Datei nicht lesen.")

def button_pdf_klick():
    # Wir nutzen die globale Variable, egal woher die Daten kamen
    if aktueller_datensatz:
        try:
            dateiname = sgb.generiere_pdf(aktueller_datensatz)
            messagebox.showinfo("Erfolg", f"PDF erstellt:\n{dateiname}")
        except Exception as e:
            messagebox.showerror("Fehler", f"PDF Fehler:\n{e}")
    else:
        messagebox.showwarning("Achtung", "Keine Daten ausgewählt!")

# --- WATCHDOG (HINTERGRUND) ---

def start_watchdog():
    global letzter_datei_zeitstempel
    skript_pfad = os.path.dirname(os.path.abspath(__file__))
    datei_pfad = os.path.join(skript_pfad, "matlab_export.csv")
    
    if os.path.exists(datei_pfad):
        aktueller_stand = os.path.getmtime(datei_pfad)
        if letzter_datei_zeitstempel > 0 and aktueller_stand > letzter_datei_zeitstempel:
            
            # TRICK: Fenster aggressiv nach vorne holen
            app.deiconify() # Wiederherstellen (falls minimiert)
            app.attributes('-topmost', True) # Zwingend nach ganz oben
            app.lift()      # Über andere Fenster heben
            app.focus_force() # Den Fokus klauen (damit Enter direkt "Ja" drückt)
            
            # parent=app ist wichtig, damit die Box AUF dem Fenster klebt
            antwort = messagebox.askyesno(
                "Neue Berechnung", 
                "MATLAB hat neue Daten bereitgestellt!\nMöchten Sie diese jetzt importieren?",
                parent=app 
            )
            
            # WICHTIG: Vordergrund-Zwang wieder aufheben
            app.attributes('-topmost', False)
            
            if antwort:
                lade_daten_aus_matlab()
        
        letzter_datei_zeitstempel = aktueller_stand
        
    app.after(2000, start_watchdog)

# --- HAUPTPROGRAMM ---

# 1. Daten laden
alle_daten = sgb.lade_daten()
# Slicing [1:], um die Kopfzeile "Auftragsnummer" im Dropdown auszublenden
sn_only = [z[0] for z in alle_daten if len(z) > 0] 

# 2. GUI starten
app = tk.Tk()
app.title("SGB Schaltschild Manager")
app.geometry("600x600")

# Header
# SGB Logo
# Logo laden (Wir nutzen die Funktion aus der Library)
logo_pfad = sgb.hole_bild_pfad("logo") # Sucht nach logo.png im bilder Ordner
if logo_pfad:
    try:
        pil_image = Image.open(logo_pfad)
        # Skalieren für die GUI (z.B. max 200px breit)
        pil_image.thumbnail((200, 80)) 
        tk_logo = ImageTk.PhotoImage(pil_image)
        
        logo_label = tk.Label(app, image=tk_logo)
        logo_label.image = tk_logo # Referenz halten!
        logo_label.pack(pady=(10, 0)) # Etwas Abstand oben
    except Exception as e:
        print(f"Konnte Logo nicht laden: {e}")

# Dropdown (ohne Header)
dropdown_werte = sn_only[1:] if len(sn_only) > 0 else []
dropdown = ttk.Combobox(app, values=dropdown_werte, width=30)
dropdown.pack(pady=5)
dropdown.set("Auftrag wählen")
dropdown.bind("<<ComboboxSelected>>", update_gui)

# Info Label
info_label = tk.Label(app, text="---", font=("Arial", 14), justify="left", width=100, anchor="w")
info_label.pack(pady=10, padx=150)

# Bild Label
bild_label = tk.Label(app)
bild_label.pack(pady=5)

# PDF Button
pdf_btn = tk.Button(app, text="📄 PDF Schaltschild generieren", command=button_pdf_klick, bg="lightblue", height=2)
pdf_btn.pack(pady=20, fill="x", padx=50)

tk.Label(app, text="Copyright Oliver Siegmund").pack(pady=20)

# --- WATCHDOG STARTEN ---
pfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), "matlab_export.csv")
if os.path.exists(pfad):
    letzter_datei_zeitstempel = os.path.getmtime(pfad)

start_watchdog()

app.mainloop()