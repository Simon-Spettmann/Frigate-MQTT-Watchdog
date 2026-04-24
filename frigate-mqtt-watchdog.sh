#!/usr/bin/env bash

# Configuration
HA_URL="https://my.home-assistant.io"
HA_TOKEN="YOUR_LONG_LIVED_ACCESS_TOKEN"

FRIGATE_STATUS_ENTITY_ID="sensor.frigate_status"
CAMERA_ENTITY_ID="camera.<some-frigate-camera-id>"

DOCKER_COMPOSE_WORKSPACE="/path/to/docker-compose-workspace"
CONTAINER_NAME="frigate"

# Function to check if Frigate status is running
is_frigate_running() {
    local response

    response=$(curl -s -X GET \
        -H "Authorization: Bearer $HA_TOKEN" \
        -H "Content-Type: application/json" \
        "$HA_URL/api/states/$FRIGATE_STATUS_ENTITY_ID" \
        | jq -r ".state")

    if [[ "$response" == "running" ]]; then
        return 0
    fi

    if [[ "$response" == "unavailable" ]]; then
        return 1
    fi

    # Unknown response
    return 1
}

# Function to check if the camera is available
is_camera_recording() {
    local response

    response=$(curl -s -X GET \
        -H "Authorization: Bearer $HA_TOKEN" \
        -H "Content-Type: application/json" \
        "$HA_URL/api/states/$CAMERA_ENTITY_ID" \
        | jq -r ".state")

    if [[ "$response" == "recording" ]]; then
        return 0
    fi

    if [[ "$response" == "unavailable" ]]; then
        return 1
    fi

    # Unknown response
    return 1
}

# Function to restart the container
restart_container() {
    cd "$DOCKER_COMPOSE_WORKSPACE" || exit 1
    docker compose restart "$CONTAINER_NAME"
}

# Main logic
main() {
    echo "Checking Home Assistant for Frigate MQTT disconnection..."

    if ! is_frigate_running; then
        echo "- [ERROR] | Frigate is not running."
        return 1
    fi

    if ! is_camera_recording; then
        echo "- MQTT disconnection detected: Frigate camera does not have state recording"

        echo "Restarting container $CONTAINER_NAME to fix..."
        restart_container
        echo "Container $CONTAINER_NAME restarted."
    fi

    echo "- No MQTT disconnection detected."
}

main "$@"
