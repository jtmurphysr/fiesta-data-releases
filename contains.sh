#!/bin/zsh

# Usage: ./search_fiesta.sh <shape|color|category> <search_term>
# Examples:
#   ./search_fiesta.sh shape platter
#   ./search_fiesta.sh color turquoise
#   ./search_fiesta.sh category Bowls

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <shape|color|category> <search_term>"
  exit 1
fi

field="$1"
term="$2"

if [[ "$field" != "shape" && "$field" != "color" && "$field" != "category" ]]; then
  echo "Error: First argument must be 'shape', 'color', or 'category'"
  exit 2
fi

FILE="fiesta_merged_with_categories.json"

# Main logic
if [[ "$field" == "category" ]]; then
  jq --arg term "$term" '
    map(select(.category | ascii_downcase == ($term | ascii_downcase)))
    | map(.shape)
    | unique
    | .[]
  ' "$FILE"
else
  jq --arg field "$field" --arg term "$term" '
    map(select(.[$field] | ascii_downcase | contains($term | ascii_downcase)))
    | map(.shape)
    | unique
    | .[]
  ' "$FILE"
fi
