#ライブラリのimport
import json
from threading import Thread

import tkinter as tk

from yt_dlp import YoutubeDL
import ffmpeg


def my_hook(d):
    if d['status'] == 'downloading':
        # ETAが存在する場合のみ表示
        if 'eta' in d:
            statusbar.insert(f"Downloading: {d['_percent_str']} and ETA: {d['eta']} seconds")
            #win.update_idletasks()
            print(f"Downloading: {d['_percent_str']} and ETA: {d['eta']} seconds")
            
#関数定義
#ダウンロード関数
def download(url):
    ydl_opts = config_read()
    with YoutubeDL(ydl_opts) as ydl:
        dl_start()
        try:
            ydl.download([url])
            dl_success()
        except:
            dl_error()

#設定の読み込み
def config_read():
    config_open = open('config.json', 'r')
    ydl_opts = json.load(config_open)
    ydl_opts = dict(ydl_opts, progress_hooks=[my_hook])
    print(ydl_opts)
    return ydl_opts

#設定の書き込み
def config_write(conf):
    config_open = open('config.json', 'w')
    json.dump(conf, config_open, indent=4)

#GUIの作成
def start_GUI():
    #windowの作成
    global win
    win = tk.Tk()
    win.title(u"yt-dlp GUI")
    win.geometry("500x450")

    #URL入力欄
    #ラベル
    label1 = tk.Label(text=u'URL->')
    label1.place(x=5, y=20)
    #入力欄
    InputURLBox = tk.Entry(width=60)
    InputURLBox.place(x=45, y=20)

    #ダウンロードボタン
    DLButton = tk.Button(text=u'Download', width=10)
    DLButton.bind("<Button-1>", lambda event: Thread(target=download, args=(InputURLBox.get(),)).start())
    DLButton.bind("<Button-1>", lambda event: InputURLBox.delete(0, tk.END), "+")
    DLButton.place(x=415, y=17)

    #ステータスバー
    global statusbar
    statusbar = tk.Entry(width=20)
    statusbar.insert(tk.END, "Stundby!")
    statusbar.place(x=45, y=45)

    win.mainloop()

#ステータスバーの更新
#ダウンロード開始時の処理
def dl_start():
    statusbar.delete(0, tk.END)
    statusbar.insert(tk.END, "Downloading...")

#ダウンロード成功時の処理
def dl_success():
    statusbar.delete(0, tk.END)
    statusbar.insert(tk.END, "Success!")

#ダウンロード失敗時の処理
def dl_error():
    statusbar.delete(0, tk.END)
    statusbar.insert(tk.END, "Error")



if __name__ == "__main__":
    start_GUI()
