# Userguide for the HTTP-Server

## Apache

### Start/Stop

```bash
sudo systemctl stop apache2
sudo systemctl start apache2
```

### The configuration file

```bash
/etc/apache2/sites-enabled/tempstabilizer2018.conf
```

### The webpage

http://localhost:80

```bash
/home/pi/tempstabilizer2018/software/http_server/python/python3_wsgi_app.wsgi
```

### The logfiles

```bash
/home/pi/tempstabilizer2018/software/http_server/node_data/apache_logs
  access.log
  error.log
```

```bash
tail -f /home/pi/tempstabilizer2018/software/http_server/node_data/apache_logs/*
```

### The grafana datafiles

```bash
/home/pi/tempstabilizer2018/software/http_server/node_data
  grafana_to_process
  grafana_processed
  grafana_failed
```

### The swdownload cache

```bash
/home/pi/tempstabilizer2018/software/http_server/node_data/swdownload
```
