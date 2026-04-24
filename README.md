# Frigate MQTT Watchdog

A lightweight Bash script to monitor and automatically fix Frigate’s MQTT connection to Home Assistant by checking the states of the Frigate status entity and a given camera via the Home Assistant API. If a disconnection is detected it will restart the container. Intended for Docker Compose setups.

## Requirements

This script is intended for Docker Compose setups and requires:

- `curl` (for API calls)
- `jq` (for JSON parsing)
- `docker compose` (for container management)

You will also need a [Long-Lived Access Token](https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token) for your Home Assistant Instance:

- Go to [https://my.home-assistant.io/redirect/profile](https://my.home-assistant.io/redirect/profile)
- Switch to the tab "Security"
- Scroll down to "Long-lived access tokens"
- Create a long-lived access token

## Installation

Clone this repository:

```bash
git clone "https://github.com/Simon-Spettmann/Frigate-MQTT-Watchdog"
```

Change into the repository directory:

```bash
cd Frigate-MQTT-Watchdog
```

## Configuration

Edit the script to set your configuration variables:

```bash
HA_URL="https://my.home-assistant.io"
HA_TOKEN="YOUR_LONG_LIVED_ACCESS_TOKEN"

FRIGATE_STATUS_ENTITY_ID="sensor.frigate_status"
CAMERA_ENTITY_ID="camera.<some-frigate-camera-id>"

DOCKER_COMPOSE_WORKSPACE="/path/to/docker-compose-workspace"
CONTAINER_NAME="frigate"
```

## Usage

Set up a cronjob for continuous monitoring (e.g. every 5 minutes):

```bash
*/5 * * * * /path/to/frigate-mqtt-watchdog.sh
```
