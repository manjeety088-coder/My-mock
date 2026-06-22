import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

WORKER_PREFIX = "https://szx-proxy.manjeety088.workers.dev/?url="

def clean_name(name):
    name = re.sub(r'[\\/:*?"<>|]+', "_", str(name or "SZX_Video"))
    name = re.sub(r"\s+", " ", name).strip()
    return name[:120] or "SZX_Video"

def origin_headers(url):
    try:
        p = urlparse(url)
        origin = f"{p.scheme}://{p.netloc}"
        return f"Referer: {origin}/\r\nOrigin: {origin}\r\n"
    except Exception:
        return ""

def pick_link(item):
    keys = ["m3u8","url","video","link","video_url","videoUrl","src","file","file_url","stream","stream_url","play_url","playUrl"]
    for k in keys:
        if isinstance(item, dict) and item.get(k):
            return item[k]
    if isinstance(item, dict):
        for v in item.values():
            if isinstance(v, dict):
                f = pick_link(v)
                if f: return f
    return ""

def pick_title(item, fallback):
    if not isinstance(item, dict): return fallback
    if item.get("subject") or item.get("chapter") or item.get("class_no"):
        parts=[]
        if item.get("subject"): parts.append(str(item["subject"]))
        if item.get("chapter"): parts.append(str(item["chapter"]).replace("_", " "))
        if item.get("class_no"): parts.append("Class " + str(item["class_no"]))
        return " - ".join(parts)
    for k in ["title","name","className","class_name","lesson_name","lecture","topic","chapter"]:
        if item.get(k): return str(item[k])
    return fallback

def get_array(data):
    if isinstance(data, list): return data
    if isinstance(data, dict):
        for k in ["classes","videos","lectures","items","data","results"]:
            if isinstance(data.get(k), list): return data[k]
    return []

def find_item(data, class_no=None, idx=None, id_=None):
    arr = get_array(data)
    if not arr: return None
    if class_no is not None:
        for x in arr:
            if str(x.get("class_no")) == str(class_no) or str(x.get("class")) == str(class_no) or str(x.get("no")) == str(class_no): return x
    if idx is not None: return arr[int(idx)]
    if id_ is not None:
        for x in arr:
            if str(x.get("class_no")) == str(id_) or str(x.get("class")) == str(id_) or str(x.get("no")) == str(id_): return x
        n = int(id_)
        if 0 <= n < len(arr): return arr[n]
        if 0 <= n - 1 < len(arr): return arr[n-1]
    return arr[0]

def run(cmd):
    print("\nRunning:\n" + " ".join(('"'+str(x)+'"') if " " in str(x) else str(x) for x in cmd) + "\n")
    return subprocess.run(cmd).returncode == 0

def download_with_n_m3u8dl(url, out_dir, name):
    exe = shutil.which("N_m3u8DL-RE") or shutil.which("N_m3u8DL-RE.exe")
    if not exe: return False
    cmd = [exe, url, "--save-dir", str(out_dir), "--save-name", name, "--auto-select", "--thread-count", "16", "--download-retry-count", "20", "--del-after-done"]
    return run(cmd)

def download_with_ffmpeg(url, output):
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("ERROR: ffmpeg install nahi hai.")
        print("Windows me try karo: winget install Gyan.FFmpeg")
        return False
    cmd = [ffmpeg, "-hide_banner", "-y", "-user_agent", "Mozilla/5.0"]
    headers = origin_headers(url)
    if headers: cmd += ["-headers", headers]
    cmd += ["-allowed_extensions", "ALL", "-protocol_whitelist", "file,http,https,tcp,tls,crypto", "-i", url, "-c", "copy", "-movflags", "+faststart", str(output)]
    return run(cmd)

def main():
    ap = argparse.ArgumentParser(description="SZX fast HLS/MP4 downloader")
    ap.add_argument("--url")
    ap.add_argument("--json")
    ap.add_argument("--class_no", "--class", dest="class_no")
    ap.add_argument("--id")
    ap.add_argument("--idx")
    ap.add_argument("--name")
    ap.add_argument("--out", default="downloads")
    ap.add_argument("--proxy", action="store_true")
    ap.add_argument("--engine", choices=["auto","ffmpeg","n_m3u8dl"], default="auto")
    args = ap.parse_args()
    url = args.url
    name = args.name or "SZX_Video"
    if args.json:
        data = json.loads(Path(args.json).read_text(encoding="utf-8"))
        item = find_item(data, class_no=args.class_no, idx=args.idx, id_=args.id)
        if not item:
            print("ERROR: JSON me class nahi mili."); sys.exit(1)
        url = pick_link(item)
        name = args.name or pick_title(item, "SZX_Video")
    if not url:
        print('Example: python szx_fast_downloader.py --json arithmetic.json --class_no 1')
        print('Example: python szx_fast_downloader.py --url "https://example.com/master.m3u8" --name "Class 1"')
        sys.exit(1)
    if args.proxy:
        url = WORKER_PREFIX + url
    out_dir = Path(args.out); out_dir.mkdir(parents=True, exist_ok=True)
    safe = clean_name(name); output = out_dir / (safe + ".mp4")
    print("Title:", safe); print("Output:", output); print("Mode:", "PROXY" if args.proxy else "DIRECT FAST")
    ok = False
    if args.engine in ("auto", "n_m3u8dl"):
        ok = download_with_n_m3u8dl(url, out_dir, safe)
        if ok: print("\nDone with N_m3u8DL-RE."); return
    if args.engine in ("auto", "ffmpeg"):
        ok = download_with_ffmpeg(url, output)
        if ok: print("\nDone:", output); return
    print('\nDownload failed. Proxy fallback try: python szx_fast_downloader.py --url "YOUR_M3U8" --name "video" --proxy')

if __name__ == "__main__":
    main()
