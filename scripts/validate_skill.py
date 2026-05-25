#!/usr/bin/env python3
import sys
from pathlib import Path

import yaml


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path} must start with YAML frontmatter")
    try:
        _, frontmatter, body = text.split("---\n", 2)
    except ValueError:
        fail(f"{path} has invalid YAML frontmatter delimiters")
    data = yaml.safe_load(frontmatter) or {}
    if not isinstance(data, dict):
        fail(f"{path} frontmatter must be a mapping")
    return data, body


def require_nonempty_mapping_value(mapping: dict, key: str, owner: str) -> None:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(f"{owner} must define non-empty string field {key!r}")


def main() -> None:
    skill_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "skills/hipdok-club")
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        fail(f"missing {skill_md}")

    metadata, body = load_frontmatter(skill_md)
    require_nonempty_mapping_value(metadata, "name", str(skill_md))
    require_nonempty_mapping_value(metadata, "description", str(skill_md))
    if metadata["name"] != skill_dir.name:
        fail(f"{skill_md} name must match directory name {skill_dir.name!r}")
    if "references/" not in body:
        fail(f"{skill_md} should point to reference files for progressive disclosure")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.is_file():
        fail(f"missing {openai_yaml}")
    agent_data = yaml.safe_load(openai_yaml.read_text(encoding="utf-8")) or {}
    interface = agent_data.get("interface")
    if not isinstance(interface, dict):
        fail(f"{openai_yaml} must define interface mapping")
    for key in ("display_name", "short_description", "default_prompt"):
        require_nonempty_mapping_value(interface, key, str(openai_yaml))

    for relpath in ("references/hipdok-workflows.md", "references/use-cases.md"):
        path = skill_dir / relpath
        if not path.is_file():
            fail(f"missing {path}")
        if not path.read_text(encoding="utf-8").strip():
            fail(f"{path} is empty")

    print(f"Skill is valid: {skill_dir}")


if __name__ == "__main__":
    main()

