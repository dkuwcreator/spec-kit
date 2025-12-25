#!/usr/bin/env bash

# Checklist Item Counter Script (Bash)
#
# This script counts checklist items in all checklist files within a feature directory.
# It provides a safe, reliable alternative to complex inline commands.
#
# Usage: ./count-checklists.sh [OPTIONS]
#
# OPTIONS:
#   --feature-dir <path>  Path to feature directory (default: auto-detect from current branch)
#   --json                Output in JSON format
#   --help, -h            Show help message

set -euo pipefail

show_help() {
    cat <<'EOF'
Usage: count-checklists.sh [OPTIONS]

Count checklist items across all checklist files in a feature directory.

OPTIONS:
  --feature-dir <path>  Path to feature directory (default: auto-detect from current branch)
  --json                Output in JSON format
  --help, -h            Show this help message

EXAMPLES:
  # Count checklists in current feature (auto-detect)
  ./count-checklists.sh

  # Count checklists with JSON output
  ./count-checklists.sh --json

  # Count checklists in specific feature directory
  ./count-checklists.sh --feature-dir "/repo/specs/001-my-feature"

OUTPUT (Text format):
  | Checklist   | Total | Completed | Incomplete | Status |
  |-------------|-------|-----------|------------|--------|
  | ux.md       | 12    | 12        | 0          | ✓ PASS |
  | test.md     | 8     | 5         | 3          | ✗ FAIL |

OUTPUT (JSON format):
  {
    "checklists": [
      {"name": "ux.md", "total": 12, "completed": 12, "incomplete": 0, "status": "PASS"},
      {"name": "test.md", "total": 8, "completed": 5, "incomplete": 3, "status": "FAIL"}
    ],
    "overall_status": "FAIL",
    "total_incomplete": 3
  }

EOF
    exit 0
}

# Parse arguments
FEATURE_DIR=""
JSON_OUTPUT=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --feature-dir)
            FEATURE_DIR="$2"
            shift 2
            ;;
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        --help|-h)
            show_help
            ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Use --help for usage information" >&2
            exit 1
            ;;
    esac
done

# Source common functions if we need to auto-detect feature directory
if [[ -z "$FEATURE_DIR" ]]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    # shellcheck source=common.sh
    source "$SCRIPT_DIR/common.sh"
    FEATURE_DIR="$(get_feature_dir)"
fi

# Check if checklists directory exists
CHECKLISTS_DIR="$FEATURE_DIR/checklists"
if [[ ! -d "$CHECKLISTS_DIR" ]]; then
    if $JSON_OUTPUT; then
        echo '{"checklists":[],"overall_status":"NO_CHECKLISTS","total_incomplete":0}'
    else
        echo "No checklists directory found at: $CHECKLISTS_DIR"
        echo "Status: NO_CHECKLISTS"
    fi
    exit 0
fi

# Get all markdown files in checklists directory
shopt -s nullglob
CHECKLIST_FILES=("$CHECKLISTS_DIR"/*.md)
shopt -u nullglob

if [[ ${#CHECKLIST_FILES[@]} -eq 0 ]]; then
    if $JSON_OUTPUT; then
        echo '{"checklists":[],"overall_status":"NO_CHECKLISTS","total_incomplete":0}'
    else
        echo "No checklist files found in: $CHECKLISTS_DIR"
        echo "Status: NO_CHECKLISTS"
    fi
    exit 0
fi

# Process each checklist file
declare -a RESULTS=()
TOTAL_INCOMPLETE=0

for file in "${CHECKLIST_FILES[@]}"; do
    filename=$(basename "$file")
    
    # Count total items: lines matching "- [ ]" or "- [X]" or "- [x]"
    total_count=$(grep -c -E '^[[:space:]]*- \[([ Xx])\]' "$file" || true)
    
    # Count completed items: lines matching "- [X]" or "- [x]"
    completed_count=$(grep -c -E '^[[:space:]]*- \[[Xx]\]' "$file" || true)
    
    # Calculate incomplete
    incomplete_count=$((total_count - completed_count))
    
    # Determine status
    if [[ $incomplete_count -eq 0 ]]; then
        status="PASS"
    else
        status="FAIL"
    fi
    
    # Add to total incomplete count
    TOTAL_INCOMPLETE=$((TOTAL_INCOMPLETE + incomplete_count))
    
    # Store result
    RESULTS+=("$filename|$total_count|$completed_count|$incomplete_count|$status")
done

# Calculate overall status
if [[ $TOTAL_INCOMPLETE -eq 0 ]]; then
    OVERALL_STATUS="PASS"
else
    OVERALL_STATUS="FAIL"
fi

# Output results
if $JSON_OUTPUT; then
    # JSON output
    echo -n '{"checklists":['
    first=true
    for result in "${RESULTS[@]}"; do
        IFS='|' read -r name total completed incomplete status <<< "$result"
        if ! $first; then
            echo -n ','
        fi
        first=false
        echo -n "{\"name\":\"$name\",\"total\":$total,\"completed\":$completed,\"incomplete\":$incomplete,\"status\":\"$status\"}"
    done
    echo -n "],"
    echo -n "\"overall_status\":\"$OVERALL_STATUS\","
    echo -n "\"total_incomplete\":$TOTAL_INCOMPLETE"
    echo '}'
else
    # Text output - table format
    echo ""
    echo "Checklist Status Summary:"
    echo ""
    
    # Calculate max name width
    max_name_width=10
    for result in "${RESULTS[@]}"; do
        IFS='|' read -r name _ _ _ _ <<< "$result"
        name_len=${#name}
        if [[ $name_len -gt $max_name_width ]]; then
            max_name_width=$name_len
        fi
    done
    name_width=$((max_name_width + 2))
    
    # Header
    separator=$(printf '|%*s|%*s|%*s|%*s|%*s|' $((name_width + 2)) '' 7 '' 11 '' 12 '' 8 '' | tr ' ' '-')
    printf "| %-${name_width}s | %5s | %9s | %10s | %6s |\n" "Checklist" "Total" "Completed" "Incomplete" "Status"
    echo "$separator"
    
    # Data rows
    for result in "${RESULTS[@]}"; do
        IFS='|' read -r name total completed incomplete status <<< "$result"
        if [[ $status == "PASS" ]]; then
            status_icon="✓"
        else
            status_icon="✗"
        fi
        printf "| %-${name_width}s | %5s | %9s | %10s | %s %-4s |\n" "$name" "$total" "$completed" "$incomplete" "$status_icon" "$status"
    done
    
    echo "$separator"
    echo ""
    
    # Overall status
    if [[ $OVERALL_STATUS == "PASS" ]]; then
        echo "Overall Status: ✓ PASS - All checklists complete"
    else
        echo "Overall Status: ✗ FAIL - $TOTAL_INCOMPLETE incomplete item(s) found"
    fi
    echo ""
fi

# Exit with appropriate code
if [[ $OVERALL_STATUS == "PASS" ]]; then
    exit 0
else
    exit 1
fi
