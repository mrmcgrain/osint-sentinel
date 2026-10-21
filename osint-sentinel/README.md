# OSINT Sentinel for Samsung (starter build)

A local-first Android browser dashboard hosted by Python inside an **existing Debian proot**. The package manager installs **Sherlock** and **Maigret** through `pipx`; username searches run in the same environment. Case data and uploaded images stay in `~/osint-sentinel/data` unless you deliberately upload/share elsewhere.

## Install without reinstalling Debian

1. Download `osint-sentinel.zip` to the Samsung Downloads folder. In native Termux (not Debian), run `termux-setup-storage` once if needed.
2. In native Termux:

```sh
pkg install -y proot-distro unzip
mkdir -p ~/sentinel-staging
unzip -o ~/storage/downloads/osint-sentinel.zip -d ~/sentinel-staging
proot-distro login debian
```

3. You are now **inside Debian**. Run:

```sh
mkdir -p ~/osint-sentinel
cp /data/data/com.termux/files/home/sentinel-staging/osint-sentinel/server.py /data/data/com.termux/files/home/sentinel-staging/osint-sentinel/index.html ~/osint-sentinel/
bash /data/data/com.termux/files/home/sentinel-staging/osint-sentinel/install-in-debian.sh
python3 ~/osint-sentinel/server.py
```

4. In Samsung Chrome on the same phone open **http://127.0.0.1:8765**. Use the browser menu **Add to Home screen**. Keep the Termux process running while using the dashboard.
5. Open **Tool Store**. Install Sherlock and/or Maigret. Use **Investigate** to run a public-username search. Use **Reports** to save notes and evidence.

## One-tap Samsung startup

For the existing-install update and Termux:Widget setup, follow [INSTALL-STARTUP.md](INSTALL-STARTUP.md). Use the **OSINT Sentinel** widget entry to launch Debian and the server, then open the dashboard automatically. A Chrome shortcut alone cannot start the server.

## Manual startup (fallback)

In native Termux:

```sh
proot-distro login debian -- python3 /root/osint-sentinel/server.py
```

If your Debian user is not root, change `/root/` to its actual home path, or simply enter Debian then run `python3 ~/osint-sentinel/server.py`.

## Notes / limits

- If Debian cannot access the staging files at `/data/data/com.termux/files/home/...`, from *native Termux* copy files into a shared storage folder after `termux-setup-storage`, and from Debian read them from `/sdcard/Download/` (depending on proot mounts).
- The dashboard listens only on `127.0.0.1`, not your network, and mutating requests require a per-start browser token. It is meant as a single-user local app, not a multiuser internet service.
- Package installation and searches require network access; dependent Python packages may fail to compile on some ARM64 proot setups. No fake success is reported.
- The image page is a **local organizer plus handoff** to Google Lens, TinEye, Bing, or Yandex. It does **not** claim to automate reverse-image searching or receive matches from those providers. The external provider will receive any picture you upload there.
- Search output is shown in the current session; Sherlock text and Maigret HTML are also retained in `~/osint-sentinel/data/` and can be reviewed in Debian. This MVP does not automatically embed raw search output inside saved case files.
- Checks can produce false positives. No automated identity assertions or definitive scam probability are provided. Only investigate public information and avoid uploading sensitive personal images without permission.
- If tools need changing, use Tool Store; it only offers the allowlisted tools, not arbitrary shell commands or unknown GitHub install scripts.

## Sherlock search coverage

Sherlock now runs with adult sites enabled and all site results visible by default. Uncheck **Show all Sherlock results** to hide misses while retaining errors. After completion the dashboard displays checked results, possible matches, misses, blocked/errors, and username-rule skips from Sherlock's CSV report. Upstream exclusions for unreliable sites remain active and are not included in those totals. Coverage depends on Sherlock's site list and site availability; a match does not establish identity.

Each new search saves CSV and text reports in Debian `~/osint-sentinel/data/sherlock-<runid>/`. The 10-minute job limit is unchanged; timeouts show partial output and an incomplete-results warning.
