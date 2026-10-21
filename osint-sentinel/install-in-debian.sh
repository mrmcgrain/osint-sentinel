#!/bin/bash
set -euo pipefail
if ! grep -qi debian /etc/os-release; then echo 'Run this inside your existing Debian proot.';exit 1;fi
apt-get update
apt-get install -y python3 python3-venv python3-pip pipx ca-certificates
mkdir -p "$HOME/osint-sentinel/data/images" "$HOME/osint-sentinel/data/cases"
echo 'Dependencies ready. Copy server.py and index.html into ~/osint-sentinel, then run: python3 ~/osint-sentinel/server.py'
