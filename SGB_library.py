import os
import csv
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4



def lade_matlab_export():
    skript_pfad = os.path.dirname(os.path.abspath(__file__))
    # Der Name muss exakt so sein wie im MATLAB-Skript
    matlab_pfad = os.path.join(skript_pfad, "matlab_export.csv")
    
    if not os.path.exists(matlab_pfad):
        return None # Datei noch nicht da (Ingenieur rechnet noch)
        
    try:
        with open(matlab_pfad, "r", encoding="utf-8") as datei:
            reader = csv.reader(datei)
            next(reader) # Header von Matlab überspringen
            zeile = next(reader) # Die erste Datenzeile holen
            return zeile
    except Exception as e:
        print(f"Fehler beim Matlab-Import: {e}")
        return None

def hole_bild_pfad(name):
    
    name = name.strip()
    
    skript_pfad = os.path.dirname(os.path.abspath(__file__))
    
    
    pfad_png = os.path.join(skript_pfad, "bilder", name + ".png")
    
    if os.path.exists(pfad_png):
        return pfad_png
    else:
        return None

def lade_daten():
    alle_auftraege = []
    with open("sgb_production_data.csv", "r", encoding="utf-8") as datei:
        for zeile in datei:
            # 1. bereinigen
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
        
def generiere_pdf(daten):
    # Daten zerlegen [Nr, Typ, MVA, kV, Gruppe, Kunde]
    auftrag = daten[0]
    kunde = daten[5]
    gruppe = daten[4]
    
    
    
    # 0. Ordner für PDFs erstellen 
    skript_pfad = os.path.dirname(os.path.abspath(__file__))
    pdf_ordner = os.path.join(skript_pfad, "pdf_druck")
    
    if not os.path.exists(pdf_ordner):
        os.makedirs(pdf_ordner)
        print(f"Ordner erstellt: {pdf_ordner}")
    
    dateiname = f"Schild_{auftrag}.pdf"
    voller_pfad = os.path.join(pdf_ordner, dateiname)
    
    # 1. Canvas (Blatt Papier) erstellen
    c = canvas.Canvas(voller_pfad, pagesize=A4)
    
    # 2. Rahmen und Titel
    c.setLineWidth(2)
    c.rect(50, 400, 500, 400) # Großer Rahmen
    
    c.setFont("Helvetica-Bold", 18)
    c.drawString(70, 810, "SGB REGENSBURG - PRODUKTIONSDATEN")
    
    # 3. Logo einfügen
    skript_pfad = os.path.dirname(os.path.abspath(__file__))
    logo_pfad = os.path.join(skript_pfad, "bilder", "logo.png")
    if os.path.exists(logo_pfad):
        c.drawImage(logo_pfad, 70, 750, width=100, height=40, mask='auto')

    # 4. Textdaten schreiben
    c.setFont("Helvetica", 12)
    y_pos = 720
    abstand = 20
    
    c.drawString(70, y_pos, f"Auftragsnummer: {auftrag}")
    c.drawString(70, y_pos - abstand, f"Kunde: {kunde}")
    c.drawString(70, y_pos - 2*abstand, f"Typ: {daten[1]}")
    c.drawString(70, y_pos - 3*abstand, f"Leistung: {daten[2]}")
    c.drawString(70, y_pos - 4*abstand, f"Spannung: {daten[3]}")
    c.drawString(70, y_pos - 5*abstand, f"Schaltgruppe: {gruppe}")
    
    # 5. Schaltbild einfügen
    bild_pfad = hole_bild_pfad(gruppe)
    if bild_pfad:
        c.drawString(70, 550, "Schaltbild / Vector Group:")
        c.drawImage(bild_pfad, 70, 420, width=300, height=100, mask='auto')
    
    c.save()
    return voller_pfad