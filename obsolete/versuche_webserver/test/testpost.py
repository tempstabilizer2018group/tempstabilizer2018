# Python 2
# import urllib2

# Python 3
from urllib.request import urlopen, Request

strData = b'''Ein Fruehlingsabend in Paris
Das Wetter ist ein bisschen mies
Il fait tres froid und dann il pleut
Ich werde nass und denk: "Och noe!"'''

# req = Request('http://tempstabilizer.positron.ch/push/upload.grafana')
req = Request('http://tempstabilizer.positron.ch/push/upload.grafana?site=waffenplatz&node=4711')
# req = Request('http://tempstabilizer.positron.ch/a.html')
req.add_header('Content-Type', 'application/text')
response = urlopen(req, data=strData)
# response = urlopen(req)
print('Response: ' + str(response.read()))
