from pathlib import Path

required = [
    ".env",
    ".gitignore",
    "diary.md",
    "dev_log.md",
    "day1_self1.py",
    "outputs/scene01_dalle.png",
]

for item in required:
    path = Path(item)
    print(item, "OK" if path.exists() else "MISSING")