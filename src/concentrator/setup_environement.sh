
#!/bin/sh

sudo cat > /etc/environment.d/50Firefighter.conf << EOF
MQTT_CLIENT="client-001"
MQTT_BROCKER="127.0.0.1"
MQTT_PORT="1883"
MQTT_TOPIC="Firefighter/Measure"

INFLUXDB_SERVER="https://eu-central-1-1.aws.cloud2.influxdata.com"
INFLUXDB_TOKEN="vr70B3T-4ykI4b9jKBUMuvAFtiCu6_lpU3nkj4a8jIEP4M0D2l5fowHUFRzWQ0VyPnOqxE8V8mp_FynQfApXmw=="
INFLUXDB_ORG="lucas.gosteli@outlook.com"
INFLUXDB_BUCKET="lucas.gosteli's Bucket"
EOF