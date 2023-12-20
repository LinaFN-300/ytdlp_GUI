#ライブラリのimport
import json
from threading import Thread

import tkinter as tk
from tkinter import filedialog

from yt_dlp import YoutubeDL
            
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

#進捗情報を処理するフック関数
def progress_hooks(d):
    if d['status'] == 'downloading':
        #if 'eta' in d:
            logbox.insert(tk.END, f"Downloading {d['tmpfilename']} ETA: {d['eta']}"+" seconds\n")
            logbox.see(tk.END)

#設定の読み込み
def config_read():
    config_open = open('config.json', 'r')
    ydl_opts = json.load(config_open)
    ydl_opts = dict(ydl_opts, progress_hooks=[progress_hooks])
    print(ydl_opts)
    return ydl_opts

#設定の書き込み
def config_write(conf):
    conf = dict(conf, writethumbnail="True")
    config_open = open('config.json', 'w')
    json.dump(conf, config_open, indent=4)

#GUIの作成
def start_GUI():
    #windowの作成
    global win
    win = tk.Tk()
    win.title(u"yt-dlp GUI")
    win.geometry("515x360")

    #URL入力欄
    #ラベル
    label1 = tk.Label(text=u'URL->')
    label1.place(x=5, y=20)
    #入力欄
    InputURLBox = tk.Entry(width=63)
    InputURLBox.place(x=45, y=20)

    #ダウンロードボタン
    DLButton = tk.Button(text=u'Download', width=10)
    DLButton.bind("<Button-1>", lambda event: Thread(target=download, args=(InputURLBox.get(),)).start())
    DLButton.bind("<Button-1>", lambda event: InputURLBox.delete(0, tk.END), "+")
    DLButton.place(x=430, y=17)

    #ステータスバー
    global statusbar
    statusbar = tk.Entry(width=13)
    statusbar.insert(tk.END, "Stundby!")
    statusbar.place(x=45, y=45)

    #進捗
    global progress_info, logbox
    logbox = tk.Text(width=60, height=20)
    logbox.bind("<Key>", lambda a: "break")
    logbox.place(x=45, y=70)

    #設定画面を開くボタン
    ConfigButton = tk.Button(text=u'Config', width=10)
    ConfigButton.bind("<Button-1>", lambda event: config_window())
    ConfigButton.place(x=430, y=42)

    win.mainloop()

#設定画面(サブウィンドウ)
def config_window():
    #windowの作成
    global config_win
    config_win = tk.Toplevel(win)
    config_win.title(u"Config Menu")
    config_win.geometry("460x200")

    #保存先のpath指定
    #ラベル
    label1 = tk.Label(config_win, text=u'ダウンロード先->')
    label1.place(x=5, y=20)
    #path入力欄
    InputPathBox = tk.Entry(config_win, width=60)
    InputPathBox.place(x=85, y=20)
    #フォルダー選択ボタン
    PathButton = tk.Button(config_win, text=u'参照', width=3)
    PathButton.place(x=420, y=17)
    PathButton.bind("<Button-1>", lambda event: InputPathBox.insert(tk.END, filedialog.askdirectory()))
    
    #音声だけダウンロードするかどうか
    #ラベル
    label2 = tk.Label(config_win, text=u'音声のみダウンロード')
    label2.place(x=40, y=45)
    #チェックボックス
    AudioOnly = tk.BooleanVar()
    AudioOnly.set(False)
    CheckButton = tk.Checkbutton(config_win, variable=AudioOnly)
    CheckButton.place(x=10, y=45)
    
    #ブラウザからcookieを取得するかどうか
    #ラベル
    label3 = tk.Label(config_win, text=u'ブラウザからcookieを取得：ブラウザ名->')
    label3.place(x=40, y=70)
    #チェックボックス
    CookieFromBrowser = tk.BooleanVar()
    CookieFromBrowser.set(False)
    CheckButton = tk.Checkbutton(config_win, variable=CookieFromBrowser)
    CheckButton.place(x=10, y=70)
    #ブラウザ名入力欄
    InputBrowserBox = tk.Entry(config_win, width=10)
    InputBrowserBox.place(x=240, y=70)
    
    #cookieのpath指定
    #ラベル
    label4 = tk.Label(config_win, text=u'cookieをファイルから取得')
    label4.place(x=40, y=95)
    #チェックボックス
    Cookie = tk.BooleanVar()
    Cookie.set(False)
    CheckButton = tk.Checkbutton(config_win, variable=Cookie)
    CheckButton.place(x=10, y=95)
    #ラベル
    label5 = tk.Label(config_win, text=u'cookies.txt->')
    label5.place(x=5, y=120)
    #path入力欄
    InputCookieBox = tk.Entry(config_win, width=60)
    InputCookieBox.place(x=85, y=120)
    #ファイル選択ボタン
    CookieButton = tk.Button(config_win, text=u'参照', width=3)
    CookieButton.place(x=420, y=117)
    CookieButton.bind("<Button-1>", lambda event: InputCookieBox.insert(tk.END, filedialog.askopenfilename()))
    
    #設定を保存するボタン
    SaveButton = tk.Button(config_win, text=u'保存', width=63)
    SaveButton.place(x=5, y=150)
    SaveButton.bind("<Button-1>", lambda event: SaveConfig())
    
    #設定を保存
    def SaveConfig():
        conf = {}
        conf = dict(conf, outtmpl=InputPathBox.get()+"/%(title)s.%(ext)s")
        if AudioOnly.get() == True:
            conf = dict(conf, format="bestaudio")
            conf = dict(conf, postprocessors=[{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}])
        else:
            conf = dict(conf, format="bestvideo+bestaudio/best")
        if CookieFromBrowser.get() == True:
            conf = dict(conf, cookieflombrowser=InputBrowserBox.get())
        if Cookie.get() == True:
            conf = dict(conf, cookiefile=InputCookieBox.get())
        config_write(conf)
            
    
    config_win.mainloop()

#ステータスバーの更新
#ダウンロード開始時の処理
def dl_start():
    statusbar.delete(0, tk.END)
    statusbar.insert(tk.END, "Downloading...")

#ダウンロード成功時の処理
def dl_success():
    statusbar.delete(0, tk.END)
    statusbar.insert(tk.END, "Success!")
    logbox.insert(tk.END, "Done.\n\n")

#ダウンロード失敗時の処理
def dl_error():
    statusbar.delete(0, tk.END)
    statusbar.insert(tk.END, "Error")



if __name__ == "__main__":
    start_GUI()
