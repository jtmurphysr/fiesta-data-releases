#!/bin/zsh

# === Config ===
DATA_FILE="fiesta_merged_with_categories.json"
TEMP_FILE="temp.json"
# BACKUP_FILE="${DATA_FILE}.bak"  # Optional backup

# === Inputs ===
OLD_NAME="$1"
NEW_NAME="$2"

# === Input Validation ===
if [[ -z "$OLD_NAME" || -z "$NEW_NAME" ]]; then
  echo "Usage: $0 'Old Shape Name' 'New Shape Name'"
  echo "Example: $0 'Planter & Saucer' 'Flower Pot with Base'"
  exit 1
fi

# === Debug ===
echo "🔄 Changing shape name:"
echo "   FROM: $OLD_NAME"
echo "   TO:   $NEW_NAME"
echo ""

# === Optional: Back up the original file
cp "$DATA_FILE" "$BACKUP_FILE" && echo "📦 Backup saved to $BACKUP_FILE"

# === Perform the Update
jq --arg old "$OLD_NAME" --arg new "$NEW_NAME" \
  'map(if .shape == $old then .shape |= $new else . end)' \
  "$DATA_FILE" > "$TEMP_FILE" && mv "$TEMP_FILE" "$DATA_FILE"

if [[ $? -eq 0 ]]; then
  echo "✅ Update complete."
else
  echo "❌ Update failed. File not modified."
fi
