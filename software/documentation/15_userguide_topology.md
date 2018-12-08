# The topology of the temp_stabilizer_2018 infrastructure

## Servers

### temp_stabilizer_2018

synonym: `ESP32`

### Raspberri Pi

synonym: `Pi`

- Is used as development environment.
- Is used to do firmware-updates over RS232.
- Is used to do software-updates over WLAN.
- Is as `HTTP-Server`.
- Is a `Grafana-Server`.

### HTTP-Server

The `HTTP-Server`
- receives Grafana-Files from the `temp_stabilizer_2018`
- archives the Grafana-Files.
- sends the Grafana-Files to the influxdb on the `Grafana-Server`.
- holds a copy of the git-repository.
- runs a python-server-webpage to
  - receive the grafana-files
  - prepare software-updates

### Grafana-Server

- The `Grafana-Server` runs grafana.
- The `Grafana-Server` runs influxdb.

## Network - Security

Principle:
- There is no confidential data on the `ESP32`.
- There is no confidential data in the github-repositories.
- The `Pi` offers a public network. The `Pi` itself forwards traffic to www.tempstabilizer2018.ch but to no other IP.
- The `Pi` may contain passwords for:
  - login 'pi'
  - Git Repositories
  - influxdb servers
  - grafana access

## Network - Fix coded addresses in the firmware

Steps for the `ESP32`-firmware to get software-updates:
 - connect to SSID [TempStabilizer2018](https://github.com/tempstabilizer2018group/temp_stabilizer_2018/blob/master/software_rpi/rpi_root/etc/hostapd/hostapd.conf) without security.
 - if the AP has the [IP-address](https://github.com/tempstabilizer2018group/temp_stabilizer_2018/blob/master/software_rpi/rpi_root/etc/dhcpcd.conf) of the `Pi`:
   - connect to http://[192.168.4.1:3001](https://github.com/tempstabilizer2018group/micropython_esp32/blob/master/ports/esp32/modules/hw_update_ota.py)/softwareupdate?mac=12:12:12:12&version=v0.9.8
 - else
   - connect to http://[www.tempstabilizer2018.org](https://github.com/tempstabilizer2018group/micropython_esp32/blob/master/ports/esp32/modules/hw_update_ota.py)/softwareupdate?mac=12:12:12:12&version=v0.9.8

## Network - Push of the Grafana Logs

The Url to push the Grafana logs is the same as above.