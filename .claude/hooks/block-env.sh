#!/bin/bash
# .claude/hooks/block-env.sh
#
# PreToolUse hook: blocks Claude Code from reading, editing, writing, or
# cat/grep-ing .env files (secrets), while still allowing .env.example,
# .env.sample, .env.template, and similar placeholder files.
#
# Install:
#   1. Copy this file to .claude/hooks/block-env.sh in your project
#      (or ~/.claude/hooks/block-env.sh to apply it to every project).
#   2. chmod +x .claude/hooks/block-env.sh
#   3. Add the hooks config below to your settings.json (project or user).
#
# Requires: jq (brew install jq if you don't have it).

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name // empty')
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# A path/command counts as ".env" if it contains ".env" but is NOT one of
# the common placeholder variants that are safe to read (.env.example etc).
is_env_secret() {
  local target="$1"
  [ -z "$target" ] && return 1
  if echo "$target" | grep -Eq '\.env(\.[a-zA-Z0-9._-]+)?($|[^a-zA-Z0-9._-])'; then
    if echo "$target" | grep -Eiq '\.env\.(example|sample|template|dist)'; then
      return 1
    fi
    return 0
  fi
  return 1
}

blocked=""
if is_env_secret "$file_path"; then
  blocked="file $file_path"
elif is_env_secret "$command"; then
  blocked="command touching $command"
fi

if [ -n "$blocked" ]; then
  jq -n --arg reason "Blocked by block-env.sh: $tool_name tried to touch a .env file ($blocked). .env holds secrets and is off-limits to Claude Code. Ask Naël to paste the specific value if it's actually needed." \
    '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "deny", permissionDecisionReason: $reason}}'
  exit 2
fi

exit 0
