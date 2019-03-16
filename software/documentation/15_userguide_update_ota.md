# Userguide: Software Update

## Step 1: Hotspot
Setup Hotspot
- SSID: TempStabilizer2018
- <RPI3_WLAN_PW>
- WPA PSK

## Step 2: Format Filesystem

- Power down
- Press button
- Power on
- Wait till led flasheds
  - The filesystem is now formated
- Release button

## Step 3: Update software

If the filesystem is empty, a software update will be started.

- Place the Raspberry Pi in WLAN-reach
- Raspberry Pi: Start the update-server
- You may want to observer the update
  - Raspberry Pi: tail -f '/home/pi/tempstabilizer2018/software/http_server/node_data/apache_logs/access.log'
  - Observe the ESP32-RS232-Output
  - Observe the events on Grafana
  - Observe the update-page on the webserver
- Power on the temp_stabilizer_2018
  - The temp_stabilizer_2018 will start the software-update

## Where the SW-Update is coming from

The softwareupdate may come from four places:

HTTP-Server               | local/remote | http://<server>/versioncheck?mac=3C71BF0F97A4&version=none
:------------------------:|:------------:| ----------------------------------------------------------
rpi                       | local        | ...;strRepo='local on raspberrypi'
rpi                       | remote       | ...;strRepo='github.com via raspberrypi'
tempstabilizer2018.org    | local        | ...;strRepo='local on tempstabilizer2018.org'
tempstabilizer2018.org    | remote       | ...;strRepo='github.com via tempstabilizer2018.org'

You may open `http://<server>\intro.html` and call `/versioncheck`. This will display the versionstring as shown in the table above.

### local/remote: config_http_server.py
```
# True: Don't connect to www.github.com and get the files locally
# False: Get files from www.github.com
bGithubPullLocal = False
```

To switch between local/remote, the above file must be edited and apache restarted `sudo systemctl restart apache2`.

### rpi/tempstabilizer2018.org

The node gets the update from Rpi if:
- Rpi is running
- Rpi-Apache is running
- Rpi-Wlan in on

## `HTTP-Get http://192.168.4.1/softwareupdate?mac=...` returns HTTP 400 (error) instead of 200

When this error is displayed on the rs232 console of the node, it might be that the HTTP-server can't compile the python files.

Switch off precompiling of the python files:

`config_http_server.py`: `bDoMpyCrossCompile = False`

`sudo systemctl restart apache2`

Now, the node may be updated and the compile-error will be displayed on the nodes-console.
