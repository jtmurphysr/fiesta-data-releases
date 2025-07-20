#!/bin/bash

OLD_NAME="$1"
NEW_NAME="$2"
FILE="fiesta_with_prior_shapes.json"
TMP_FILE="updated_file.json"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${FILE%.json}_backup_${TIMESTAMP}.json"

if [ -z "$OLD_NAME" ] || [ -z "$NEW_NAME" ]; then
  echo "Usage: $0 <old_name> <new_name>"
  exit 1
fi

# Create a backup
cp "$FILE" "$BACKUP_FILE"
echo "🔒 Backup saved to: $BACKUP_FILE"

# Process and apply rename
jq --arg old "$OLD_NAME" --arg new "$NEW_NAME" '
  map(
    if .shape == $old then
      .shape = $new |
      .prior_shapes = (if .prior_shapes then (.prior_shapes + [$old] | unique) else [$old] end)
    else
      .
    end
  )
' "$FILE" > "$TMP_FILE" && mv "$TMP_FILE" "$FILE"

echo "✅ Shape renamed and prior_shapes updated in: $FILE"
