#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: ./install.sh [--copy|--symlink] [--force] [--target DIR]

Options:
  --copy        Copy the skill into the target skills directory. Default.
  --symlink     Symlink the skill for local development.
  --force       Move an existing installed hipdok-club skill to a backup path.
  --target DIR  Install into DIR instead of ${CODEX_HOME:-$HOME/.codex}/skills.
USAGE
}

mode="copy"
force="0"
target_root="${CODEX_HOME:-$HOME/.codex}/skills"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --copy)
      mode="copy"
      ;;
    --symlink)
      mode="symlink"
      ;;
    --force)
      force="1"
      ;;
    --target)
      shift
      if [ "$#" -eq 0 ]; then
        echo "--target requires a directory" >&2
        exit 2
      fi
      target_root="$1"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_dir="$repo_root/skills/hipdok-club"
target_dir="$target_root/hipdok-club"

if [ ! -f "$source_dir/SKILL.md" ]; then
  echo "Missing skill source: $source_dir/SKILL.md" >&2
  exit 1
fi

mkdir -p "$target_root"

if [ -e "$target_dir" ] || [ -L "$target_dir" ]; then
  if [ -L "$target_dir" ] && [ "$(readlink "$target_dir")" = "$source_dir" ]; then
    echo "hipdok-club skill is already installed at $target_dir"
    exit 0
  fi
  if [ "$force" != "1" ]; then
    echo "Skill already exists at $target_dir. Re-run with --force to back it up and replace it." >&2
    exit 1
  fi
  backup_dir="$target_dir.backup.$(date +%Y%m%d%H%M%S)"
  mv "$target_dir" "$backup_dir"
  echo "Moved existing install to $backup_dir"
fi

if [ "$mode" = "symlink" ]; then
  ln -s "$source_dir" "$target_dir"
else
  mkdir -p "$target_dir"
  cp -R "$source_dir/." "$target_dir/"
fi

echo "Installed hipdok-club skill to $target_dir"
