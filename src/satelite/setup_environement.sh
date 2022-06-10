#!/bin/sh
sudo cat > /etc/profile.d/91mqtt.sh << EOF
#!/bin/sh

export MQTT_BROCKER="192.168.1.167"
export MQTT_PORT="1883"
export MQTT_TOPIC="Firefighter/Measure"
EOF
