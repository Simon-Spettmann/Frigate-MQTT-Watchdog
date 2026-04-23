# Frigate MQTT Watchdog

A lightweight Python script to monitor and automatically fix Frigate's MQTT connection in Docker Compose setups by restarting the container if a disconnection is detected. It checks if the MQTT broker is reachable and the container is running before acting, and searches the Frigate MQTT module logs (`frigate.comms.mqtt`) with pattern matching to detect disconnections.

## Requirements

This script is intended for Docker Compose setups and requires:

- Python 3.7+
- [paho-mqtt](https://pypi.org/project/paho-mqtt/) (installed via `requirements.txt`)

**Note:** The log level of `frigate.comms.mqtt` must be set to `debug` in the Frigate configuration:

```yml
logger:
  # module by module log level configuration
  logs:
    frigate.comms.mqtt: debug
```

## Installation

Clone this repository:

```bash
git clone "https://github.com/Simon-Spettmann/Frigate-MQTT-Watchdog"
```

Change into the repository directory:

```bash
cd "Frigate-MQTT-Watchdog"
```

Set up a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Set the following configuration variables in the Python script (`frigate_mqtt_watchdog.py`):

```python
docker_compose_workspace = "/path/to/docker-compose-workspace"
mqtt_host = "homeassistant"
mqtt_port = 1883
container_name = "frigate"
```

## Usage

Set up a cronjob for continuous monitoring (e.g. every 5 minutes):

```text
*/5 * * * * /path/to/.venv/bin/python /path/to/frigate_mqtt_watchdog.py
```
