#!/usr/bin/env bash
set -euo pipefail
source_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
[[ "${PREFIX:-}" == /data/data/com.termux/files/usr ]] || {
    echo 'Run this installer in native Termux, outside Debian.' >&2
    exit 1
}
for tool in proot-distro curl flock termux-open-url; do
    command -v "$tool" >/dev/null || {
        echo "Missing $tool. See INSTALL-STARTUP.md; this installer does not change packages." >&2
        exit 1
    }
done
mkdir -p "$HOME/.shortcuts"
chmod 700 "$HOME/.shortcuts"
target="$HOME/.shortcuts/OSINT Sentinel"
if [[ -e "$target" ]]; then
    backup_dir="$HOME/.cache/osint-sentinel/backups"
    mkdir -p "$backup_dir"
    cp -p -- "$target" "$backup_dir/OSINT-Sentinel-$(date +%Y%m%d-%H%M%S)-$$"
fi
install -m 700 "$source_dir/start-osint-sentinel" "$target"
echo 'Installed OSINT Sentinel. Add or refresh the Termux:Widget home-screen widget.'
