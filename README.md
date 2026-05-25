# Hipdok Club Skill

Codex skill for operating Seoul Outdoor Library Hipdok Club in Safari through `agent-safari`.

The skill supports common Hipdok Club requests such as attendance, book registration, reading records, completion certification checks, transcription certification, activity review eligibility, and mileage/status lookup.

## Install

### Prompt install

In Codex, ask:

```text
Use $skill-installer to install the skill from https://github.com/handlecusion/hipdok-skill/tree/main/skills/hipdok-club
```

Or in Korean:

```text
https://github.com/handlecusion/hipdok-skill/tree/main/skills/hipdok-club 에 있는 Codex skill 설치해줘.
```

Restart Codex after installation so the new skill is discovered.

### Manual install

Clone the repo and run the installer:

```bash
git clone https://github.com/handlecusion/hipdok-skill.git
cd hipdok-skill
./install.sh
```

For local development, install as a symlink:

```bash
./install.sh --symlink --force
```

The installer copies the skill to `${CODEX_HOME:-$HOME/.codex}/skills/hipdok-club`.

## Dependencies

- macOS with Safari.
- `agent-safari` CLI/MCP available to Codex.
- A Seoul Outdoor Library Hipdok Club account.
- A browser session that can complete Naver login when the site requires authentication.

The skill does not store credentials, cookies, or browser sessions.

## Usage

Example prompts:

```text
Use $hipdok-club to complete today's attendance.
Use $hipdok-club to record Zero to One as read through page 70 today.
Use $hipdok-club to check my mileage and next grade requirements.
```

## Validate

```bash
python -m pip install pyyaml
python scripts/validate_skill.py skills/hipdok-club
```
