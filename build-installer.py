from pathlib import Path
import base64,io,tarfile,hashlib,zipfile
root=Path(__file__).resolve().parent
src=root/'osint-sentinel'
files=sorted(p for p in src.iterdir() if p.is_file())
buf=io.BytesIO()
with tarfile.open(fileobj=buf,mode='w:gz') as tar:
    for p in files:tar.add(p,arcname=p.name)
payload=buf.getvalue()
header='''#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == --help ]]; then
    echo 'OSINT Sentinel complete phone installer'
    echo 'Usage: bash /sdcard/Download/install-osint-sentinel.sh'
    echo 'Requires native Termux, internet, and sufficient free storage.'
    echo 'Installs missing Debian, Sentinel, Sherlock, Maigret, and widget script.'
    echo 'Termux and compatible Termux:Widget Android apps need manual installation.'
    exit 0
fi
[[ $# == 0 ]] || { echo 'Unknown option. Use --help.' >&2; exit 1; }
[[ "${PREFIX:-}" == /data/data/com.termux/files/usr && "$HOME" == /data/data/com.termux/files/home ]] || {
    echo 'Run inside native Termux, outside Debian.' >&2
    exit 1
}
umask 077
mkdir -p "$HOME/.cache/osint-sentinel"
work_dir=$(mktemp -d "$HOME/.cache/osint-sentinel/bundle.XXXXXXXX")
trap 'rm -rf -- "$work_dir"' EXIT
sed '1,/^__SENTINEL_PAYLOAD__$/d' "${BASH_SOURCE[0]}" | base64 -d > "$work_dir/bundle.tar.gz"
expected_sha=PAYLOAD_SHA
actual_sha=$(sha256sum "$work_dir/bundle.tar.gz")
[[ "${actual_sha%% *}" == "$expected_sha" ]] || { echo 'Installer payload damaged; copy the file again.' >&2; exit 1; }
tar -xzf "$work_dir/bundle.tar.gz" -C "$work_dir"
bash "$work_dir/install-all-termux.sh"
exit 0
__SENTINEL_PAYLOAD__
'''.replace('PAYLOAD_SHA',hashlib.sha256(payload).hexdigest())
out=root/'install-osint-sentinel.sh'
out.write_text(header+base64.encodebytes(payload).decode())
out.chmod(0o755)
with zipfile.ZipFile(root/'osint-sentinel-complete.zip','w',zipfile.ZIP_DEFLATED) as z:
    z.write(out,out.name)
    for p in files:z.write(p,'osint-sentinel/'+p.name)
(root/'COMPLETE-SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in [out,root/'osint-sentinel-complete.zip']))
print(out)
