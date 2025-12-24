% --- SGB TRAFO BERECHNUNGS-SIMULATION ---
% Dieses Skript simuliert eine abgeschlossene Berechnung eines Trafos
% und exportiert die Ergebnisse für die Python-Weiterverarbeitung.

clc; clear;
fprintf('Starte komplexe Feldberechnung...\n');
pause(1); % Kurze Pause für den "Rechen-Effekt"

% 1. Simulierte Ergebnisse (Ingenieur-Daten)
Auftrag     = "SGB-2025-MATLAB";
Kunde       = "Siemens Energy";
Typ         = "DTTH 4000";
Leistung    = "4.0 MVA";
Spannung    = "20 kV";
Schaltgruppe = "Dyn5";

% 2. Tabelle erstellen
TrafoDaten = table(Auftrag, Typ, Leistung, Spannung, Schaltgruppe, Kunde);

% 3. Export als CSV (Die Schnittstelle)
dateiname = 'matlab_export.csv';


pfad = '/Users/macncheese/SGB-Projekt/';
full_path = fullfile(pfad, dateiname);

writetable(TrafoDaten, full_path);

fprintf('✅ Berechnung fertig.\n');
fprintf('Daten exportiert nach: %s\n', full_path);