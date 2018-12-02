# -*- coding: utf-8 -*-

# Ausgangsstufe DAC und FET

fR2 = 3.0	# Widerstand unter FET
fVoltageDAC = 3.3	# Full Range of DAC
fDACFS = 4096 # Full Range DAC

# Umrechnung Spannung auf DAC
'''
iDAC = fUsoll * fDACFS / fVoltageDAC

'''

# Wie schnell darf UDAC erhoeht werden ohne eine Zerstoerung vom FET zu riskieren weil dieser schneller Warm wird als der H-Sensor es messen kann

fMaxUDAC = 0.0 # Startwert UDAC, dieser Wert wird spaeter erhoeht. Die Maximale Leistung vom FET soll so 7W sein. BUK9875-100A, Limiting values, total power dissipation, 8W
fSecurePowerIncreaseW = 1.0 # maximale Erhoehung der Leistung ohne Gefahr den FET zu ueberhitzen
fMaxSupplyFETV = 48.0 # maximale Speisung vom FET
fSecureUDACIncreaseV = fSecurePowerIncreaseW * fR2 / fMaxSupplyFETV

fTauIncreaseUDACs = 10.0 # Zeitkonstante zum erstmaligen erhoehen der Spannung


fUDACzeroHeat = 0.0 # sicherer Startwert UDAC Grenze wo FET zu leiten beginnt. Regelt sich spaeter ein auf BUK9875-100A, gate-source threshold voltage, typ 1.5V

fdts = 0.2 # sekunden Verstrichene Zeit seit letzter Berechnung

fSetHeatW = 5.0 # Test, Leistung auf diesen Wert setzen

fUDAC_gefiltert = 0.0

fUDACsollV = fSetHeatW * fR2 / fMaxSupplyFETV + fUDACzeroHeat

time = 0.0

for counter in range(500):

    fUDACV = min( fUDACsollV , fMaxUDAC) # Spannung wird an DAC angelegt
    fUDAC_gefiltert = fUDAC_gefiltert + (fUDACV - fUDAC_gefiltert) / fTauIncreaseUDACs * fdts
    fMaxUDAC = max ( fUDAC_gefiltert + fSecureUDACIncreaseV, fMaxUDAC) # die Grenze wird allenfalls erhoeht
    time = time + fdts

    print ("time, fUDACV, fUDAC_gefiltert, fMaxUDAC:  %0.3f %0.3f %0.3f %0.3f" % ( time, fUDACV, fUDAC_gefiltert, fMaxUDAC))



'''

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

'''
