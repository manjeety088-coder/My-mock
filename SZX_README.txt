SZX ADVANCED PLAYER + FAST DOWNLOADER

1) player_advanced_direct_proxy_download.html ko rename karo:
   player.html

2) Upload folder me daal do.

Use:
   player.html?json=arithmetic.json&class_no=1
   player.html?subject=arithmetic&class_no=1
   player.html?m3u8=VIDEO_LINK&title=Class Name

Player buttons:
   Direct Fast  = proxy ke bina fastest try karega
   Proxy        = tumhara worker use karega
   Auto         = direct first, fail hua to proxy fallback
   Play in Tab  = direct raw video browser tab me open karega
   Download     = MP4 direct download; HLS me m3u8 open/download karega

Full HLS ko MP4 me download karna ho to browser se nahi hota.
Uske liye local PC/mobile me ffmpeg/N_m3u8DL-RE chahiye.

Fast downloader examples:
   python szx_fast_downloader.py --json arithmetic.json --class_no 1
   python szx_fast_downloader.py --url "https://example.com/master.m3u8" --name "Class 1"

Agar ffmpeg missing ho Windows me:
   winget install Gyan.FFmpeg

N_m3u8DL-RE installed hoga to script auto use karega, nahi to ffmpeg use karega.
