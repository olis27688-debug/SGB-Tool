"""
SGB Schaltschild Manager - Backend Library
Enthält die Logik für Datenimport, Bildverwaltung und PDF-Generierung.
"""

import os
import csv
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


# -----------------------------------------------------------------------------
# DATEN-IMPORT (CSV & MATLAB)
# -----------------------------------------------------------------------------
def lade_matlab_export():
    """
    Liest die simulierte MATLAB-Exportdatei (matlab_export.csv).
    Gibt die erste Datenzeile zurück oder None.
    """
    skript_pfad = os.path.dirname(os.path.abspath(__file__))
    matlab_pfad = os.path.join(skript_pfad, "matlab_export.csv")

    if not os.path.exists(matlab_pfad):
        return None  # Datei noch nicht da (Ingenieur rechnet noch)

    try:
        with open(matlab_pfad, "r", encoding="utf-8") as datei:
            reader = csv.reader(datei)
            next(reader)  # Header von Matlab überspringen
            zeile = next(reader)  # Die erste Datenzeile holen
            return zeile
    except Exception as e:
        print(f"Fehler beim Matlab-Import: {e}")
        return None


def lade_daten():
    """
    Lädt die Hauptdatenbank (sgb_production_data.csv).
    Gibt eine Liste aller Aufträge zurück.
    """
    alle_auftraege = []
    skript_pfad = os.path.dirname(os.path.abspath(__file__))
    csv_pfad = os.path.join(skript_pfad, "sgb_production_data.csv")

    if not os.path.exists(csv_pfad):
        return []

    with open(csv_pfad, "r", encoding="utf-8") as datei:
        for zeile in datei:
            saubere_zeile = zeile.strip()
            # Nur verarbeiten, wenn Zeile nicht leer ist
            if saubere_zeile:
                daten_liste = saubere_zeile.split(",")
                alle_auftraege.append(daten_liste)
    return alle_auftraege


# -----------------------------------------------------------------------------
# BILD-VERWALTUNG (ASSETS)
# -----------------------------------------------------------------------------
def hole_bild_pfad(name):
    """Hilfsfunktion: Sucht den echten Dateipfad (PNG oder JPG) für ein Bild."""
    if not name:
        return None
    name = name.strip()
    skript_pfad = os.path.dirname(os.path.abspath(__file__))

    pfad_png = os.path.join(skript_pfad, "bilder", name + ".png")
    pfad_jpg = os.path.join(skript_pfad, "bilder", name + ".jpg")

    if os.path.exists(pfad_png):
        return pfad_png
    if os.path.exists(pfad_jpg):
        return pfad_jpg
    return None


def lade_bild(name):
    """Lädt ein Bild, skaliert es und wandelt es für Tkinter um."""
    pfad = hole_bild_pfad(name)

    if pfad:
        print(f"---> Suche Bild: '{pfad}'")
        try:
            original = Image.open(pfad)
            original.thumbnail((500, 300))  # Proportionales Skalieren
            bild = ImageTk.PhotoImage(original)
            return bild
        except Exception:
            return None
    return None


# -----------------------------------------------------------------------------
# PDF GENERIERUNG (REPORTLAB)
# -----------------------------------------------------------------------------
def generiere_pdf(daten):
    """
    Erstellt ein technisches Typenschild als PDF.
    Daten-Format: [Auftrag, Typ, Leistung, Spannung, Gruppe, Kunde]
    """
    # Daten zerlegen
    auftrag = daten[0]
    kunde = daten[5]
    gruppe = daten[4]

    # Ordner für PDFs erstellen
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
    c.rect(50, 400, 500, 400)  # Großer Rahmen

    c.setFont("Helvetica-Bold", 18)
    c.drawString(70, 810, "SGB REGENSBURG - PRODUKTIONSDATEN")

    # 3. Logo einfügen
    logo_pfad = os.path.join(skript_pfad, "bilder", "logo.png")
    if os.path.exists(logo_pfad):
        # x, y, width, height
        c.drawImage(logo_pfad, 70, 750, width=100, height=40, mask='auto')

    # 4. Textdaten schreiben
    c.setFont("Helvetica", 12)
    y_pos = 720
    abstand = 20

    # Sicherstellen, dass genug Daten vorhanden sind
    if len(daten) >= 6:
        c.drawString(70, y_pos,             f"Auftragsnummer:  {auftrag}")
        c.drawString(70, y_pos - abstand,   f"Kunde:           {kunde}")
        c.drawString(70, y_pos - 2*abstand, f"Typ:             {daten[1]}")
        c.drawString(70, y_pos - 3*abstand, f"Leistung:        {daten[2]}")
        c.drawString(70, y_pos - 4*abstand, f"Spannung:        {daten[3]}")
        c.drawString(70, y_pos - 5*abstand, f"Schaltgruppe:    {gruppe}")

        # 5. Schaltbild einfügen
        bild_pfad = hole_bild_pfad(gruppe)
        if bild_pfad:
            c.drawString(70, 550, "Schaltbild / Vector Group:")
            c.drawImage(bild_pfad, 150, 420, width=300, height=100, mask='auto')

    c.save()
    return voller_pfad