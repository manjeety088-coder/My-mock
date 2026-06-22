SZX ONE CLICK DOWNLOAD PACK

player.html:
- MP4 direct link par Download click karte hi download start.
- HLS/m3u8 par agar DOWNLOAD_SERVER set hai to MP4 download start.
- DOWNLOAD_SERVER blank hai to sirf .m3u8 playlist download/open hogi.

HLS/m3u8 ko MP4 me one-click download karne ke liye:
1. pip install flask
2. winget install Gyan.FFmpeg
3. python download_server.py
4. player.html me line set karo:
   const DOWNLOAD_SERVER="http://YOUR_PUBLIC_IP:5000/download";

Agar EdgeOne HTTPS par player upload hai to download server bhi HTTPS hona better hai.
