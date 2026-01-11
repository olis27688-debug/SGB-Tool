"""


SGB Schaltschild Manager - Frontend
Hauptanwendung zur Steuerung des Prozesses, Anzeige der GUI
und Überwachung von externen MATLAB-Datenquellen.
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import SGB_library as sgb

# -----------------------------------------------------------------------------
# GLOBALE VARIABLEN
# -----------------------------------------------------------------------------
letzter_datei_zeitstempel = 0
aktueller_datensatz = None  # Speichert den aktuell angezeigten Datensatz


# -----------------------------------------------------------------------------
# ANZEIGE-LOGIK
# -----------------------------------------------------------------------------
def zeige_datensatz(zeile):
    """
    Zentrale Funktion: Aktualisiert Text und Bild in der GUI.
    Kann vom Dropdown ODER vom MATLAB-Import aufgerufen werden.
    """
    global aktueller_datensatz
    aktueller_datensatz = zeile  # Merken für später (PDF Button)

    try:
        # Sicherstellen, dass genug Daten vorhanden sind
        if len(zeile) < 6:
            print("Fehler: Datensatz unvollständig")
            return

        # Daten auspacken: [Auftrag, Typ, Leistung, Spannung, Gruppe, Kunde]
        infos = (
            f"Kunde: {zeile[5]}\n"
            f"Typ: {zeile[1]}\n"
            f"Leistung:  {zeile[2]}\n"
            f"Spannung:  {zeile[3]}\n"
            f"Schaltgruppe:  {zeile[4]}"
        )

        # Text Update
        info_label.config(text=infos)

        # Bild laden
        img = sgb.lade_bild(zeile[4])
        if img:
            bild_label.config(image=img, text="")
            bild_label.image = img  # Referenz halten (Wichtig für Garbage Collector)
        else:
            bild_label.config(image="", text="Kein Bild gefunden")

    except IndexError:
        print("Fehler beim Anzeigen der Daten")


# -----------------------------------------------------------------------------
# EVENT HANDLER
# -----------------------------------------------------------------------------
def update_gui(_event):
    """Callback für Dropdown-Auswahl."""
    auswahl = dropdown.get()

    for zeile in alle_daten:
        if zeile[0] == auswahl:
            zeige_datensatz(zeile)
            break

def lade_daten_aus_matlab():
    """Wird vom Watchdog aufgerufen, wenn neue Daten erkannt wurden."""
    daten = sgb.lade_matlab_export()

    if daten:
        # WICHTIG: Wir übergeben die Daten DIREKT an die Anzeige
        zeige_datensatz(daten)

        # Dropdown Text ändern, um Herkunft anzuzeigen
        dropdown.set(f"MATLAB: {daten[0]}")
    else:
        messagebox.showerror("Fehler", "Konnte MATLAB-Datei nicht lesen.")

def button_pdf_klick():
    """Callback für PDF-Button."""
    if aktueller_datensatz:
        try:
            dateiname = sgb.generiere_pdf(aktueller_datensatz)
            messagebox.showinfo("Erfolg", f"PDF erstellt:\n{dateiname}")
        except Exception as error:
            messagebox.showerror("Fehler", f"PDF Fehler:\n{error}")
    else:
        messagebox.showwarning("Achtung", "Keine Daten ausgewählt!")


# -----------------------------------------------------------------------------
# HINTERGRUND-DIENST (WATCHDOG)
# -----------------------------------------------------------------------------
def start_watchdog():
    """Prüft periodisch (Polling), ob sich die MATLAB-Datei geändert hat."""
    global letzter_datei_zeitstempel

    skript_pfad = os.path.dirname(os.path.abspath(__file__))
    datei_pfad = os.path.join(skript_pfad, "matlab_export.csv")

    if os.path.exists(datei_pfad):
        try:
            aktueller_stand = os.path.getmtime(datei_pfad)

            # Wenn Datei neuer ist als beim letzten Check
            if letzter_datei_zeitstempel > 0 and aktueller_stand > letzter_datei_zeitstempel:

                # Fenster aggressiv nach vorne holen
                app.deiconify()
                app.attributes('-topmost', True)
                app.lift()
                app.focus_force()

                # parent=app ist wichtig, damit die Box AUF dem Fenster klebt
                antwort = messagebox.askyesno(
                    "Neue Berechnung",
                    "MATLAB hat neue Daten bereitgestellt!\n"
                    "Möchten Sie diese jetzt importieren?",
                    parent=app
                )

                # Vordergrund-Zwang wieder aufheben
                app.attributes('-topmost', False)

                if antwort:
                    lade_daten_aus_matlab()

            letzter_datei_zeitstempel = aktueller_stand

        except OSError:
            pass  # Fehler beim Dateizugriff ignorieren

    # Die Funktion ruft sich selbst nach 2000ms wieder auf
    app.after(2000, start_watchdog)


# -----------------------------------------------------------------------------
# HAUPTPROGRAMM (MAIN)
# -----------------------------------------------------------------------------

# 1. Daten initial laden
alle_daten = sgb.lade_daten()
# Mittels List Comprehension: Neue Liste mit Seriennummern only
sn_only = [z[0] for z in alle_daten if len(z) > 0]

# 2. GUI Fenster erstellen
app = tk.Tk()
app.title("SGB Schaltschild Manager")
app.geometry("600x600")

# --- Header & Logo ---
logo_pfad = sgb.hole_bild_pfad("logo")  # Sucht nach logo.png im bilder Ordner
if logo_pfad:
    try:
        pil_image = Image.open(logo_pfad)
        # Skalieren für die GUI (z.B. max 200px breit)
        pil_image.thumbnail((200, 80))
        tk_logo = ImageTk.PhotoImage(pil_image)

        logo_label = tk.Label(app, image=tk_logo)
        logo_label.image = tk_logo  # Referenz halten!
        logo_label.pack(pady=(10, 0))  # Etwas Abstand oben
    except Exception as e:
        print(f"Konnte Logo nicht laden: {e}")
    
# --- Dropdown ---
# Header überspringen (slicing [1:])
dropdown_werte = sn_only[1:] if len(sn_only) > 0 else []
dropdown = ttk.Combobox(app, values=dropdown_werte, width=30)
dropdown.pack(pady=5)
dropdown.set("Auftrag wählen")
dropdown.bind("<<ComboboxSelected>>", update_gui)

# --- Info & Vorschau ---
info_label = tk.Label(
    app, text="---", font=("Arial", 14), justify="left", width=100, anchor="w"
)
info_label.pack(pady=10, padx=150)

bild_label = tk.Label(app, text="Vorschau")
bild_label.pack(pady=5)

# --- Aktions-Button ---
pdf_btn = tk.Button(
    app, text="📄 PDF Schaltschild generieren",
    command=button_pdf_klick, bg="lightblue", height=2
)
pdf_btn.pack(pady=20, fill="x", padx=50)

# --- Footer ---
tk.Label(app, text="Copyright Oliver Siegmund").pack(pady=20)

# 3. Watchdog Initialisierung
pfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), "matlab_export.csv")
if os.path.exists(pfad):
    letzter_datei_zeitstempel = os.path.getmtime(pfad)

start_watchdog()

# App starten
app.mainloop()