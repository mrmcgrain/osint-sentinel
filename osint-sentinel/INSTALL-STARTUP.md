# Samsung one-tap startup update

This update uses your existing `proot-distro login debian` environment and its default user's home. It does not install Debian, replace Termux, run the dependency installer, or touch SpiderFoot. Start from native Termux, outside Debian (`exit` first if needed).

## Apply this update once

The update ZIP is named `osint-sentinel-startup.zip`. Put it in Samsung Downloads. If Termux already has storage access, no storage setup is needed; otherwise run `termux-setup-storage` and grant access.

```sh
mkdir -p ~/sentinel-startup-update
unzip -o ~/storage/downloads/osint-sentinel-startup.zip -d ~/sentinel-startup-update
cd ~/sentinel-startup-update/osint-sentinel
```

If commands are missing, install only the missing native Termux prerequisites: `pkg install unzip curl util-linux`. `flock` comes from util-linux. The existing proot-distro and Debian are required; do not reinstall them.

Copy the application update into your existing Debian home (backs up application code; preserves all data and installed tools):

```sh
proot-distro login debian -- bash -lc '
set -euo pipefail
src=/data/data/com.termux/files/home/sentinel-startup-update/osint-sentinel
test -f "$HOME/osint-sentinel/server.py" || { echo "Existing Sentinel not found in this Debian user home"; exit 1; }
backup_dir="$HOME/osint-sentinel/backups/$(date +%Y%m%d-%H%M%S)-$$"
mkdir -p "$backup_dir"
cp -p "$HOME/osint-sentinel/server.py" "$HOME/osint-sentinel/index.html" "$backup_dir/"
cp "$src/server.py" "$src/index.html" "$HOME/osint-sentinel/"
'
bash install-startup-termux.sh
```

If you normally log in using a different Debian user, add the same `--user USER` option to both the update command and `proot-distro login debian` in `start-osint-sentinel` before installing the shortcut. The `~` path is resolved inside Debian, never in native Termux.

Stop any old Sentinel server using Ctrl+C in its Termux session once after updating, so the new health check is active. Do not stop SpiderFoot.

## Put the one-tap control on Samsung Home

Termux:Widget is already installed on the inspected phone. If installing on another phone, use a Termux:Widget build compatible with the existing Termux signing source; see https://github.com/termux/termux-widget#installation. Do not uninstall, downgrade, or replace Termux to resolve a plugin mismatch.

1. Long-press an empty area of the Samsung home screen and choose **Widgets**.
2. Find **Termux:Widget**, drag its widget onto Home, and tap its refresh button.
3. Tap **OSINT Sentinel** in that widget. This is the one-tap startup control. It opens a Termux session, enters existing Debian, runs `python3 ~/osint-sentinel/server.py`, waits for readiness, and opens http://127.0.0.1:8765/.
4. If your widget offers a single-script shortcut picker, select **OSINT Sentinel** for a standalone shortcut. The list widget works without this optional feature.

Keep the Termux session running while using the app. Tap again to reopen a running dashboard; concurrent taps do not launch duplicate servers. Ctrl+C in the Sentinel session stops it. A Chrome Add to Home screen bookmark alone cannot start an offline server. Startup and local reports work without internet; online searches and package installation still need it.

On Samsung, if Android stops Termux while the screen is off, set Settings → Apps → Termux → Battery → Unrestricted, and exclude Termux from Sleeping/Deep sleeping apps if those options are present. Android can still terminate processes; tap the widget to start again.

## Troubleshooting / undo

- Missing server: confirm the application exists in the default Debian user's `~/osint-sentinel`. The shortcut never installs a new environment.
- Startup error: read the visible Termux output. Port 8765 must be free or serve the updated Sentinel. Other services are never killed by this launcher.
- Widget entry missing: refresh it; confirm `~/.shortcuts/OSINT Sentinel` exists in native Termux with permission 700. Do not run the shortcut from Downloads.
- To remove startup integration: delete only `~/.shortcuts/OSINT Sentinel` and remove the widget. Prior shortcut backups are in native Termux `~/.cache/osint-sentinel/backups/`.
- To roll back application code: stop Sentinel and copy `server.py` and `index.html` from the desired Debian `~/osint-sentinel/backups/` folder back into `~/osint-sentinel/`. Leave `data/` intact.
