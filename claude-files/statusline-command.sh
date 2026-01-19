#!/bin/bash

# Read JSON input from stdin
input=$(cat)

# Extract values from JSON
current_dir=$(echo "$input" | jq -r '.workspace.current_dir')
model_name=$(echo "$input" | jq -r '.model.display_name')
style_name=$(echo "$input" | jq -r '.output_style.name')
version=$(echo "$input" | jq -r '.version')

# Extract token/context window data
context_size=$(echo "$input" | jq -r '.context_window.context_window_size // 0')
current_usage=$(echo "$input" | jq '.context_window.current_usage')

# Calculate context percentage from current_usage
if [ "$current_usage" != "null" ] && [ "$context_size" -gt 0 ]; then
    current_tokens=$(echo "$current_usage" | jq '(.input_tokens // 0) + (.cache_creation_input_tokens // 0) + (.cache_read_input_tokens // 0)')
    context_percent=$((current_tokens * 100 / context_size))
else
    current_tokens=0
    context_percent=0
fi

# Generate progress bar (10 blocks total)
bar_length=10
filled=$((context_percent * bar_length / 100))
empty=$((bar_length - filled))
progress_bar=""
for ((i=0; i<filled; i++)); do
    progress_bar="${progress_bar}█"
done
for ((i=0; i<empty; i++)); do
    progress_bar="${progress_bar}░"
done

# Get username and hostname
username=$(whoami)
hostname=$(hostname -s)

# Get git branch and check for uncommitted changes
cd "$current_dir" 2>/dev/null
git_info=""
if git rev-parse --git-dir > /dev/null 2>&1; then
    branch=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null)
    if [ -n "$branch" ]; then
        # Check for uncommitted changes
        if ! git diff-index --quiet HEAD -- 2>/dev/null; then
            git_info=" $(printf '\033[35m') $branch*$(printf '\033[0m')"
        else
            git_info=" $(printf '\033[35m') $branch$(printf '\033[0m')"
        fi
    fi
fi

# Get current date/time
current_date=$(date '+%H:%M')

# Build status line with colors
# Green for username@hostname, cyan for directory, magenta for git, default for model/style
printf '\033[32m'
printf '%s@%s' "$username" "$hostname"
printf '\033[0m'
printf ' '
printf '\033[36m'
printf '%s' "$current_dir"
printf '\033[0m'
printf '%s' "$git_info"
printf ' '
printf '\033[33m'
printf ' %s' "$current_date"
printf '\033[0m'
printf '\n'
printf '[%s]' "$model_name"
printf ' '
printf '\033[90m'
printf 'v%s' "$version"
printf '\033[0m'
printf ' '

# Format token counts with K suffix if over 1000
if [ "$current_tokens" -gt 999 ]; then
    token_display="$((current_tokens / 1000))K"
else
    token_display="$current_tokens"
fi
if [ "$context_size" -gt 999 ]; then
    size_display="$((context_size / 1000))K"
else
    size_display="$context_size"
fi

# Display tokens and progress bar
printf '\033[90m'
printf 'Tokens: %s/%s' "$token_display" "$size_display"
printf '\033[0m'
printf ' '

# Color code progress bar: green < 50%, yellow 50-80%, red > 80%
if [ "$context_percent" -lt 50 ]; then
    printf '\033[32m'
elif [ "$context_percent" -lt 80 ]; then
    printf '\033[33m'
else
    printf '\033[31m'
fi
printf '[%s] %d%%' "$progress_bar" "$context_percent"
printf '\033[0m'
