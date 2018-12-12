#
# Create directories (git doesn't store directories)
#

mkdir -p ~pi/tempstabilizer2018/software/http_server/node_data/grafana_to_process
mkdir -p ~pi/tempstabilizer2018/software/http_server/node_data/grafana_processed
mkdir -p ~pi/tempstabilizer2018/software/http_server/node_data/grafana_failed
mkdir -p ~pi/tempstabilizer2018/software/http_server/node_data/apache_logs
mkdir -p ~pi/tempstabilizer2018/software/http_server/node_data/swdownload

chown -R pi:pi ~pi/tempstabilizer2018
