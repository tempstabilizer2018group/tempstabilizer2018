# Handling influxdb

## Key Concepts
https://docs.influxdata.com/influxdb/v1.7/concepts/key_concepts/
 Fields: butterflies, honeybees 
   fields are not indexed
 Tags: location scientist
   tags are indext
 Measurement: acts as a container for tags, fields, and the time column.

## Start/Stop
sudo service influxdb start


# installation
http://www.andremiller.net/content/grafana-and-influxdb-quickstart-on-ubuntu

influx
CREATE DATABASE tempstabilizer2018
CREATE USER pi WITH PASSWORD 'XXXentercorreptpwXXXX' WITH ALL PRIVILEGES
exit

USE tempstabilizer2018
INSERT tempH,node=node4711 value=22.3
SELECT * from tempH
exit

curl -i -XPOST 'http://localhost:8086/write?db=tempstabilizer' --data-binary 'tempH,node=node4711 value=22.6'

curl -i -XPOST 'http://localhost:8086/write?db=tempstabilizer' --data-binary 'tempO,node=node4711 value=21.0'

https://maxchadwick.xyz/blog/grafana-influxdb-annotations
curl -i -XPOST 'http://localhost:8086/write?db=tempstabilizer' --data-binary 'events title="Reboot",text="<a href='https://github.com'>Release notes</a>",tags="node4711,node4712"'
curl -i -XPOST 'http://localhost:8086/write?db=tempstabilizer' --data-binary 'events title="Reboot",text="Hello <b>World</b>",tags="node4711,node4712"'


## Useful Queries
USE tempstabilizer2018

drop series from labHombi

https://indico.cern.ch/event/664210/contributions/2712273/attachments/1526684/2387385/Andrei_DUMITRU_-_InfluxDB.pdf
> SHOW MEASUREMENTS
name: measurements
name
----
labHombi

> SHOW SERIES
key
---
labHombi,node=name_20181217_11
labHombi,node=name_20181217_12
labHombi,node=name_20181217_13
labHombi,node=name_20181217_14
labHombi,node=name_20181217_16
labHombi,node=name_20181217_17
labHombi,node=name_20181217_19
labHombi,node=name_20181217_20
labHombi,node=name_20181217_21
labHombi,node=name_20181217_22
labHombi,node=name_20181217_23
labHombi,node=name_20181217_24
labHombi,node=name_20181217_25
labHombi,node=steel

> SHOW TAG KEYS
name: labHombi
tagKey
------
node

> SELECT * FROM EVENTS

> SHOW TAG KEYS FROM labHombi
name: labHombi
tagKey
------
node

> SHOW FIELD KEYS FROM labHombi
name: labHombi
fieldKey           fieldType
--------           ---------
PidH_bLimitHigh    float
fDACzeroHeat_V     float
fDiskFree_MBytes   float
fHeat_W            float
fSupplyVoltage_V   float
fTempEnvirons_51_C float
fTempEnvirons_C    float
fTempEnvirons_C_4C float
fTempEnvirons_C_50 float
fTempEnvirons_C_51 float
fTempEnvirons_C_52 float
fTempEnvirons_C_53 float
fTempEnvirons_C_58 float
fTempEnvirons_C_59 float
fTempO_C           float
fTempO_Setpoint_C  float

> SHOW series FROM labHombi
key
---
labHombi,node=name_20181217_11
labHombi,node=name_20181217_12
labHombi,node=name_20181217_13
labHombi,node=name_20181217_14
labHombi,node=name_20181217_16
labHombi,node=name_20181217_17
labHombi,node=name_20181217_19
labHombi,node=name_20181217_20
labHombi,node=name_20181217_21
labHombi,node=name_20181217_22
labHombi,node=name_20181217_23
labHombi,node=name_20181217_24
labHombi,node=name_20181217_25
labHombi,node=steel

----------------
SELECT count(value) FROM tempH
SELECT count(value) FROM tempH WHERE node='node4711'

DROP SERIES FROM /.*/
----------------
SELECT time,node,value FROM tempH

SHOW TAG VALUES FROM tempH WITH KEY in ("node")





------------------------ Min Max Avg
https://www.neteye-blog.com/2017/02/how-to-tune-your-grafana-dashboards/


=================================
SHOW TAG VALUES FROM fTempO_C WITH KEY in ("node")

SHOW field KEYS FROM [[site]]


SHOW TAG VALUES with key = "node"
name: httptest
key  value
---  -----
node 4712

name: httptest2
key  value
---  -----
node 4713
node 4714

SHOW TAG VALUES from "httptest2" with key = "node"
name: httptest2
key  value
---  -----
node 4713
node 4714
