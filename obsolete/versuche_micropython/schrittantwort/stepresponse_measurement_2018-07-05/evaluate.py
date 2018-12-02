import os
import pyplot

MEAN = 5

def find(listMeas, fT, key):
    for i in range(300, len(listMeas)):
        if fT < key(listMeas[i]):
            return listMeas[i]

class LineEquation():
    def __init__(self, listMeas, fT_Min, fT_Max, key):
        self.key = key
        self.measT_Min = find(listMeas, fT_Min, key)
        self.measT_Max = find(listMeas, fT_Max, key)

    def plot(self, objCurve):
        objCurve.point(self.measT_Min.iTime, self.key(self.measT_Min))
        objCurve.point(self.measT_Max.iTime, self.key(self.measT_Max))

class evaluateMeas:
    def __init__(self, fMeas, strMeasFilename, listMeas):
        mean(listMeas)
        fTO_Min = min([meas.fTO for meas in listMeas[250:300]])

        fTO_Max = max([meas.fTO for meas in listMeas[2000:len(listMeas)-MEAN]])

        fTOunten_Max = max([meas.fTOunten for meas in listMeas[2000:len(listMeas)-MEAN]])

        fTO_MaxDiff = fTO_Max - fTO_Min

        fTO_Min_plusLower = fTO_Min + 0.3
        fTO_Min_plusHigher = fTO_Min + 0.8

        self.lineTO = LineEquation(listMeas, fTO_Min_plusLower, fTO_Min_plusHigher, lambda meas: meas.fTO)
        self.lineTH = LineEquation(listMeas, fTO_Min_plusLower, fTO_Min_plusHigher, lambda meas: meas.fTH)

        # measTO_Min_plusLower = find(listMeas, fTO_Min_plusLower, lambda meas: meas.fTO)
        # measTO_Min_plusHigher = find(listMeas, fTO_Min_plusHigher, lambda meas: meas.fTO)

        # measTH_Min_plusLower = find(listMeas, fTO_Min_plusLower, lambda meas: meas.fTH)
        # measTH_Min_plusHigher = find(listMeas, fTO_Min_plusHigher, lambda meas: meas.fTH)

        fMeas.write('%s\t%.2f\t%.2f\t%.2f\t%.2f\n' % (strMeasFilename, fTO_MaxDiff, fTO_Min, fTO_Max, fTOunten_Max))
    
    def plot(self, objCurve):
        self.lineTO.plot(objCurve)
        self.lineTH.plot(objCurve)

def mean(listMeas):
    def __mean(i, key):
        l = [key(meas) for meas in listMeas[i-MEAN:i+MEAN]]
        l.sort()
        return l[MEAN]

    for i in range(MEAN, len(listMeas)-MEAN):
        listMeas[i].fTO = __mean(i, lambda meas: meas.fTO)
        listMeas[i].fTH = __mean(i, lambda meas: meas.fTH)
        listMeas[i].fTOunten = __mean(i, lambda meas: meas.fTOunten)

class Measurement:
    def __init__(self, strLine):
        listColums = strLine.strip().split('\t')
        self.iTime = int(listColums[0])
        self.fPower = float(listColums[2])
        self.fTO = float(listColums[3])
        self.fTH = float(listColums[4])
        self.fTOunten = float(listColums[5])

with open('evaluate_out.txt', 'w') as fMeas:
    fMeas.write('strMeasFilename\tfTO_MaxDiff\tfTO_Min\tfTO_Max\tfTOunten_Max\n')

    for strMeasFilename in os.listdir('.'):
        if not os.path.isfile(strMeasFilename):
            continue
        if not strMeasFilename.startswith('meas_'):
            continue
        if not strMeasFilename.endswith('.txt'):
            continue
        print(strMeasFilename)
        with open(strMeasFilename, 'r') as f:
            objCurvePower = pyplot.Curve('Power', 'red')
            objCurveO = pyplot.Curve('O', 'red')
            objCurveH = pyplot.Curve('H', 'orange')
            objCurveOunten = pyplot.Curve('Ounten', 'green')
            listMeas = []
            for strLine in f.readlines():
                if strLine.startswith('time'):
                    continue
                meas = Measurement(strLine)
                listMeas.append(meas)

                objCurvePower.point(meas.iTime, meas.fPower)
                objCurveO.point(meas.iTime, meas.fTO)
                objCurveH.point(meas.iTime, meas.fTH)
                objCurveOunten.point(meas.iTime, meas.fTOunten)

            objEvaluate = evaluateMeas(fMeas, strMeasFilename, listMeas)
            objCurveEvaluate = pyplot.Curve('Evaluate', 'gray')
            objEvaluate.plot(objCurveEvaluate)

            strFilenamePlot = strMeasFilename.replace('.txt', '_plot.png')
            plot = pyplot.Plot('Time [s]')
            plot.PlotY1('Temperature [C]', objCurveO, objCurveH, objCurveOunten, objCurveEvaluate)
            plot.PlotY2('Heat [W]', objCurvePower)
            plot.PlotSave(strFilenamePlot)

