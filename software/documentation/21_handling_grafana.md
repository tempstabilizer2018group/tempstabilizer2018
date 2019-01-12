# Handling Grafana

http://10.0.11.237:3000/datasources/new
  Name: tempstabilizer
  Type: InfluxDB
  HTTP-URL: http://localhost:8086
  HTTP-Access: proxy
  Auto-Basic Auth: No
  Auto-TLS Client Auth: No
  InfluxDB Details-Database: tempstabilizer
   InfluxDB Details-User: maerki maerki

Create new Dashboard - New Panel - Graph
  Query: SELECT "value" FROM "tempH" WHERE $timeFilter GROUP BY "host"
