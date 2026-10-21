# Install on another phone

Use the single file `install-osint-sentinel.sh`. The ZIP is optional for source review; the script already contains the full application. It contains no cases, photos, credentials, Debian filesystem, or personal files.

1. Install Termux on the phone and open it once. Install a compatible Termux:Widget from the same signing source. Follow https://github.com/termux/termux-widget#installation. On an existing phone keep its Termux installation and data.
2. Copy `install-osint-sentinel.sh` to the phone's Downloads folder.
3. In native Termux run:

```sh
bash /sdcard/Download/install-osint-sentinel.sh
```

If Android denies access to Downloads, run `termux-setup-storage`, grant the requested permission, then run the command again.

Setup downloads packages from Termux, Debian and PyPI. Use a reliable internet connection and allow several GB of free storage for Debian, tools, downloads and future reports. Installation duration depends on the phone and network. A package failure stops setup visibly; fix the error and rerun the same command. Existing Debian is reused, not reset. Existing app code is backed up. Existing Sherlock/Maigret are retained and validated; missing tools install through pipx. No SpiderFoot files or environments are edited. Debian's shared Python/system dependencies may be installed or updated by apt; this is a full setup script, unlike the code-only update ZIP.

4. Long-press an empty home-screen area → Widgets → Termux:Widget. Add it, tap Refresh, then tap **OSINT Sentinel**.

Android app installation approval and home-screen placement are manual. The script installs the widget's startup script, not the Android APK. It does not root the phone, downgrade Termux, or install SpiderFoot. It uses standard Termux paths and the default `debian` login user. Custom proot runtime locations or nonstandard Termux package IDs need adaptation.

Adult-site checks and all Sherlock results are enabled. Searches require internet; local report storage stays on the phone. Keep the Sentinel Termux session running. To stop Sentinel, press Ctrl+C in that session. Existing running Sentinel code must be restarted after an update.

To inspect without installing: `bash install-osint-sentinel.sh --help`. The readable source installer is `osint-sentinel/install-all-termux.sh` in the complete ZIP. The embedded payload has a SHA-256 integrity check; it detects copying damage, not a maliciously replaced installer. Compare against COMPLETE-SHA256SUMS from a trusted copy if needed.
