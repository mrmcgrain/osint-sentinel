#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == --help ]]; then
    echo 'Usage: bash install-all-termux.sh'
    echo 'Run in native Termux. Installs missing prerequisites, Debian if absent, Sentinel, Sherlock and Maigret.'
    exit 0
fi
[[ $# == 0 ]] || { echo 'Unknown option. Use --help.' >&2; exit 1; }
[[ "${PREFIX:-}" == /data/data/com.termux/files/usr && "$HOME" == /data/data/com.termux/files/home ]] || {
    echo 'Open native Termux (outside Debian) and run this script there.' >&2
    exit 1
}
source_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
for name in server.py index.html start-osint-sentinel install-startup-termux.sh; do
    [[ -f "$source_dir/$name" ]] || { echo "Missing bundled file: $name" >&2; exit 1; }
done
trap 'echo "Setup stopped at line $LINENO. Fix the error above, then rerun the same script. Existing data is retained." >&2' ERR
# Install only missing host commands; do not replace an existing proot-distro.
packages=()
command -v proot-distro >/dev/null || packages+=(proot-distro)
command -v curl >/dev/null || packages+=(curl)
command -v flock >/dev/null || packages+=(util-linux)
if (( ${#packages[@]} )); then
    pkg update -y
    pkg install -y "${packages[@]}"
fi
mkdir -p "$HOME/.cache/osint-sentinel"
exec 8>"$HOME/.cache/osint-sentinel/setup.lock"
flock -n 8 || { echo 'Another Sentinel setup is running.' >&2; exit 1; }
if proot-distro login debian -- /bin/true; then
    echo 'Reusing existing Debian.'
else
    runtime_dir="$PREFIX/var/lib/proot-distro"
    if [[ -e "$runtime_dir/containers/debian" || -e "$runtime_dir/installed-rootfs/debian" ]]; then
        echo 'Existing Debian could not start. Repair its login before rerunning; setup will not reinstall it.' >&2
        exit 1
    fi
    echo 'Installing Debian for this phone...'
    proot-distro install debian
    proot-distro login debian -- /bin/true
fi
# Pass the bundle through stdin so Debian need not expose Termux home mounts.
# A Debian-side lock prevents simultaneous application updates.
tar -C "$source_dir" -cf - server.py index.html | proot-distro login debian -- bash -lc '
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
mkdir -p "$HOME/osint-sentinel"
stage_dir=$(mktemp -d)
trap '\''rm -rf -- "$stage_dir"'\'' EXIT
tar -xf - -C "$stage_dir"
apt-get update
apt-get install -y python3 python3-venv python3-pip pipx ca-certificates util-linux
exec 7>"$HOME/osint-sentinel/.setup.lock"
flock -n 7 || { echo "Another Debian Sentinel setup is running" >&2; exit 1; }
backup_dir="$HOME/osint-sentinel/backups/setup-$(date +%Y%m%d-%H%M%S)-$$"
for name in server.py index.html; do
    if [[ -f "$HOME/osint-sentinel/$name" ]]; then
        mkdir -p "$backup_dir"
        cp -p "$HOME/osint-sentinel/$name" "$backup_dir/"
    fi
done
cp "$stage_dir/server.py" "$stage_dir/index.html" "$HOME/osint-sentinel/"
mkdir -p "$HOME/osint-sentinel/data/images" "$HOME/osint-sentinel/data/cases"
python3 -m py_compile "$HOME/osint-sentinel/server.py"
export PATH="$HOME/.local/bin:$PATH"
if ! command -v sherlock >/dev/null; then pipx install sherlock-project; fi
if ! command -v maigret >/dev/null; then pipx install maigret; fi
sherlock --version
maigret --help >/dev/null
# Verify flags used by Sentinel are supported by an existing Sherlock.
sherlock_help=$(sherlock --help)
for flag in --nsfw --print-all --csv --txt --folderoutput; do
    [[ "$sherlock_help" == *"$flag"* ]] || {
        echo "Existing Sherlock lacks $flag; update it from Sentinel Tool Store, then rerun setup." >&2
        exit 1
    }
done
echo "Debian application and search tools ready."
'
bash "$source_dir/install-startup-termux.sh"
cat <<'MESSAGE'

Sentinel setup finished. Adult-site searches are enabled.
If an older Sentinel session is running, stop only that session with Ctrl+C.

ONE-TAP STARTUP:
1. Install Termux:Widget from the SAME signing source as your existing Termux.
   Official instructions: https://github.com/termux/termux-widget#installation
   Keep your existing Termux; do not uninstall or downgrade it.
2. On Samsung Home: long-press empty space > Widgets > Termux:Widget.
3. Add the widget, refresh it, then tap OSINT Sentinel.

The widget starts Debian and Sentinel and opens http://127.0.0.1:8765/.
You may also start now with: bash "$HOME/.shortcuts/OSINT Sentinel"
Keep Termux running. Online searches require internet.
MESSAGE
