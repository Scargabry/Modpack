import json
import os
import stat
import traceback
from urllib.parse import quote

FOLDERS = ["mods", "resourcepacks", "shaderpacks"]
OUTPUT_FILE = "sync.json"

TYPE_MAP = {
    "mods": "mod",
    "resourcepacks": "resourcepack",
    "shaderpacks": "shaderpack",
}

try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    entries = []
    for folder in FOLDERS:
        if not os.path.isdir(folder):
            continue
        index = 1
        for filename in sorted(os.listdir(folder), key=str.lower):
            filepath = os.path.join(folder, filename)
            if not os.path.isfile(filepath) or filename.startswith("."):
                continue
            rel_path = f"{folder}/{filename}"
            encoded_path = "/".join(quote(part) for part in rel_path.split("/"))
            entries.append({
                "url": f"https://raw.githubusercontent.com/Scargabry/Modpack/main/{encoded_path}",
                "name": os.path.splitext(filename)[0],
                "version": f"1.0.1-{index:03d}",
                "type": TYPE_MAP[folder],
            })
            index += 1

    manifest = {
        "sync_version": 3,
        "sync": entries,
    }

    if os.path.exists(OUTPUT_FILE):
        os.chmod(OUTPUT_FILE, stat.S_IWRITE)

    tmp_file = OUTPUT_FILE + ".tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    os.replace(tmp_file, OUTPUT_FILE)
    print(f"Updated {OUTPUT_FILE} with {len(entries)} files.")
except Exception:
    traceback.print_exc()

input("Press Enter to close...")