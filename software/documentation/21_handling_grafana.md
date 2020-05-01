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

Create new Dashboard - New Panel - Choose Visualization 0 Graph
  Query: SELECT "value" FROM "tempH" WHERE $timeFilter GROUP BY "host"

Or: Create Dashboard - "New Dashboard" - Import dashboard - Paste JSON 'json_model_2020-05-01a.txt'