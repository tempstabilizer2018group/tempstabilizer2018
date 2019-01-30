# Handling Grafana

http://tempstabilizer2018.org:3000/datasources/new
  Type: InfluxDB
  Name: tempstabilizer2018
  Default: Yes
  HTTP-URL: http://localhost:8086
  HTTP-Access: Server (Default)
  Auth: uncheck all
  InfluxDB Details-Database: tempstabilizer2018
  InfluxDB Details-User: pi
  InfluxDB Details-Password: <<<strInfluxDbPw>>>

Create new Dashboard - New Panel - Graph
  Query: SELECT "value" FROM "tempH" WHERE $timeFilter GROUP BY "host"
