import csv
import random

# --- SGB GIESSHARZ PORTFOLIO ---

kunden = ["Stadtwerke München", "Deutsche Bahn InfraGO", "Tesla Gigafactory Berlin",
          "BASF Ludwigshafen", "Flughafen Frankfurt", "Intel Magdeburg",
          "Google Rechenzentrum", "BMW Werk Regensburg", "Audi Ingolstadt"]

# Gießharz-Typen
typen = ["SGB Gießharz-Trafo DTTH", "SGB Gießharz-Trafo DTTH (Klimaklasse C2)",
         "SGB Gießharz-Trafo (E3 - Wind)", "SGB Safe (Rechenzentrum)"]

# Schaltgruppen
schaltgruppen = ["Dyn5", "Dyn11", "Yyn0", "YNd11", "Dd0"]

def generiere_sgb_daten(anzahl=100):
    daten = []
    # Kopfzeile
    daten.append(["Auftragsnummer",
                  "Typ",
                  "Leistung_MVA",
                  "Spannung_Pri_kV",
                  "Schaltgruppe",
                  "Kunde"])

    for i in range(1, anzahl + 1):
        nr = f"SGB-2025-{i:03d}"

        typ = random.choice(typen)
        gruppe = random.choice(schaltgruppen)
        kunde = random.choice(kunden)

        # Realistische Werte für Gießharz (bis max 25 MVA laut Stellenanzeige)
        leistung = random.choice([0.4, 0.63, 1.0, 2.5, 6.3, 10.0, 15.0, 20.0, 25.0])

        # Typische Mittelspannungen
        spannung = random.choice([10, 15, 20, 30, 36])

        daten.append([nr, typ, f"{leistung} MVA", f"{spannung} kV", gruppe, kunde])

    return daten

# --- AUSFÜHREN ---
meine_daten = generiere_sgb_daten(100)

filename = "sgb_production_data.csv"
with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(meine_daten)

print(f" Datei '{filename}' mit 100 Gießharz-Datensätzen erstellt.")