import os
import yaml
from pathlib import Path

# Load the manifest
with open("scribe_manifest.yml", "r") as f:
    manifest = yaml.safe_load(f)

# Apply each update
for update in manifest.get("update", []):
    file_path = Path(update["file"])
    commit_message = update.get("commit_message", "Update via Mirror Scribe")

    if "source" in update:
        source_path = Path(update["source"])
        if source_path.exists():
            content = source_path.read_text()
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
            print(f"Updated file: {file_path}")
        else:
            print(f"Source file not found: {source_path}")

    elif "append_line" in update:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if file_path.exists():
            with open(file_path, "a") as f:
                f.write("\n" + update["append_line"])
        else:
            with open(file_path, "w") as f:
                f.write(update["append_line"])
        print(f"Appended to file: {file_path}")

    else:
        print(f"No recognizable update action for file: {file_path}")
