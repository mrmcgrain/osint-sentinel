# OSINT Sentinel

A local-first OSINT dashboard for Samsung and other Android phones, powered by Termux, Debian proot, and Python.

**This is an early working build, and much more is coming soon.** We are building a practical investigation workspace that can start with one tap from your phone’s home screen.

## Built on the work of others

Thank you to **Siddharth Dushantha, the Sherlock Project contributors, soxoj and the Maigret contributors, the Termux team, and the maintainers of PRoot-Distro, PRoot, Debian, Python, pipx, and the supporting utilities**. Their work makes this project possible. Sentinel provides the dashboard and integration; the upstream authors deserve credit for their tools and research logic.

See [credits and third-party notices](THIRD-PARTY-NOTICES.md) for project links, licenses, and how each component is used. This is an independent project with no implied upstream endorsement.

## What we built

We started with a browser dashboard running inside Debian and added the pieces needed to make it usable on a phone:

- **One-tap startup:** a Termux:Widget script opens the existing Debian environment, starts `python3 ~/osint-sentinel/server.py`, waits for the server to respond, and opens the dashboard.
- **Repeat-tap handling:** tapping again opens the running dashboard without launching another server. Startup errors stay visible in Termux.
- **Username research:** run Sherlock and Maigret from the dashboard. Sherlock includes adult sites and displays all reported results by default, with an option to hide misses.
- **Search transparency:** completed Sherlock reports show possible matches, misses, blocked/error results, and username-rule skips. Known unreliable sites excluded by Sherlock stay excluded. Timed-out searches are labeled incomplete.
- **Saved output:** Sherlock exports CSV and text; Maigret produces HTML reports in the Debian application data folder.
- **Case workspace:** save investigation notes, indicators, and local images; export saved case records as JSON.
- **Image research handoffs:** open Google Lens, Bing Visual Search, TinEye, or Yandex to submit an image manually. Automated reverse-image results are not implemented.
- **Tool Store:** install, update, or remove Sherlock and Maigret through pipx.
- **Portable installer:** one self-contained script installs the missing Termux prerequisites, Debian when absent, Sentinel, the search tools, and the startup script.

The dashboard lives at **http://127.0.0.1:8765/**. A browser bookmark alone cannot launch a stopped server; the Termux:Widget entry handles startup.

## Install on a phone

1. Install and open **Termux** once. Install **Termux:Widget** from a compatible signing source. Keep existing Termux installations rather than uninstalling or downgrading them. See the [official Widget installation instructions](https://github.com/termux/termux-widget#installation).
2. Download [`install-osint-sentinel.sh`](install-osint-sentinel.sh) into the phone’s **Downloads** folder. Use GitHub’s download/raw-file control to save the actual script, not the HTML page. The script already contains the application; no ZIP extraction is needed.
3. In **native Termux**, outside Debian, run:

```bash
bash /sdcard/Download/install-osint-sentinel.sh
```

If Downloads access is denied, run `termux-setup-storage`, grant access, and retry.

4. Long-press an empty home-screen area → **Widgets → Termux:Widget**. Add it, refresh its list, and tap **OSINT Sentinel**.

Keep the Termux session running while using the app. Internet is required for setup, tool installation, and online searches. Allow several GB of free storage for Debian, tools, downloads, and future reports. Android APK approval and widget placement still require manual steps.

[Detailed installation and recovery instructions](osint-sentinel/INSTALL-OTHER-PHONES.md)

## Existing installations

The complete installer reuses a working default `debian` environment and backs up existing Sentinel code. It stops if an existing Debian cannot start, rather than resetting it. It installs or updates shared Debian system dependencies and leaves existing Sherlock/Maigret installations in place when their commands already exist.

For a smaller code-only update, follow [the startup update instructions](osint-sentinel/INSTALL-STARTUP.md). Those instructions use the separate `osint-sentinel-startup.zip` package.

The installers do not install or edit SpiderFoot. They do not reinstall existing Debian or downgrade Termux. Standard Termux paths and the default Debian login user are assumed; custom layouts may need adaptation.

Stop an older Sentinel session with **Ctrl+C** before launching updated code. Do not stop unrelated services.

## Data and interpretation

Application data is stored inside Debian at `~/osint-sentinel/data/`. Search tools contact external websites. Image providers receive pictures only when you submit them there. The local server binds to loopback and uses a per-start browser token for protected API actions.

Username matches are leads, not identity verification. False positives, blocked requests, and missing results are possible. Site coverage changes with Sherlock’s upstream list. No automatic identity conclusions or scam scores are provided.

## Project files

| Path | Purpose |
| --- | --- |
| `osint-sentinel/server.py` | Local Python server and tool jobs |
| `osint-sentinel/index.html` | Phone-friendly dashboard |
| `osint-sentinel/start-osint-sentinel` | Foreground Termux:Widget launcher |
| `osint-sentinel/install-all-termux.sh` | Readable full installation source |
| `osint-sentinel/install-startup-termux.sh` | Installs the widget script only |
| `install-osint-sentinel.sh` | Generated self-contained installer |
| `osint-sentinel-complete.zip` | Installer and application sources |
| `build-installer.py` | Rebuilds the full installer and complete ZIP |
| `COMPLETE-SHA256SUMS` | Checksums for the complete distribution |

No case data, uploaded images, credentials, or phone backups are included in this repository.

## Validation so far

Bash/Python/JavaScript syntax checks passed. Local integration checks covered server readiness, dashboard opening, repeat taps without duplicate servers, API token enforcement, and Sherlock status-count parsing. Installer simulations covered fresh Debian, existing Debian, and refusing to replace a broken existing environment. The code update and startup script were installed on the connected Samsung; the complete installer’s help mode was checked there.

A complete fresh installation on a second phone and end-to-end widget startup across different Android devices still need validation. Package downloads and dependency builds can fail; setup stops with the error and can be rerun after resolving it.

## Much more coming soon

This is the foundation. Planned areas to explore include:

- Live search progress and clearer result browsing.
- Site filters and configurable search coverage.
- Richer case reports and export options.
- More curated OSINT integrations.
- Easier installation, updates, and troubleshooting.
- Broader testing across Samsung and other Android phones.

These are roadmap ideas, not features available today or delivery commitments. **Much more is coming soon—OSINT Sentinel is just getting started.**

## Rebuild the installer

On a development machine with Python 3:

```bash
python3 build-installer.py
```

This regenerates the bundled script, complete ZIP, and complete-package checksums from `osint-sentinel/`. Do not hand-edit the embedded payload. Third-party tools retain their own licenses and are downloaded during installation, not bundled here.
