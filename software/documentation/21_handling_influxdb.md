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
CREATE USER pi WITH PASSWORD '<<<strInfluxDbPw>>>' WITH ALL PRIVILEGES
exit

USE tempstabilizer2018
INSERT fTempO_C,node=node4711 value=22.3
SELECT * from fTempO_C
exit

curl -i -XPOST 'http://localhost:8086/write?db=tempstabilizer' --data-binary 'fTempO_C,node=node4711 value=22.6'

curl -i -XPOST 'http://localhost:8086/write?db=tempstabilizer' --data-binary 'tempO,node=node4711 value=21.0'

https://maxchadwick.xyz/blog/grafana-influxdb-annotations
curl -i -XPOST 'http://localhost:8086/write?db=tempstabilizer2018' --data-binary 'events title="Reboot",text="<a href='https://github.com'>Release notes</a>",tags="node4711,node4712"'
curl -i -XPOST 'http://localhost:8086/write?db=tempstabilizer2018' --data-binary 'events title="Reboot",text="Hello <b>World</b>",tags="node4711,node4712"'


## Useful Queries
USE tempstabilizer2018

drop series from labHombi

> SELECT * FROM EVENTS

https://indico.cern.ch/event/664210/contributions/2712273/attachments/1526684/2387385/Andrei_DUMITRU_-_InfluxDB.pdf
> SHOW MEASUREMENTS
name: measurements
name
----
labHombi

> SHOW SERIES
key
---
labHombi,node=12,origin=tempstabilizer2018
labHombi,node=16,origin=tempstabilizer2018
labHombi,node=17,origin=tempstabilizer2018
labHombi,node=18,origin=tempstabilizer2018
labHombi,node=20,origin=tempstabilizer2018
labHombi,node=22,origin=tempstabilizer2018
labHombi,node=23,origin=tempstabilizer2018
labHombi,node=24,origin=tempstabilizer2018
labHombi,node=steel,origin=tempstabilizer2018

> SHOW SERIES from /.*/ WHERE node='24'
key
labHombi,node=24,origin=tempstabilizer2018

> SHOW SERIES from /.*/ WHERE origin='tempstabilizer2018'
key
labHombi,node=11,origin=tempstabilizer2018
labHombi,node=12,origin=tempstabilizer2018
labHombi,node=13,origin=tempstabilizer2018
labHombi,node=14,origin=tempstabilizer2018
labHombi,node=15,origin=tempstabilizer2018
labHombi,node=16,origin=tempstabilizer2018
labHombi,node=17,origin=tempstabilizer2018
labHombi,node=18,origin=tempstabilizer2018
labHombi,node=20,origin=tempstabilizer2018
labHombi,node=22,origin=tempstabilizer2018
labHombi,node=23,origin=tempstabilizer2018
labHombi,node=24,origin=tempstabilizer2018

> SHOW SERIES WHERE origin='tempstabilizer2018'
key
labHombi,node=11,origin=tempstabilizer2018
labHombi,node=12,origin=tempstabilizer2018
labHombi,node=13,origin=tempstabilizer2018
labHombi,node=14,origin=tempstabilizer2018
labHombi,node=15,origin=tempstabilizer2018
labHombi,node=16,origin=tempstabilizer2018
labHombi,node=17,origin=tempstabilizer2018
labHombi,node=18,origin=tempstabilizer2018
labHombi,node=20,origin=tempstabilizer2018
labHombi,node=22,origin=tempstabilizer2018
labHombi,node=23,origin=tempstabilizer2018
labHombi,node=24,origin=tempstabilizer2018
 
> SHOW TAG KEYS
name: labHombi
tagKey
------
tagKey
environs
node
origin

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

> SHOW TAG KEYS FROM labHombi
name: labHombi
--------------
tagKey
environs
node
origin


> SHOW series FROM labHombi
key
---
labHombi,node=11,origin=tempstabilizer2018
labHombi,node=12,origin=tempstabilizer2018
labHombi,node=13,origin=tempstabilizer2018
labHombi,node=14,origin=tempstabilizer2018
labHombi,node=15,origin=tempstabilizer2018
labHombi,node=16,origin=tempstabilizer2018
labHombi,node=17,origin=tempstabilizer2018
labHombi,node=18,origin=tempstabilizer2018
labHombi,node=20,origin=tempstabilizer2018
labHombi,node=22,origin=tempstabilizer2018
labHombi,node=23,origin=tempstabilizer2018
labHombi,node=24,origin=tempstabilizer2018
labHombi,node=steel,origin=tempstabilizer2018

----------------
SELECT count(fTempO_C) FROM labHombi
SELECT count(fTempO_C) FROM labHombi WHERE node='24'
SELECT * FROM labHombi where node = '17' limit 5
SELECT * FROM labHombi where environs = '17' limit 5

DROP SERIES FROM /.*/

DROP SERIES WHERE origin='tempstabilizer2018'

----------------
SELECT time,fTempO_C,fHeat_W FROM labHombi

SHOW TAG VALUES FROM fTempO_C WITH KEY in ("node")

select * from labHombi
select fTempO_C from labHombi

select *::field FROM labHombi
select fTempO_C::field FROM labHombi
select fTempO_C::field,node::tag from labHombi
select fTempEnvirons_C_50::field,node::tag from labHombi

------------------------ Min Max Avg
https://www.neteye-blog.com/2017/02/how-to-tune-your-grafana-dashboards/


=================================
SHOW TAG VALUES FROM fTempO_C WITH KEY in ("node")

SHOW field KEYS FROM labHombi


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

SHOW TAG VALUES with key = "origin"
name: labHombi
--------------
key     value
origin  tempstabilizer2018

SHOW TAG VALUES from "httptest2" with key = "node"
name: httptest2
key  value
---  -----
node 4713
node 4714


=================================================
Grafana Annotations

http://docs.grafana.org/reference/annotations/
https://maxchadwick.xyz/blog/grafana-influxdb-annotations
http://docs.grafana.org/http_api/annotations/
https://github.com/sitespeedio/sitespeed.io/issues/1984
https://github.com/underley/annotate-influxdb/pull/3/commits/18ebfa31bc6dcb58a7120c9d6f29952d0cc8c709

> SELECT title,text,tags,severity FROM /.*/ where type = 'event' limit 10
name: ETH-E9
------------
time                    title                           text                            tags    severity
1549093627000000000     INFO ETH-E9 20ETH_Alu_40_isol   networkOnce() took 6440 ms      info    info

name: labHombi
--------------
time                    title                   text                            tags    severity
1548942037000000000     INFO labHombi 17        networkOnce() took 4107 ms      info    info
1549094146000000000     INFO labHombi 24        networkOnce() took 6957 ms      info    info
1549097114000000000     INFO labHombi 23        networkOnce() took 7975 ms      info    info


> SELECT title,text,tags,severity FROM /.*/ where type = 'event' and severity = 'info' limit 10
dito
