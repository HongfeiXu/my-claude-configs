#!/bin/bash
# Install skills from this repo to ~/.claude/skills/

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE="$SCRIPT_DIR/skills"
TARGET="$HOME/.claude/skills"

if [ ! -d "$SOURCE" ]; then
    echo "Error: skills directory not found at $SOURCE"
    exit 1
fi

mkdir -p "$TARGET"

echo "Syncing skills from $SOURCE to $TARGET"
echo

# On Windows (Git Bash/MSYS2), use robocopy; otherwise use rsync/cp
if command -v robocopy &>/dev/null; then
    for dir in "$SOURCE"/*/; do
        name=$(basename "$dir")
        echo "  [+] $name"
        MSYS_NO_PATHCONV=1 robocopy "$dir" "$TARGET/$name" /E /MIR /NJH /NJS /NDL /NFL >/dev/null 2>&1
    done
else
    for dir in "$SOURCE"/*/; do
        name=$(basename "$dir")
        echo "  [+] $name"
        rm -rf "$TARGET/$name"
        cp -r "$dir" "$TARGET/$name"
    done
fi

echo
echo "Done. Installed skills:"
for dir in "$TARGET"/*/; do
    echo "  - $(basename "$dir")"
done
