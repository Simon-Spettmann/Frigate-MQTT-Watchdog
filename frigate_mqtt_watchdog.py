#!/usr/bin/env python3

import os
import re
import subprocess
import sys

import paho.mqtt.client as mqtt

# Configuration
docker_compose_workspace="/path/to/docker-compose-workspace"

mqtt_host = "homeassistant"
mqtt_port = 1883

container_name = "frigate"

# Frigate MQTT log patterns
mqtt_error_patterns = [
    r"frigate\.comms\.mqtt.*ERROR.*MQTT disconnected",
    r"frigate\.comms\.mqtt.*Unable to publish.*client is not connected"
]
mqtt_success_patterns = [
    r"frigate\.comms\.mqtt.*MQTT connected"
]

def is_mqtt_broker_reachable():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect_timeout = 3

    try:
        client.connect(mqtt_host, mqtt_port)
        client.disconnect()
        return True
    except Exception as e:
        return False

def is_container_running():
    try:
        result = subprocess.run(
            ["docker", "compose", "ps", "--status", "running", "--format", "{{.Name}}"],
            capture_output=True,
            text=True,
            check=True,
        )
        return container_name in result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error checking container status: {e}")
        return False

def is_error_in_container_logs():
    try:
        # Get the last 'log_lines_to_check' lines from the container logs
        result = subprocess.run(
            ["docker", "compose", "logs", container_name],
            capture_output=True,
            text=True,
            check=True,
        )

        # Split  into lines and reverse them (newest first)
        log_lines = result.stdout.splitlines()[::-1]

        # Check the first MQTT-related log line
        for line in log_lines:
            if "frigate.comms.mqtt" in line:
                if any(re.search(pattern, line) for pattern in mqtt_error_patterns):
                    return True
                if any(re.search(pattern, line) for pattern in mqtt_success_patterns):
                    return False
                break

        return False

    except subprocess.CalledProcessError as e:
        print(f"Error checking logs: {e}")
        return False

def restart_container():
    try:
        # Restart the container
        subprocess.run(
            ["docker", "compose", "up", "--detach", "--force-recreate", container_name],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error restarting container: {e}")

def main():
    # Set the working directory to the script's location
    os.chdir(docker_compose_workspace)

    print(f"Checking Frigate for MQTT disconnection...")

    if not is_mqtt_broker_reachable():
        print(f"- [ERROR] | MQTT broker is unreachable.")
        return 1

    if not is_container_running():
        print(f"- [ERROR] | Container <{container_name}> is not running.")
        return 1

    if not is_error_in_container_logs():
        print(f"- No MQTT disconnection error detected in logs of container.")
    else:
        print(f"- Detected MQTT disconnection in logs of container.")
        print(f"- Restarting container <{container_name}> to fix it...")
        restart_container()
        print(f"- Container <{container_name}> restarted.")

if __name__ == "__main__":
    sys.exit(main())
