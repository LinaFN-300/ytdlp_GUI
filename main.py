#ライブラリのimport
import tkinter as tk
from yt_dlp import YoutubeDL
import ffmpeg

#関数定義
def download(url):
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

#設定の読み込み
config_file = open('config','r')
ydl_opts = {config_file.read}
config_file.close

#
win = tk.Tk()
win.title(u"yt-dlp GUI")
win.geometry("800x450")

#ラベル
label1 = tk.Label(text=u'URL->')
label1.place(x=30, y=20)

#エントリー
InputURLBox = tk.Entry(width=100)
InputURLBox.place(x=70, y=20)

win.mainloop()