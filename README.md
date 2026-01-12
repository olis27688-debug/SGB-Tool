https://github.com/user-attachments/assets/154d7757-12e1-421a-af90-5eb9c007b85b

Es handelt sich um einen funktionsfähigen Software-Prototypen, der zeigt, wie ich die Anforderungen der Stellenanzeige (Python, GUI, Modularität) technisch umsetzen würde.

Idee & Funktion

Das Programm simuliert den Prozess der Schaltschild-Erstellung:

Datenimport: Einlesen von fiktiven Produktionsdaten (simuliert als CSV-Datei).

Auswahl: Über eine grafische Benutzeroberfläche (GUI) kann ein Auftrag ausgewählt werden.

Visualisierung: Das Tool zeigt automatisch die passenden technischen Daten und das korrekte Schaltbild (Vektorgrafik) an.

Generierung: Auf Knopfdruck wird ein technisches Typenschild als PDF erstellt.

Aufbau des Codes

Um die geforderte "Baustein-Bibliothek" abzubilden, habe ich den Code in Frontend und Backend getrennt:

main.py: Enthält nur die Benutzeroberfläche (Frontend mit tkinter).

SGB_library.py: Enthält die gesamte Logik (Daten laden, Bilder verarbeiten, PDF zeichnen), damit diese Funktionen wiederverwendbar sind.

sgb_production_data.csv: Ein Datensatz, den ich generiert habe, um das Gießharz-Portfolio (z.B. Dyn5, 20 MVA) zu simulieren.

Nutzung

Voraussetzung ist eine Python-Installation. Zusätzlich werden folgende Pakete benötigt:

pip install reportlab pillow


Starten der Anwendung:

python main.py


Im Fenster einen Auftrag aus dem Dropdown-Menü wählen.

Auf "PDF Generieren" klicken.

Das fertige PDF liegt anschließend im Ordner pdf_druck.

Erstellt von Oliver Siegmund, Dezember 2025.
