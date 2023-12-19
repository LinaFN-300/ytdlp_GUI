from yt_dlp import YoutubeDL

url = 'https://twitter.com/i/status/1736748158393176224'
ydl_opts ={}


with YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
