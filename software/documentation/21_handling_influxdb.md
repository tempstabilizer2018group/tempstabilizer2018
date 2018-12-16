# Handling influxdb

## Start/Stop
sudo service influxdb start


# installation
http://www.andremiller.net/content/grafana-and-influxdb-quickstart-on-ubuntu

influx
CREATE DATABASE tempstabilizer2018
CREATE USER pi WITH PASSWORD 'XXXentercorreptpwXXXX' WITH ALL PRIVILEGES
exit

USE tempstabilizer
INSERT tempH,host=node4711 value=22.3
SELECT * from tempH
exit

curl -i -XPOST 'http://localhost:8086/write?db=tempstabilizer' --data-binary 'tempH,node=node4711 value=22.6'

curl -i -XPOST 'http://localhost:8086/write?db=tempstabilizer' --data-binary 'tempO,node=node4711 value=21.0'

https://maxchadwick.xyz/blog/grafana-influxdb-annotations
curl -i -XPOST 'http://localhost:8086/write?db=tempstabilizer' --data-binary 'events title="Reboot",text="<a href='https://github.com'>Release notes</a>",tags="node4711,node4712"'
curl -i -XPOST 'http://localhost:8086/write?db=tempstabilizer' --data-binary 'events title="Reboot",text="Hello <b>World</b>",tags="node4711,node4712"'

