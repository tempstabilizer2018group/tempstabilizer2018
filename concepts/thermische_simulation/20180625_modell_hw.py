# -*- coding: utf-8 -*-

# Thermisches Modell der Hardware

fTUmgebung = 20.0	# Umgebungstemperatur in Celsius
fCH = 0.01	# Ws/K	Waermekapazität beim FET, Energie pro Kelvin
fRH = 25.0	# K/W	Wärmewiderstand beim FET zur Umgebung.
fRHO = 238.0	# K/W	Waermewiderstand von FET zu TO
fCO = 1.0	# Ws/K	Waermekapazitaet bei TO, Teilbereich des Bleches
fRO	= 20.0	# K/W	Waermewiderstand von von TO zu Umgebung: Waermeverlust durch Konvektion und Strahlung

# Linearisierung Optokoppler und Heizung mit FET
# Berechnung DAC, spaeter vermutlich komplizierter

fHeatW = 1.0 # Heizleistung Vorgabe in Watt

fFetMaxW = 5.0 # Maximalleiatung
fFetMaxTeil = 1.0 # Spannung Anteil an DAC für Maximalleistung, 1.0 entspricht z.B. 3.3V
fFetminW = 0.0 # Minimalleiatung, fix bei 0.0
fFetminTeil = 0.2 # Spannung Anteil an DAC für Minimalleistung, 0.2 entspricht z.B. 1.0V

fDAC = fHeatW/(fFetMaxW-fFetminW)*(fFetMaxTeil-fFetminTeil)+fFetminTeil
fDAC = sorted([fFetminTeil, fDAC, fFetMaxTeil])[1]# Wertebereich limitieren, spaeter mit Info nach Aussen, dass limitiert


# Beispiel Modell, Berechnung naechste Temperaturen

# Startwerte
fTH = fTUmgebung # Celsius
fTO = fTUmgebung # Celsius
fdt = 0.2 # sekunden Verstrichene Zeit seit letzter Berechnung

for counter in range(1000):

    fHLeistungW = fHeatW - (fTH-fTUmgebung)/fRH - (fTH-fTO)/fRHO # Leistung zu H
    fOLeistungW = (fTH-fTO)/fRHO - (fTO-fTUmgebung)/fRO # Leistung zu O
    fTHnew = fTH + (fHLeistungW * fdt / fCH)
    fTOnew = fTO + (fOLeistungW * fdt / fCO)

    fTH = fTHnew
    fTO = fTOnew

    print counter, fTH, fTO

