#!/bin/bash

# === Config ===
DATA_FILE="fiesta_merged_with_categories.json"

# === Inputs ===
NAME="$1"

# === Debug (optional) ===
echo "Finding '$NAME'"

# === Update Name ===
jq --arg name $NAME '[.[] | select(.shape == $name)]' $DATA_FILE
