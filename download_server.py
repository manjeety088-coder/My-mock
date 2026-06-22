from flask import Flask, request, Response, jsonify
from urllib.parse import urlparse
import subprocess
import re
import os
import shutil

app = Flask(__name__)

def safe_name(name):
    name = re.sub(r'[\\/:*?"<>|]+', "_", str(name or "SZX_Video"))
    name = re.sub(r"\s+", " ", name).strip()
    return (name[:100] or "SZX_Video") + ".mp4"

def origin_headers(url):
    try:
        p = urlparse(url)
        origin = f"{p.scheme}://{p.netloc}"
        return f"Referer: {origin}/\r\nOrigin: {origin}\r\n"
    except Exception:
        return ""

@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Range"
    resp.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return resp

@app.route("/")
def home():
    return "SZX Download Server Running. Use /download?url=VIDEO_M3U8&name=Class"

@app.route("/download")
def download():
    url = request.args.get("url", "").strip()
    name = safe_name(request.args.get("name", "SZX_Video"))

    if not url.startswith(("http://", "https://")):
        return jsonify({"error": "Invalid URL"}), 400

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return jsonify({"error": "ffmpeg not installed. Windows: winget install Gyan.FFmpeg"}), 500

    headers = origin_headers(url)
    cmd = [ffmpeg, "-hide_banner", "-loglevel", "error", "-user_agent", "Mozilla/5.0"]
    if headers:
        cmd += ["-headers", headers]
    cmd += [
        "-allowed_extensions", "ALL",
        "-protocol_whitelist", "file,http,https,tcp,tls,crypto",
        "-i", url,
        "-c", "copy",
        "-bsf:a", "aac_adtstoasc",
        "-movflags", "frag_keyframe+empty_moov+faststart",
        "-f", "mp4",
        "pipe:1"
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1024 * 1024)

    def generate():
        try:
            while True:
                chunk = process.stdout.read(1024 * 1024)
                if not chunk:
                    break
                yield chunk
        finally:
            try:
                process.kill()
            except Exception:
                pass

    return Response(
        generate(),
        mimetype="video/mp4",
        headers={
            "Content-Disposition": f'attachment; filename="{name}"',
            "Cache-Control": "no-store",
            "X-Accel-Buffering": "no"
        }
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, threaded=True)
